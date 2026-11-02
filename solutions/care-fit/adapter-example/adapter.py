"""Starting adapter: delegates to the deterministic baseline; no model required.

Copy this folder to a named approach, replace solve, and record dependencies and
limitations. Only the input case is passed to solve; do not load expected files.
"""
from labbench.baseline import solve as baseline_solve


def solve(case):
    return baseline_solve(case)
