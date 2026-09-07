#!/usr/bin/env python3
"""Launch a documented quorum once, without CLI discovery or shell evaluation."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import signal
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
        self.lock = threading.Lock()
        self.cancelled = threading.Event()
        run_id = uuid.uuid4().hex[:12]
        for index, worker in enumerate(workers, 1):
            worker["name"] = f"hq-{run_id}-{index}"
        self.state = {"run_id": run_id, "cwd": os.getcwd(),
                      "caller_pane": os.environ["HERDR_PANE_ID"],
                      "created_at": time.time(), "workers": workers}
        (self.directory / "brief.txt").write_text(brief)
        self.record(event="created")

    def record(self, worker=None, event="progress", **changes):
        with self.lock:
            target = worker if worker is not None else self.state
            target.update(changes)
            temporary = self.directory / "run.json.tmp"
            temporary.write_text(json.dumps(self.state, indent=2) + "\n")
            temporary.replace(self.directory / "run.json")
            print(json.dumps({"event": event, "run_dir": str(self.directory),
                              "worker": worker, **({} if worker else changes)}), flush=True)


def create_panes(run, direction=None):
    # Reserve one sibling area, then split only this run's panes. Re-read geometry
    # inside the helper so resize events do not become model decisions.
    owned = []
    caller = run.state["caller_pane"]
    for worker in run.state["workers"]:
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
        command = ["agent", "prompt", worker["name"], brief]
        response = None
        submitted_at = time.time()
        # Start the budget at submission, not when a later join happens. Native
        # configuration/permissions are untouched. Never reuse a conversation.
        run.record(worker, event="dispatching", status="dispatching", submitted_at=submitted_at,
                   deadline=submitted_at + BRIEF_BUDGET_SECONDS)
        prompted = response = herdr(command, timeout=30)
        agent = prompted["agent"]
        if (not isinstance(agent, dict) or agent.get("name") != worker["name"]
                or agent.get("pane_id") != worker["pane_id"]):
            raise ValueError("Prompt response does not match the requested worker")
        run.record(worker, event="dispatched", status="dispatched",
                   dispatch_returned_at=time.time(), dispatch_state=agent)
    except (CommandError, ValueError, KeyError, TypeError) as error:
        details = error.details if isinstance(error, CommandError) else {
            "reason": str(error), "argv": ["herdr", *command], "response": response}
        run.record(worker, event="failed", status=f"{stage}_failed", error=details)


def launch(workers, brief, direction=None):
    if os.environ.get("HERDR_ENV") != "1" or not os.environ.get("HERDR_PANE_ID"):
        raise ValueError("Run inside a Herdr-managed pane (HERDR_ENV=1 and HERDR_PANE_ID required)")
    if not brief.strip():
        raise ValueError("Provide the common brief on stdin")
    run = Run(workers, brief)
    try:
        create_panes(run, direction)
    except (CommandError, ValueError, KeyError, TypeError) as error:
        # Layout mutations depend on earlier responses: abort this phase rather
        # than guessing IDs or choosing replacement panes. Retain partial state.
        details = error.details if isinstance(error, CommandError) else {"reason": str(error)}
        for worker in workers:
            run.record(worker, event="failed", status="layout_failed", error=details)
        return run, 1
    with ThreadPoolExecutor(max_workers=len(workers)) as pool:
        try:
            futures = [pool.submit(start_and_dispatch, run, worker, brief) for worker in workers]
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            # In-flight starts may still finish. Prevent their subsequent prompts;
            # the lead owns inspection/interruption of workers already dispatched.
            run.cancelled.set()
            run.record(event="launch_interrupted", interrupted_at=time.time())
            raise
    run.record(event="launch_complete", launch_completed_at=time.time())
    return run, int(any(worker["status"] != "dispatched" for worker in workers))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="append", required=True, metavar="CLI|MODEL|REASONING")
    parser.add_argument("--direction", choices=("right", "down"), help="Requested first split direction")
    args = parser.parse_args()

    def interrupt(signum, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupt)
    try:
        workers = parse_workers(args.worker)
        _, status = launch(workers, sys.stdin.read(), args.direction)
        return status
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Launch interrupted. Inspect the printed run_dir/run.json and this run's panes; "
              "do not relaunch automatically. Interrupt any working workers through Herdr.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
