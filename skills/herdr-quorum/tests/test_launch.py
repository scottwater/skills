"""Contract tests: all subprocess integration uses a fake Herdr, never live panes."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "launch.py"
spec = importlib.util.spec_from_file_location("quorum_launch", SCRIPT)
launch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launch)

FAKE_HERDR = r'''
import json, os, pathlib, sys, time
root = pathlib.Path(os.environ['FAKE_ROOT'])
a = sys.argv[1:]
with (root / 'calls.jsonl').open('a') as f:
    f.write(json.dumps(a) + '\n')

def emit(result):
    print(json.dumps({'result': result}))

def option(key):
    return a[a.index(key) + 1]

if a[:2] == ['pane', 'layout']:
    state = root / 'panes.json'
    panes = json.loads(state.read_text()) if state.exists() else [
        {'pane_id': 'opaque:caller', 'rect': {'width': 206, 'height': 62}}]
    emit({'layout': {'panes': panes}})
elif a[:2] == ['pane', 'split']:
    state = root / 'panes.json'
    panes = json.loads(state.read_text()) if state.exists() else [
        {'pane_id': 'opaque:caller', 'rect': {'width': 206, 'height': 62}}]
    if os.environ.get('FAKE_LAYOUT_FAIL') and len(panes) == 2:
        print('split rejected', file=sys.stderr)
        sys.exit(1)
    parent = next(p for p in panes if p['pane_id'] == option('--pane'))
    axis = 'width' if option('--direction') == 'right' else 'height'
    parent['rect'][axis] //= 2
    pane = {'pane_id': 'opaque:created-' + str(len(panes) * 17), 'rect': dict(parent['rect'])}
    panes.append(pane)
    state.write_text(json.dumps(panes))
    emit({'pane': pane})
elif a[:2] == ['agent', 'start']:
    model = option('--model')
    if model == 'fail':
        print('{"error":"unsupported model"}', file=sys.stderr)
        sys.exit(2)
    if model == 'bad-json':
        print('not JSON')
        sys.exit(0)
    if model == 'slow':
        # A fast worker must be prompted before this startup completes.
        deadline = time.monotonic() + 3
        while not (root / 'prompted').exists() and time.monotonic() < deadline:
            time.sleep(.01)
        if not (root / 'prompted').exists():
            print('start-all barrier prevented prompt', file=sys.stderr)
            sys.exit(1)
    agent = {'name': a[2], 'pane_id': option('--pane'), 'agent': option('--kind'),
             'interactive_ready': True, 'agent_status': 'idle', 'state_change_seq': 10}
    (root / (a[2] + '.json')).write_text(json.dumps({'agent': agent, 'model': model}))
    if model == 'wrong-pane':
        agent['pane_id'] = 'unrelated:pane'
    emit({'agent': agent})
elif a[:2] == ['agent', 'prompt']:
    data = json.loads((root / (a[2] + '.json')).read_text())
    if data['model'] == 'prompt-fail':
        print('prompt rejected', file=sys.stderr)
        sys.exit(1)
    (root / 'prompted').touch()
    emit({'agent': data['agent']})
else:
    print('Unexpected command: ' + repr(a), file=sys.stderr)
    sys.exit(2)
'''


class WorkerArgumentsTests(unittest.TestCase):
    def test_exact_mappings_and_default(self):
        workers = launch.parse_workers([
            'pi|provider/model|high', 'codex|model|medium', 'claude|alias|low',
            'pi|other|default', 'codex|other|default', 'claude|other|default',
        ])
        self.assertEqual([w['native_args'] for w in workers], [
            ['--model', 'provider/model', '--thinking', 'high'],
            ['--model', 'model', '-c', 'model_reasoning_effort="medium"'],
            ['--model', 'alias', '--effort', 'low'],
            ['--model', 'other'], ['--model', 'other'], ['--model', 'other'],
        ])

    def test_rejects_malformed_duplicate_and_unmapped_workers(self):
        for values in ([], ['pi|model'], ['pi||high'], ['pi|model|'],
                       ['pi|model|high|extra'], ['unknown|model|high'],
                       ['pi|model|high', ' pi | model | high '], ['pi|mo\ndel|high']):
            with self.subTest(values=values), self.assertRaises(ValueError):
                launch.parse_workers(values)

    def test_codex_override_is_quoted_as_data(self):
        effort = 'a"b\\c'
        args = launch.parse_workers([f'codex|model|{effort}'])[0]['native_args']
        self.assertEqual(json.loads(args[-1].split('=', 1)[1]), effort)

    def test_command_timeout_retains_diagnostics(self):
        with patch.object(launch.subprocess, 'run', side_effect=subprocess.TimeoutExpired(
                ['herdr'], 1, output=b'partial', stderr=b'diagnostic')):
            with self.assertRaises(launch.CommandError) as raised:
                launch.herdr(['agent', 'list'])
        self.assertEqual(raised.exception.details['stdout'], 'partial')
        self.assertEqual(raised.exception.details['stderr'], 'diagnostic')

    def test_cancellation_prevents_new_start(self):
        worker = launch.parse_workers(['pi|model|high'])[0]
        worker.update(name='test-worker', pane_id='owned:pane')
        run = SimpleNamespace(cancelled=threading.Event(),
                              record=lambda worker, **changes: worker.update(changes))
        run.cancelled.set()
        with patch.object(launch, 'herdr') as command:
            launch.start_and_dispatch(run, worker, 'brief')
        command.assert_not_called()
        self.assertEqual(worker['status'], 'cancelled')

    def test_cancellation_during_start_prevents_dispatch(self):
        worker = launch.parse_workers(['pi|model|high'])[0]
        worker.update(name='test-worker', pane_id='owned:pane')
        run = SimpleNamespace(cancelled=threading.Event(),
                              record=lambda worker, **changes: worker.update(changes))

        def started(*args, **kwargs):
            run.cancelled.set()
            return {'agent': {'name': worker['name'], 'pane_id': worker['pane_id'],
                              'agent': 'pi', 'interactive_ready': True}}

        with patch.object(launch, 'herdr', side_effect=started) as command:
            launch.start_and_dispatch(run, worker, 'brief')
        self.assertEqual(command.call_count, 1)
        self.assertEqual(worker['status'], 'cancelled')


class LaunchIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        fake = self.bin / 'herdr'
        fake.write_text('#!' + sys.executable + '\n' + FAKE_HERDR)
        fake.chmod(0o755)
        self.project = self.root / 'project'
        self.project.mkdir()
        self.env = {**os.environ, 'HERDR_ENV': '1', 'HERDR_PANE_ID': 'opaque:caller',
                    'FAKE_ROOT': str(self.root), 'PATH': str(self.bin), 'TMPDIR': str(self.root)}

    def run_helper(self, workers, brief='Exact scope. Read only.', extra=(), env=None):
        args = [sys.executable, str(SCRIPT)]
        for worker in workers:
            args += ['--worker', worker]
        result = subprocess.run([*args, *extra], input=brief, text=True, capture_output=True,
                                cwd=self.project, env={**self.env, **(env or {})}, timeout=15)
        events = [json.loads(line) for line in result.stdout.splitlines()]
        state = (json.loads((Path(events[0]['run_dir']) / 'run.json').read_text())
                 if events else None)
        calls_file = self.root / 'calls.jsonl'
        calls = [json.loads(line) for line in calls_file.read_text().splitlines()] if calls_file.exists() else []
        return result, events, state, calls

    def test_direct_launch_preserves_brief_config_cwd_focus_and_ids(self):
        model = 'provider/$(touch should-not-exist); "literal"'
        brief = 'Review exact SHA..SHA.\nDo not run tests.\n'
        result, events, state, calls = self.run_helper([
            f'pi|{model}|high', 'codex|model|medium', 'claude|alias|default'], brief)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual((Path(events[0]['run_dir']) / 'brief.txt').read_text(), brief)
        starts = [a for a in calls if a[:2] == ['agent', 'start']]
        prompts = [a for a in calls if a[:2] == ['agent', 'prompt']]
        splits = [a for a in calls if a[:2] == ['pane', 'split']]
        self.assertEqual(len(starts), 3)
        self.assertEqual(len(prompts), 3)
        self.assertTrue(all(a[3] == brief for a in prompts))
        self.assertTrue(all('--wait' not in a for a in prompts))
        self.assertTrue(any(a[a.index('--') + 1:] == ['--model', model, '--thinking', 'high'] for a in starts))
        self.assertTrue(all('--no-focus' in a and a[a.index('--cwd') + 1] == str(self.project.resolve()) for a in splits))
        self.assertEqual(splits[0][splits[0].index('--pane') + 1], 'opaque:caller')
        self.assertTrue(all(a[a.index('--pane') + 1] != 'opaque:caller' for a in splits[1:]))
        self.assertEqual({w['pane_id'] for w in state['workers']},
                         {'opaque:created-17', 'opaque:created-34', 'opaque:created-51'})
        for worker in state['workers']:
            self.assertEqual(worker['status'], 'dispatched')
            self.assertEqual(worker['deadline'] - worker['submitted_at'], 600)
            self.assertLessEqual(worker['ready_at'], worker['submitted_at'])
            self.assertRegex(worker['name'], r'^hq-[a-f0-9]{12}-[1-9][0-9]*$')
        self.assertTrue(all(a[:2] in [['pane', 'layout'], ['pane', 'split'],
                                     ['agent', 'start'], ['agent', 'prompt']] for a in calls))

    def test_fast_worker_dispatched_before_slow_start_finishes(self):
        result, _, state, _ = self.run_helper(['pi|slow|high', 'claude|fast|default'])
        self.assertEqual(result.returncode, 0, result.stderr)
        slow, fast = state['workers']
        self.assertLess(fast['dispatch_returned_at'], slow['ready_at'])

    def test_worker_failure_does_not_retry_or_block_survivors(self):
        result, _, state, calls = self.run_helper(['pi|fail|high', 'claude|fast|medium'])
        self.assertEqual(result.returncode, 1)
        failed, survivor = state['workers']
        self.assertEqual(failed['status'], 'startup_failed')
        self.assertEqual(failed['error']['exit_code'], 2)
        self.assertIn('unsupported model', failed['error']['stderr'])
        self.assertEqual(survivor['status'], 'dispatched')
        self.assertEqual(len([a for a in calls if a[:2] == ['agent', 'start']]), 2)
        self.assertEqual([a[2] for a in calls if a[:2] == ['agent', 'prompt']], [survivor['name']])

    def test_dispatch_failure_is_recorded_once(self):
        result, _, state, calls = self.run_helper(['pi|prompt-fail|high'])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(state['workers'][0]['status'], 'dispatch_failed')
        self.assertEqual(len([a for a in calls if a[:2] == ['agent', 'prompt']]), 1)

    def test_invalid_start_responses_are_not_prompted(self):
        result, _, state, calls = self.run_helper(['pi|bad-json|high', 'pi|wrong-pane|high'])
        self.assertEqual(result.returncode, 1)
        self.assertTrue(all(w['status'] == 'startup_failed' for w in state['workers']))
        self.assertFalse(any(a[:2] == ['agent', 'prompt'] for a in calls))

    def test_partial_layout_failure_preserves_created_pane_without_launching(self):
        result, _, state, calls = self.run_helper(['pi|one|high', 'pi|two|high'],
                                                  env={'FAKE_LAYOUT_FAIL': '1'})
        self.assertEqual(result.returncode, 1)
        self.assertEqual(state['workers'][0]['pane_id'], 'opaque:created-17')
        self.assertNotIn('pane_id', state['workers'][1])
        self.assertTrue(all(w['status'] == 'layout_failed' for w in state['workers']))
        self.assertFalse(any(a[0] == 'agent' for a in calls))

    def test_requested_first_direction(self):
        result, _, _, calls = self.run_helper(['pi|one|default'], extra=['--direction', 'down'])
        self.assertEqual(result.returncode, 0, result.stderr)
        split = next(a for a in calls if a[:2] == ['pane', 'split'])
        self.assertEqual(split[split.index('--direction') + 1], 'down')

    def test_outside_herdr_fails_before_any_command(self):
        result, _, state, calls = self.run_helper(['pi|one|high'], env={'HERDR_ENV': '0'})
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(state)
        self.assertEqual(calls, [])

    def test_invalid_tuple_fails_before_any_command(self):
        result, _, state, calls = self.run_helper(['other|one|high'])
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(state)
        self.assertEqual(calls, [])

    def test_empty_brief_fails_before_any_command(self):
        result, _, state, calls = self.run_helper(['pi|one|high'], brief='  \n')
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(state)
        self.assertEqual(calls, [])

    def test_missing_binary_fails_without_discovery(self):
        (self.bin / 'herdr').unlink()
        result, _, state, calls = self.run_helper(['pi|one|high'])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(state['workers'][0]['status'], 'layout_failed')
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
