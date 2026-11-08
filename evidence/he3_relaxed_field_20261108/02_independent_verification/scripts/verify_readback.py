#!/usr/bin/env python3
"""Check a fresh independent replay against retained evidence, without an engine."""
import argparse
import datetime
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True, type=Path)
    parser.add_argument('--replay', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    assert not args.out.exists(), 'Choose a fresh output file.'
    case = args.case.resolve()
    peer = case / 'peers/VERIFIER'
    result = read(args.replay / 'RESULTS.json')
    assert (args.replay / 'RESULTS.json').read_bytes() == (peer / 'RESULTS.json').read_bytes()
    assert result['status'] == 'PASS' and result['verdict'] == 'HELD'
    assert len(result['checks']) == 285 and all(c['passed'] for c in result['checks'])
    assert len(result['rows']) == 12
    assert len(result['breaking_controls']) == 7
    predictions = read(case / 'PREDICTIONS.json')
    assert set(result['breaking_controls']) == {c['id'] for c in predictions['breaking_controls']}
    for version in [1, 2, 3]:
        registration = read(peer / f'EXECUTION_PREREGISTRATION_v{version}.json')
        assert registration['scripts']['replay.py'] == sha(peer / f'versions/replay_v{version}.py')
        launch = read(peer / f'runs/attempt{version}.launch.json')
        assert datetime.datetime.fromisoformat(registration['sealed_utc']) < datetime.datetime.fromisoformat(launch['started_utc'])
    assert sha(peer / 'replay.py') == sha(peer / 'versions/replay_v3.py')
    execution = read(args.replay / 'EXECUTION.json')
    assert execution['script_sha256'] == sha(peer / 'replay.py') and execution['status'] == 'PASS'
    rows = []
    for row in result['rows']:
        assert row['retarded_numerical_lower_required_for_certificate'] is False
        record = dict(row=row['row'], mR=row['mR'], lane=row['lane'], classification=row['classification'])
        if row['classification'] == 'CERTIFIES_CLAIM_INTERVAL':
            witness = row['claim_ceiling_witness']
            tau = Q(witness['tau'])
            assert Q(witness['tau_at_lower']) <= tau <= Q(witness['tau_at_upper'])
            assert Q(witness['gap_upper']) < 0
            assert tau < Q(row['unique_zero']['tau_lower'])
            record.update(tau_ceiling=str(tau), gap_upper=witness['gap_upper'], root_bracket=row['unique_zero'])
        else:
            assert Q(row['gap_at_r0']) > 0
        rows.append(record)
    for row in result['rows']:
        assert Q(row['positive_gate_gap_lower']) > 0
        assert Q(row['changed_paid_epsilon_gap_lower']) > 0
        assert Q(row['omitted_variance_lower_at_r1']) > 0
    payload = dict(status='PASS', verdict='HELD', same_result_bytes=True,
                   checks_passed=len(result['checks']), frozen_inputs=len(result['input_hashes']),
                   code_seals_before_every_execution=True, all_rows=rows,
                   breaking_controls=result['breaking_controls'],
                   primary_retarded_numerical_lower_required=False,
                   remaining_inherited_premises=['Sharp-profile inverse moments', 'Complete correlated normal-EDGE/localized-gate bound and overlap enclosure'],
                   source_and_mass_notes='Finite sources and full massive head/tail majorant independently reconstructed; universal spectral paid bound proved analytically.',
                   source_result_sha256=sha(peer / 'RESULTS.json'), fresh_result_sha256=sha(args.replay / 'RESULTS.json'),
                   replay_script_sha256=sha(peer / 'replay.py'),
                   independence='I1 same inherited model with separate code/proof; no external verification',
                   checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x') as handle:
        json.dump(payload, handle, indent=2)
        handle.write('\n')
    print(json.dumps(dict(status='PASS', verdict='HELD', checks_passed=285,
                         certified_rows=[r['row'] for r in rows if 'tau_ceiling' in r]), indent=2))


if __name__ == '__main__':
    main()
