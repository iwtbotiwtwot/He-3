#!/usr/bin/env python3
"""Recover mathematical result fields; preserve sealed placeholder extracts."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True, type=Path)
    parser.add_argument('--prior-capsule', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    assert not args.out.exists(), 'Retain every earlier extraction.'
    seal = json.loads((args.prior_capsule / 'PREPARATION_SEAL.json').read_text())
    source_root = args.prior_capsule / 'sources_raw/GEN4/duck_gen6_local/runs'
    extracted = []
    records = []
    for original in sorted(source_root.rglob('*.json')):
        relative = str(original.relative_to(args.prior_capsule))
        assert sha(original) == seal['files'][relative], original
        raw = json.loads(original.read_text())
        returned = raw['returned']
        assert isinstance(returned, dict) and isinstance(returned['matrix'], (list, dict))
        old_relative = 'sources/' + str(original.relative_to(args.prior_capsule / 'sources_raw'))
        old = args.case / old_relative
        old_payload = json.loads(old.read_text())
        assert old_payload == returned['output'] == 'Output'
        # ordered_program, native_payload and engine construction remain private.
        mathematical = {key: returned[key] for key in ['field', 'matrix', 'rank'] if key in returned}
        extracted.append((original.name, mathematical))
        records.append(dict(raw_original=str(original), raw_sha256=sha(original),
                            preparation_seal_sha256=sha(args.prior_capsule / 'PREPARATION_SEAL.json'),
                            prior_frozen_extract=old_relative, prior_frozen_sha256=sha(old),
                            prior_extract_type=type(old_payload).__name__,
                            cause='The old extractor descended into the output label after reaching the returned result dictionary.',
                            corrected_file=original.name,
                            extraction='Verbatim returned.field/matrix/rank values; no numerical changes or execution.'))
    assert len(records) == 4
    args.out.mkdir(parents=True, exist_ok=False)
    for filename, value in extracted:
        (args.out / filename).write_text(json.dumps(value, indent=2) + '\n')
    for item in records:
        item['corrected_sha256'] = sha(args.out / item['corrected_file'])
    receipt = dict(status='PASS', recovered_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   records=records, files_recovered=4,
                   timing='Post-verifier custody supplement; not a scientific input to the sealed independent computation.',
                   scientific_effect='None. Shared theorem and HELD verdict are unchanged; moment and complete gate inequalities remain explicit inherited premises.',
                   original_frozen_packets_unchanged=True)
    (args.out / 'EXTRACTION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', files_recovered=4, output=str(args.out)), indent=2))


if __name__ == '__main__':
    main()
