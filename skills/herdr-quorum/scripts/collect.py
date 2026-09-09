#!/usr/bin/env python3
"""Block for the next quorum event; cursor replay makes interrupted reads safe."""

import argparse
import json
from pathlib import Path
import socket
import sys
import time


def snapshot(state, after, cancel=False):
    if not 0 <= after <= len(state["events"]):
        raise ValueError("Cursor is outside this run's event history")
    return {"cursor": len(state["events"]), "events": state["events"][after:],
            "complete": state["complete"], "workers": state["workers"],
            "monitor_error": state.get("monitor_error"),
            "cancellation_unavailable": (
                "Monitor finished; no new input sent. Inspect any still-active or unknown workers "
                "and interrupt this run's working agents directly through Herdr."
                if cancel and state["complete"] else None),
            "reason": "complete" if state["complete"] else "events"}


def collect(directory, after=0, timeout=300, cancel=False):
    path = Path(directory) / "run.json"
    state = json.loads(path.read_text())
    result = snapshot(state, after, cancel)
    if state["complete"] or (result["events"] and not cancel):
        return result
    monitor = state.get("monitor")
    if not monitor:
        raise ValueError("Monitor is not ready; inspect run.json and monitor.log, do not relaunch")
    try:
        with socket.create_connection((monitor["host"], monitor["port"]), timeout=5) as connection:
            remaining = max((w.get("deadline", 0) - time.time() for w in state["workers"]), default=0)
            connection.settimeout(max(timeout, remaining if cancel else 0) + 75)
            request = {"token": monitor["token"], "after": after,
                       "timeout": timeout, "cancel": cancel}
            connection.sendall((json.dumps(request) + "\n").encode())
            with connection.makefile("r") as stream:
                line = stream.readline()
            if not line:
                raise OSError("Monitor closed without a response")
            return json.loads(line)
    except OSError as error:
        # Completion can race the connection attempt. Durable events survive the
        # monitor's normal exit; otherwise report loss instead of spinning/relaunching.
        state = json.loads(path.read_text())
        result = snapshot(state, after, cancel)
        if state["complete"] or (result["events"] and not cancel):
            return result
        raise ValueError(f"Monitor unavailable ({error}); inspect this run's panes and monitor.log") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--after", type=int, default=0, help="Cursor from the previous response")
    parser.add_argument("--timeout", type=int, default=300, help="Checkpoint interval, 1–300 seconds")
    parser.add_argument("--cancel", action="store_true", help="Inspect and interrupt this run's working agents")
    args = parser.parse_args()
    if args.after < 0 or not 1 <= args.timeout <= 300:
        parser.error("Use a nonnegative cursor and a timeout from 1 to 300 seconds")
    try:
        print(json.dumps(collect(args.run_dir, args.after, args.timeout, args.cancel)))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
