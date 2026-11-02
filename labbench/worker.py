"""One local adapter invocation. This process is not a security sandbox."""
import importlib.util
import json
from pathlib import Path
import sys
import time
from .contract import loads


def main():
    cpu_start = time.process_time()
    try:
        case = loads(sys.stdin.read())
        if len(sys.argv) > 1:
            path = Path(sys.argv[1]).resolve()
            sys.path.insert(0, str(path.parent))
            spec = importlib.util.spec_from_file_location("participant_adapter", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            solve = module.solve
        else:
            from .baseline import solve
        response = solve(case)
        print(json.dumps({"response": response, "worker_cpu_seconds": time.process_time() - cpu_start},
                         allow_nan=False))
        return 0
    except Exception as exc:
        # Exclude arbitrary exception text, prompts and credentials from reports.
        print(json.dumps({"error_type": type(exc).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
