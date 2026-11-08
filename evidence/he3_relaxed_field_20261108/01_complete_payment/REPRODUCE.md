# Engine-free reproduction

Tested with Python 3.12, standard library only. No native runtime, network, original project tree, archived generator or peer service is needed. Replays authenticate the frozen input files, rebuild matrices and bounds, retain all controls, and write only to new output directories. Run from this case directory:

```bash
he3_case_dir="$PWD"
he3_replay_dir=$(mktemp -d)
python3 -I -B peers/A/replay.py --case "$he3_case_dir" --out "$he3_replay_dir/A"
python3 -I -B peers/B/replay.py --case "$he3_case_dir" --output "$he3_replay_dir/B"
python3 -I -B scripts/compare_replays.py --case "$he3_case_dir" --a "$he3_replay_dir/A" --b "$he3_replay_dir/B" --output "$he3_replay_dir/COMPARISON.json"
```

Expect both replays to finish successfully and comparison status PASS. The two newly generated row lists must equal the respective blind retained results exactly. All source matrices must agree and the common sufficient endpoint must give strictly negative signs in both complete gap bounds. Absolute path provenance may differ between machines. The retained reference runs are in `RESULTS/lead_replay/`; their post-blind comparison is `RESULTS/COMPARISON.json`. `RESULTS/PORTABLE_COMPARISON.json` also tests output outside the case.

This reproduces the new finite algebra, rational bounds and interval isolation using the supplied historical continuum/massive/gate enclosures. It does not claim a fresh evaluation of those integrals or an outside human replay. Read `DERIVATION.md` for the analytical inequalities.

The private capsule keeps complete native input/program/output trees, failures, helper, preparation and full original input snapshots. Its sibling archive and delivery receipt are hash-committed in this case; `CAPSULE_DELIVERY.json` names the exact local recovery path and SHA256. The archive was read back file by file, originals retained. Native recipes and engine traces are withheld; none is required for the engine-free replay above. Director approval and publication remain separate from reproducibility.

Next: a new verification case can take the shared conditional statement, rederive it independently, and include controls that break its stated hypotheses.
