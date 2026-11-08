#!/usr/bin/env python3
"""Hash-only provenance check; never parse prior executable/program logic."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

VERIFIER = Path(__file__).resolve().parent.parent
CASE = Path('/home/lilhelper/SAM_Research_Overflow/Courtroom_II/campaigns/isotope_constructor_checks_20261108/02_shared_field_covariance')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

freeze = json.loads((CASE/'FREEZE.json').read_text())
custody = json.loads((CASE/'RESULTS/INPUT_CUSTODY.json').read_text())
fixed = []
for rel, expected in freeze['files'].items():
    got = sha(CASE/rel)
    fixed.append({'path':str(CASE/rel),'expected_sha256':expected,
                  'actual_sha256':got,'passed':got == expected})
snapshots = []
for entry in custody['files']:
    expected = entry.get('snapshot_sha256',entry.get('sha256'))
    if expected is None:
        raise ValueError('Custody snapshot has no authenticated expected hash')
    p = Path(entry['snapshot'])
    got = sha(p)
    snapshots.append({'path':str(p),'expected_sha256':expected,
                      'actual_sha256':got,'passed':got == expected,
                      'method':'hash bytes only; no prior program member parsed'})
result = {'checked_utc':datetime.now(timezone.utc).isoformat(),
          'FREEZE_sha256':sha(CASE/'FREEZE.json'),
          'fixed_file_count':len(fixed),'custody_snapshot_count':len(snapshots),
          'fixed_files':fixed,'custody_snapshots':snapshots,
          'all_passed':all(x['passed'] for x in fixed+snapshots)}
target = VERIFIER/'provenance/FINAL_INPUT_CUSTODY.json'
if target.exists():
    raise FileExistsError('Retain prior custody checks; select a new artifact instead')
target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ('fixed_file_count','custody_snapshot_count','all_passed')},sort_keys=True))
