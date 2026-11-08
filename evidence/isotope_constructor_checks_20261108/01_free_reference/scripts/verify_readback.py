#!/usr/bin/env python3
"""Audit fresh replay equality, script seals and case-specific exact witnesses."""
import argparse
import datetime as dt
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_time(value):
    return dt.datetime.fromisoformat(value.replace('Z','+00:00'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',required=True,type=Path)
    parser.add_argument('--fresh',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    case=args.case.resolve();peer=case/'peers/VERIFIER'
    assert not args.out.exists(),'Use a fresh output file.'
    fresh=read(args.fresh/'RESULTS.json')
    assert fresh['verdict']=='HELD'
    freeze=read(case/'FREEZE.json')
    assert all(sha(case/rel)==h for rel,h in freeze['files'].items())
    controls={c['id'] for c in read(case/'PREDICTIONS.json')['breaking_controls']}
    if case.name=='01_free_reference':
        assert (args.fresh/'RESULTS.json').read_bytes()==(peer/'RESULTS.json').read_bytes()
        checks=read(args.fresh/'CHECKS.json')
        assert len(checks)==247 and all(c['passed'] for c in checks)
        assert fresh['all_checks_passed'] and fresh['check_count']==247
        assert {c['id'] for c in fresh['breaking_controls']}==controls
        assert all(c['rejected_mutation'] for c in fresh['breaking_controls'])
        assert fresh['free_pair']['floor']==0 and fresh['adjacent']['dimension']==24
        assert fresh['adjacent']['true_drift_rank']==18
        assert fresh['cyclic']['dimensions']==[24,42,46,47,47]
        assert fresh['cyclic']['dynamically_hidden_dimensions']==23 and fresh['cyclic']['dark_dimension']==17
        assert Q(fresh['resolvent']['diagonal_defect'])==Q(3064,116025)>0
        start=read(args.fresh/'START.json');end=read(args.fresh/'COMPLETE.json')
        assert start['script_sha256']==sha(peer/'replay.py')==end['script_sha256']
        assert parse_time(start['registration_sealed_utc'])<parse_time(start['started_utc'])
        for attempt in ['attempt_001','attempt_002']:
            folder=peer/'attempts'/attempt
            registration=read(folder/'EXECUTION_PREREGISTRATION.json')
            assert registration['script_sha256']==sha(folder/'replay.py')
            run_start=read(folder/'output/START.json')
            assert parse_time(registration['sealed_utc'])<parse_time(run_start['started_utc'])
        seal=read(peer/'SEAL.json')
        assert sha(peer/'replay.py')==seal['script_sha256']
        for rel,wanted in seal['files'].items():
            assert sha(peer/rel)==(wanted if isinstance(wanted,str) else wanted['sha256']),rel
        assert (peer/'SCOPE_CLARIFICATION.md').is_file()
        details=dict(free_pair_floor=0,adjacent_compression='12I24',preparation_expectation='12*tau',
                     omitted_complement=40,drift_rank=18,cyclic_dimensions=fresh['cyclic']['dimensions'],
                     hidden_dimension=23,dark_dimension=17,resolvent_diagonal_defect=fresh['resolvent']['diagonal_defect'],
                     nested_dimensions=[512,192,48],primary_cyclic_dimension=fresh['primary']['cyclic_dimension'],
                     primary_floor=12,connected_expectation=18,
                     documentation_correction='Append-only clarification: the inherited relaxed-field He3 theorem uses primary192; shared144 is separate. Frozen geometric claim and checks unchanged.')
        start_time=start['started_utc'];finish_time=end['completed_utc'];count=247
    elif case.name=='02_shared_field_covariance':
        original=read(peer/'attempts/run_v002/RESULTS.json')
        assert {k:v for k,v in fresh.items() if k!='completed_utc'}=={k:v for k,v in original.items() if k!='completed_utc'}
        checks=read(args.fresh/'CHECKS.json')
        assert fresh['checks_total']==fresh['checks_passed']==108
        assert len(checks)==108 and all(c['passed'] for c in checks)
        assert set(fresh['registered_controls'])==controls
        assert all(c['witness_nonzero'] for c in fresh['registered_controls'].values())
        assert Q(fresh['anticorrelated_e0'])==3*Q(fresh['correlated_e0'])>0
        assert Q(fresh['entangled_defect'])==Q(-1600,3)
        assert Q(fresh['complex_order_e0_defect'])==Q(-461296,3)
        assert all(Q(v)>0 for v in fresh['M_leading_principal_minors'])
        for filename in ['CHECKS.json','PLACEMENT_OPERANDS.json','COLOUR_OPERANDS.json','CONTROLS.json','FIELD_COEFFICIENTS.json','ENTANGLED_CONTROL.json']:
            assert read(args.fresh/filename)==read(peer/'attempts/run_v002'/filename),filename
        registration=read(peer/'EXECUTION_PREREGISTRATION_V002.json')
        assert registration['script_sha256']==sha(peer/'replay.py')==fresh['script_sha256']
        start=read(args.fresh/'RUN_START.json');end=read(args.fresh/'RUN_STATUS.json')
        assert start['script_sha256']==sha(peer/'replay.py')
        assert parse_time(registration['sealed_utc'])<parse_time(start['started_utc'])
        for version in ['001','002']:
            registration=read(peer/f'EXECUTION_PREREGISTRATION_V{version}.json')
            run_start=read(peer/f'attempts/run_v{version}/RUN_START.json')
            assert registration['script_sha256']==run_start['script_sha256']
            assert parse_time(registration['sealed_utc'])<parse_time(run_start['started_utc'])
        seal=read(peer/'FINAL_SEAL.json')
        for rel,wanted in seal['files'].items():
            assert sha(peer/rel)==(wanted if isinstance(wanted,str) else wanted['sha256']),rel
        details=dict(M=fresh['M'],correlated_coefficient='M/4',anticorrelated_coefficient='3M/4',
                     ratio_scope=fresh['factor_three_scope'],entangled_defect=fresh['entangled_defect'],
                     complex_order_imaginary_defect=fresh['complex_order_e0_defect'],
                     strengthened_scalar_D_profile_ratio_bound=['1/3','3'],
                     complete_physical_field_payment=False)
        start_time=start['started_utc'];finish_time=end['finished_utc'];count=108
    else:
        raise ValueError('Unexpected case')
    receipt=dict(status='PASS',verdict='HELD',case=case.name,check_count=count,controls=len(controls),
                 exact_mathematical_readback_matches=True,fixed_input_count=len(freeze['files']),
                 script_sha256=sha(peer/'replay.py'),fresh_result_sha256=sha(args.fresh/'RESULTS.json'),
                 execution_seals_precede_runs=True,original_deliverable_seal_unchanged=True,
                 replay_elapsed_seconds=(parse_time(finish_time)-parse_time(start_time)).total_seconds(),
                 details=details,independence='I1: same inherited model; separate proof/code; no outside verification',
                 reproducibility='R2: new exact finite results and conditional proof replay from the case with standard Python',
                 checked_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x') as handle:
        json.dump(receipt,handle,indent=2);handle.write('\n')
    print(json.dumps({k:receipt[k] for k in ['status','case','check_count','controls','replay_elapsed_seconds']},indent=2))


if __name__=='__main__':
    main()
