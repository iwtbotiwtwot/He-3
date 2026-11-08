# Reproducibility

Run `python3 -I -B reproduce.py` from the repository, or supply its absolute path from any working directory. Python 3.12 is the tested baseline; the scientific scripts use only its standard library. `--output` accepts a new path, including a path containing spaces. Every subprocess uses an argument list and Python isolation.

The root runner first verifies the SHA-256 and size of all files listed in `provenance/EVIDENCE_MANIFEST.json`. It then executes the original public-case commands from the case directories' `REPRODUCE.md`, passing explicit relocated paths. These mathematical scripts and their original source freezes are copied byte-for-byte.

| Execution | Expected readback |
|---|---|
| Payment A and B | Fresh rows match each route's retained results; literal source matrices agree; both bounds are negative at the common conservative ceilings |
| He-3 verification | Result file is byte-identical; all 285 checks and seven controls pass |
| Free reference | Result file is byte-identical; 247 checks and five controls pass |
| Shared-field covariance | All mathematical results and operand/control files match; only the recorded completion time differs; 108 checks and six controls pass |

The final `SUMMARY.json` reports the check counts and executions. Each command's stdout/stderr is saved separately. A failure leaves a `FAILED.json` and the relevant logs. No previous output directory is reused or removed.

`python3 -I -B reproduce.py --verify-only` authenticates evidence without executing the mathematics. Exact arithmetic decisions use integers, fractions and outward bounds; decimal displays are not certificate thresholds.

No engine, AI service, network, historical absolute path or separate SAM installation is needed for these replays. Some preserved provenance records contain the original absolute paths; they are historical descriptions. Original scripts with an optional historical default always receive an explicit repository-local `--case` argument from the runner.

The packet contains finite source reconstruction, exact upper-bound arithmetic, interval witnesses, proof texts and their premises. It does not freshly integrate the historical profile moments or complete correlated gate bound. Reproduction of a theorem with those premises preserves that dependency.

The assembly checks are retained in [PACKAGE_QA.json](../provenance/PACKAGE_QA.json). A clean local Git clone was replayed from a different working directory, with spaces in both checkout and output paths. Both the initial and relocated replays passed. Their complete outputs and logs are preserved in `provenance/initial_replay.tar.gz` and `provenance/portable_replay.tar.gz`; [REPLAY_ARCHIVES.json](../provenance/REPLAY_ARCHIVES.json) records every member's size and SHA-256 and the successful archive readbacks. Extract either archive into a new empty directory to inspect its `SUMMARY.json`, readbacks and execution logs.
