#!/usr/bin/env python3
"""Launch a documented quorum once, without CLI discovery or shell evaluation."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import signal
import socketserver
import secrets
import subprocess
import sys
import tempfile
import threading
import time
import uuid


START_TIMEOUT_MS = 30_000
BRIEF_BUDGET_SECONDS = 600


def parse_workers(tuples):
    workers = []
    seen = set()
    for value in tuples:
        fields = tuple(part.strip() for part in value.split("|"))
        if len(fields) != 3 or not all(fields):
            raise ValueError(f"Expected cli|model|reasoning: {value!r}")
        if any(any(ord(char) < 32 for char in field) for field in fields):
            raise ValueError(f"Control characters in worker: {value!r}")
        if fields in seen:
            raise ValueError(f"Duplicate worker: {value!r}")
        cli, model, reasoning = fields
        if cli not in ("pi", "codex", "claude"):
            raise ValueError(f"No documented mapping for CLI: {cli!r}")
        args = ["--model", model]
        if reasoning != "default":
            if cli == "codex":
                args += ["-c", "model_reasoning_effort=" + json.dumps(reasoning)]
            else:
                args += ["--thinking" if cli == "pi" else "--effort", reasoning]
        workers.append({"tuple": "|".join(fields), "cli": cli, "native_args": args,
                        "status": "pending"})
        seen.add(fields)
    if not workers:
        raise ValueError("At least one worker is required")
    return workers


class CommandError(Exception):
    def __init__(self, argv, reason, stdout="", stderr="", exit_code=None):
        super().__init__(reason)
        self.details = {"argv": argv, "reason": reason, "exit_code": exit_code,
                        "stdout": stdout, "stderr": stderr}


def herdr(args, timeout=10):
    argv = ["herdr", *args]
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        def text(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        raise CommandError(argv, "Command timed out; outcome may be unknown",
                           text(error.stdout), text(error.stderr)) from error
    except OSError as error:
        raise CommandError(argv, str(error)) from error
    if result.returncode:
        raise CommandError(argv, "Herdr command failed", result.stdout, result.stderr,
                           result.returncode)
    try:
        envelope = json.loads(result.stdout)
        if not isinstance(envelope, dict) or "error" in envelope:
            raise ValueError("Expected a successful JSON envelope")
        payload = envelope["result"]
        if not isinstance(payload, dict):
            raise ValueError("Expected a result object")
        return payload
    except (ValueError, KeyError) as error:
        raise CommandError(argv, f"Unexpected Herdr response: {error}",
                           result.stdout, result.stderr, result.returncode) from error


class Run:
    def __init__(self, workers, brief):
        self.directory = Path(tempfile.mkdtemp(prefix="herdr-quorum-"))
        self.condition = threading.Condition()
        self.cancelled = threading.Event()
        self.active_cancellations = 0
        self.announce = False
        run_id = uuid.uuid4().hex[:12]
        for index, worker in enumerate(workers, 1):
            worker["name"] = f"hq-{run_id}-{index}"
        self.state = {"run_id": run_id, "cwd": os.getcwd(),
                      "caller_pane": os.environ["HERDR_PANE_ID"],
                      "created_at": time.time(), "workers": workers,
                      "events": [], "complete": False, "launch_complete": False}
        (self.directory / "brief.txt").write_text(brief)
        self.record(event="created")

    def record(self, worker=None, event="progress", **changes):
        with self.condition:
            target = worker if worker is not None else self.state
            target.update(changes)
            if worker and event in ("settled", "failed", "cancelled", "deadline", "interrupted", "wait_error"):
                self.state["events"].append({"event": event, "worker": worker.copy()})
            ready = all(w["status"] not in ("pending", "starting", "ready")
                        for w in self.state["workers"])
            announce = self.announce and ready and not self.state["launch_complete"]
            if announce:
                self.state["launch_complete"] = True
            temporary = self.directory / "run.json.tmp"
            temporary.write_text(json.dumps(self.state, indent=2) + "\n")
            temporary.replace(self.directory / "run.json")
            self.condition.notify_all()
            if announce:
                try:
                    print(json.dumps({"event": "launch_complete", "run_dir": str(self.directory)}),
                          flush=True)
                except BrokenPipeError:
                    # A tool timeout can disconnect the launcher; keep monitoring.
                    sys.stdout = open(os.devnull, "w")

    def collect(self, after, timeout):
        with self.condition:
            self.condition.wait_for(
                lambda: len(self.state["events"]) > after or self.state["complete"], timeout)
            # Copy under the lock: worker threads continue mutating the manifest.
            return json.loads(json.dumps({
                "cursor": len(self.state["events"]), "events": self.state["events"][after:],
                "complete": self.state["complete"], "workers": self.state["workers"],
                "monitor_error": self.state.get("monitor_error"),
                "reason": "complete" if self.state["complete"] else
                          "events" if len(self.state["events"]) > after else "checkpoint",
            }))


def create_panes(run, direction=None):
    # Reserve one sibling area, then split only this run's panes. Re-read geometry
    # inside the helper so resize events do not become model decisions.
    owned = []
    caller = run.state["caller_pane"]
    for worker in run.state["workers"]:
        if run.cancelled.is_set():
            return
        layout = herdr(["pane", "layout", "--pane", caller])["layout"]
        candidates = [pane for pane in layout["panes"]
                      if pane["pane_id"] in (owned or [caller])]
        if not candidates:
            raise ValueError("Expected pane missing from caller layout")
        target = max(candidates, key=lambda pane: pane["rect"]["width"] * pane["rect"]["height"])
        rect = target["rect"]
        split_direction = (direction if not owned and direction else
                           "right" if rect["width"] >= 2 * rect["height"] else "down")
        pane = herdr(["pane", "split", "--pane", target["pane_id"],
                      "--direction", split_direction, "--cwd", run.state["cwd"],
                      "--no-focus"])["pane"]
        pane_id = pane["pane_id"]
        if not isinstance(pane_id, str) or not pane_id or pane_id == caller or pane_id in owned:
            raise ValueError("Split did not return a fresh pane ID")
        owned.append(pane_id)
        run.record(worker, event="pane_created", pane_id=pane_id)


def start_and_dispatch(run, worker, brief):
    stage = "startup"
    command = ["agent", "start", worker["name"], "--kind", worker["cli"],
               "--pane", worker["pane_id"], "--timeout", str(START_TIMEOUT_MS),
               "--", *worker["native_args"]]
    response = None
    timer = None
    try:
        if run.cancelled.is_set():
            run.record(worker, event="cancelled", status="cancelled")
            return
        run.record(worker, event="starting", status="starting", start_requested_at=time.time())
        started = response = herdr(command, timeout=START_TIMEOUT_MS / 1000 + 5)
        agent = started["agent"]
        if (not isinstance(agent, dict) or agent.get("name") != worker["name"]
                or agent.get("pane_id") != worker["pane_id"]
                or agent.get("agent") != worker["cli"] or not agent.get("interactive_ready")):
            raise ValueError("Started agent does not match the requested ready worker")
        run.record(worker, event="ready", status="ready", ready_at=time.time(),
                   observed_argv=started.get("argv"))
        if run.cancelled.is_set():
            run.record(worker, event="cancelled", status="cancelled")
            return
        stage = "dispatch"
        command = ["agent", "prompt", worker["name"], brief,
                   "--wait", "--timeout", str(BRIEF_BUDGET_SECONDS * 1000)]
        response = None
        submitted_at = time.time()
        # Start the budget at submission, not when a later join happens. Native
        # configuration/permissions are untouched. Never reuse a conversation.
        run.record(worker, event="waiting", status="waiting", submitted_at=submitted_at,
                   deadline=submitted_at + BRIEF_BUDGET_SECONDS)
        timer = threading.Timer(BRIEF_BUDGET_SECONDS, interrupt_worker,
                                args=(run, worker, "deadline"))
        timer.start()
        if run.cancelled.is_set():
            timer.cancel()
            run.record(worker, event="cancelled", status="cancelled")
            return
        prompted = response = herdr(command, timeout=BRIEF_BUDGET_SECONDS + 5)
        agent = prompted["agent"]
        if (not isinstance(agent, dict) or agent.get("name") != worker["name"]
                or agent.get("pane_id") != worker["pane_id"]
                or agent.get("agent_status") not in ("idle", "done", "blocked")):
            raise ValueError("Prompt response does not match the requested worker")
        timer.cancel()
        timer.join()
        run.record(worker, event="settled", status="settled",
                   settled_at=time.time(), settled_state=agent)
    except (CommandError, ValueError, KeyError, TypeError) as error:
        details = error.details if isinstance(error, CommandError) else {
            "reason": str(error), "argv": ["herdr", *command], "response": response}
        run.record(worker, event="failed", status=f"{stage}_failed", error=details)
        if timer and interrupt_worker(run, worker, "wait_error"):
            timer.cancel()
    finally:
        # Failed/uncertain waits retain their deadline watchdog unless inspection
        # confirms the worker is no longer working. Keep the monitor alive for it.
        if timer:
            timer.join()


def interrupt_worker(run, worker, reason):
    """A wait timeout is not cancellation. Inspect identity/state before input."""
    try:
        agent = herdr(["agent", "get", worker["name"]])["agent"]
        matches = (agent.get("name") == worker["name"] and
                   agent.get("pane_id") == worker.get("pane_id") and
                   agent.get("agent") == worker["cli"])
        interrupted = matches and agent.get("agent_status") == "working"
        if interrupted:
            herdr(["agent", "send-keys", worker["name"], "ctrl+c"])
            agent = herdr(["agent", "get", worker["name"]])["agent"]
        status = agent.get("agent_status")
        inactive = not matches or status in ("idle", "done", "blocked")
        run.record(worker, event=reason, **{reason + "_cleanup": {
            "interrupted": interrupted, "observed_agent": agent,
            "still_active": False if inactive else True if status == "working" else "unknown",
            "identity_matched": matches}})
        return inactive
    except (CommandError, KeyError, TypeError, ValueError) as error:
        run.record(worker, event=reason, **{reason + "_cleanup": {
            "error": error.details if isinstance(error, CommandError) else str(error),
            "still_active": "unknown"}})
        return False


def launch(workers, brief, direction=None, run=None):
    if os.environ.get("HERDR_ENV") != "1" or not os.environ.get("HERDR_PANE_ID"):
        raise ValueError("Run inside a Herdr-managed pane (HERDR_ENV=1 and HERDR_PANE_ID required)")
    if not brief.strip():
        raise ValueError("Provide the common brief on stdin")
    run = run or Run(workers, brief)
    try:
        create_panes(run, direction)
    except (CommandError, ValueError, KeyError, TypeError) as error:
        # Layout mutations depend on earlier responses: abort this phase rather
        # than guessing IDs or choosing replacement panes. Retain partial state.
        details = error.details if isinstance(error, CommandError) else {"reason": str(error)}
        for worker in workers:
            run.record(worker, event="failed", status="layout_failed", error=details)
        return run, 1
    if run.cancelled.is_set():
        for worker in workers:
            run.record(worker, event="cancelled", status="cancelled")
        return run, 1
    with ThreadPoolExecutor(max_workers=len(workers)) as pool:
        try:
            futures = [pool.submit(start_and_dispatch, run, worker, brief) for worker in workers]
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            # In-flight starts may still finish. Prevent their subsequent prompts;
            # the monitor's exception handler cleans up workers already submitted.
            run.record(event="launch_interrupted", interrupted_at=time.time())
            cancel_run(run)
            raise
    return run, int(any(worker["status"] != "settled" for worker in workers))


def budget_brief(brief):
    return (brief.rstrip() + "\n\nExecution budget: You have "
            f"{BRIEF_BUDGET_SECONDS // 60} minutes from submission. Reserve the final minute "
            "to write your report. Prioritize the highest-value investigation. If time runs "
            "short, return supported findings and explicitly identify unfinished scope. "
            "The coordinator enforces the deadline externally.\n")


def cancel_worker(run, worker):
    # Non-working can mean the atomic prompt call is still submitting, not that
    # cancellation succeeded. Wait for activity without polling the lead, until
    # the prompt waiter finishes or its original deadline arrives.
    while worker["status"] == "waiting" and time.time() < worker["deadline"]:
        try:
            agent = herdr(["agent", "get", worker["name"]])["agent"]
            if (agent.get("name") != worker["name"] or
                    agent.get("pane_id") != worker["pane_id"] or
                    agent.get("agent") != worker["cli"] or
                    agent.get("agent_status") not in ("idle", "done")):
                break
            if worker["status"] != "waiting":
                return
            remaining = max(1, min(5000, int((worker["deadline"] - time.time()) * 1000)))
            try:
                herdr(["agent", "wait", worker["name"], "--until", "working",
                       "--until", "blocked", "--timeout", str(remaining)],
                      timeout=remaining / 1000 + 5)
            except CommandError as error:
                # A bounded lifecycle wait may expire after a very fast turn.
                # Only a documented timeout is safe to keep waiting through.
                try:
                    server_error = json.loads(error.details["stderr"])["error"]
                    if server_error.get("code") != "timeout":
                        break
                except (ValueError, KeyError, TypeError, AttributeError):
                    break
        except (CommandError, KeyError, TypeError, ValueError):
            break
    if worker["status"] in ("waiting", "dispatch_failed"):
        interrupt_worker(run, worker, "interrupted")


def cancel_run(run):
    with run.condition:
        if run.state["complete"]:
            return
        run.active_cancellations += 1
        run.cancelled.set()
    try:
        with run.condition:
            workers = [w for w in run.state["workers"]
                       if w["status"] in ("waiting", "dispatch_failed")]
        with ThreadPoolExecutor(max_workers=max(1, len(workers))) as pool:
            list(pool.map(lambda w: cancel_worker(run, w), workers))
    finally:
        with run.condition:
            run.active_cancellations -= 1
            run.condition.notify_all()


def serve(directory):
    run = Run.__new__(Run)
    run.directory = Path(directory)
    run.state = json.loads((run.directory / "run.json").read_text())
    run.condition = threading.Condition()
    run.cancelled = threading.Event()
    run.active_cancellations = 0
    run.announce = True
    token = secrets.token_hex(32)

    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            self.connection.settimeout(5)
            try:
                request = json.loads(self.rfile.readline(65536))
                if not secrets.compare_digest(request.get("token", ""), token):
                    return
                if request.get("cancel"):
                    cancel_run(run)
                after = request["after"]
                timeout = request["timeout"]
                if not isinstance(after, int) or not 0 <= after <= len(run.state["events"]):
                    return
                if not isinstance(timeout, (int, float)) or not 0 <= timeout <= 300:
                    return
                result = run.collect(after, timeout)
                self.wfile.write((json.dumps(result) + "\n").encode())
            except (OSError, ValueError, KeyError, TypeError):
                return

    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
    run.record(event="monitor_ready", monitor={"host": "127.0.0.1",
               "port": server.server_address[1], "token": token, "pid": os.getpid()})
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    def request_cancel(*_):
        threading.Thread(target=cancel_run, args=(run,)).start()

    signal.signal(signal.SIGTERM, request_cancel)
    signal.signal(signal.SIGINT, request_cancel)
    try:
        launch(run.state["workers"], (run.directory / "brief.txt").read_text(),
               run.state.get("direction"), run=run)
    except BaseException as error:
        run.record(event="monitor_failed", monitor_error=str(error))
        cancel_run(run)
    finally:
        with run.condition:
            run.condition.wait_for(lambda: run.active_cancellations == 0)
            run.record(event="complete", complete=True)
        server.shutdown()
        thread.join()
        server.server_close()
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="append", metavar="CLI|MODEL|REASONING")
    parser.add_argument("--direction", choices=("right", "down"), help="Requested first split direction")
    parser.add_argument("--serve", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.serve:
        if os.environ.get("HERDR_ENV") != "1" or not os.environ.get("HERDR_PANE_ID"):
            print("Monitor requires its inherited Herdr execution context", file=sys.stderr)
            return 2
        return serve(args.serve)
    try:
        workers = parse_workers(args.worker or [])
        brief = sys.stdin.read()
        if os.environ.get("HERDR_ENV") != "1" or not os.environ.get("HERDR_PANE_ID"):
            raise ValueError("Run inside a Herdr-managed pane (HERDR_ENV=1 and HERDR_PANE_ID required)")
        if not brief.strip():
            raise ValueError("Provide the common brief on stdin")
        run = Run(workers, budget_brief(brief))
        run.record(direction=args.direction)
        print(json.dumps({"event": "created", "run_dir": str(run.directory)}), flush=True)
        with (run.directory / "monitor.log").open("a") as log:
            process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()),
                                        "--serve", str(run.directory)], stdin=subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=log, text=True,
                                       start_new_session=True)
        # Exactly one startup acknowledgement. The detached monitor owns all later
        # waits; stdout is never used as an assumed model-notification channel.
        line = process.stdout.readline()
        process.stdout.close()
        if not line:
            print("Monitor exited during launch; inspect run.json and monitor.log.", file=sys.stderr)
            return 1
        print(line.rstrip(), flush=True)
        state = json.loads((run.directory / "run.json").read_text())
        return int(any(w["status"].endswith("_failed") for w in state["workers"]))
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Launch interrupted. Inspect the printed run_dir/run.json; do not relaunch. "
              "Use collect.py --run-dir <run_dir> --cancel to interrupt this run.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
