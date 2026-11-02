# Starting adapter

This example calls the deterministic baseline. Copy this folder to a named approach, replace `solve(case)` in `adapter.py`, and record what changed. It demonstrates integration; it is not an independently implemented agent.

From the repository root:

```sh
python -m labbench run --split practice --adapter solutions/care-fit/adapter-example/adapter.py --output results/local/example-practice.json
```

Read the [adapter contract](../../../docs/ADAPTER_CONTRACT.md), then save a [result](../../../docs/RESULT_TEMPLATE.md) and a [progress checkpoint](../../../docs/PROGRESS_TEMPLATE.md) beside your approach. The example needs Python 3.12+ and no third-party packages, models or network access.
