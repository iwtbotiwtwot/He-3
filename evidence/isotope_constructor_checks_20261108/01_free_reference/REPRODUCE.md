# Engine-free replay

Tested with Python3.12 and its standard library only. Run from this case directory, preserving every earlier output:

```bash
isotope_case_dir="$PWD"
isotope_replay_dir=$(mktemp -d)
python3 -I -B peers/VERIFIER/replay.py preregister --case "$isotope_case_dir" --record "$isotope_replay_dir/EXECUTION_PREREGISTRATION.json"
python3 -I -B peers/VERIFIER/replay.py run --case "$isotope_case_dir" --registration "$isotope_replay_dir/EXECUTION_PREREGISTRATION.json" --out "$isotope_replay_dir/fresh"
python3 -I -B scripts/verify_readback.py --case "$isotope_case_dir" --fresh "$isotope_replay_dir/fresh" --out "$isotope_replay_dir/READBACK.json"
```

Expect verdict HELD and readback PASS. The readback checks the original script seals, authenticated source hashes, exact mathematical result/control equality and registered witnesses. Execution timestamps/paths differ by machine. Output paths must be new. The public case alone contains all scientific replay inputs; prior native recipes, private receipts and engine services are not required.

The full proof, hypothesis map, failed/corrected implementations, outputs and all registered controls are retained under peers/VERIFIER. Read every scope clarification with the original report. A finite coefficient/geometric replay does not select physical species, currents, profiles, tau, controller work or atomic endpoints.

The complete two-case private capsule is losslessly archived and hash-committed in CAPSULE_DELIVERY.json, including raw prior-native custody and original inputs. Every archived file was read and SHA256 checked; originals retained. Approval remains false. Next: use the actual theorem boundaries and controls in physical bridge/action construction.
