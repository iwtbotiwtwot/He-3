# Engine-free independent replay

Tested with Python 3.12; standard library only. From this case directory:

```bash
he3_case_dir="$PWD"
he3_replay_dir=$(mktemp -d)
python3 -I -B peers/VERIFIER/replay.py --case "$he3_case_dir" --out "$he3_replay_dir/fresh"
python3 -I -B scripts/verify_readback.py --case "$he3_case_dir" --replay "$he3_replay_dir/fresh" --out "$he3_replay_dir/READBACK.json"
```

Expect PASS and verdict HELD, all 285 recorded checks, four certified rows and all seven registered controls. The new result file must be byte-identical to `peers/VERIFIER/RESULTS.json`. Execution timestamps/platform/path provenance may differ. Output directories must be new; the script rejects reuse and retains computational failures. Python isolation prevents incidental environment/module dependencies.

Read the hypothesis map and proof: finite arithmetic plus retained historical premises do not constitute fresh certification of the sharp-profile moments or complete gate inequality. The primary energy certificate uses the universal positive spectral bound rather than the historical numerical retarded-cross lower; metadata consistency for the older account is still authenticated. All earlier code versions, seals, attempts and failures are preserved under `peers/VERIFIER/`.

The four historical placeholder extracts remain in the frozen packet. Correct mathematical matrices are supplied under `supplemental_sources/recovered_native_results/`, with raw original hashes. This is a post-verification custody correction. `scripts/recover_native_results.py` reproduces that extraction when the intact prior private capsule is available; the engine-free scientific replay above does not require it.

The sibling private capsule archive and `CAPSULE_DELIVERY.json` preserve every input, raw recovered return and generated file, with file-by-file SHA256 readback and originals retained. No engine, Duck service, network, old learner code or original project path is needed for scientific replay. Director approval and publication are separate.

Next: use the theorem with its stated hypotheses in the unfitted physical receiving/reference assignment.
