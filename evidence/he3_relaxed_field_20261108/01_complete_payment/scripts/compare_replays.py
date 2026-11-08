#!/usr/bin/env python3
"""Post-blind comparison. Standard library only; never overwrites evidence."""
import argparse
from decimal import Decimal, ROUND_FLOOR, localcontext
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def downward_display(value):
    with localcontext() as context:
        context.prec = 6
        context.rounding = ROUND_FLOOR
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--a', type=Path, required=True)
    parser.add_argument('--b', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    case = args.case.resolve()
    args.a = args.a.resolve()
    args.b = args.b.resolve()
    assert not args.output.exists(), 'Choose a fresh comparison output.'
    a = read(args.a / 'RESULTS.json')
    b = read(args.b / 'RESULTS.json')
    assert a['rows'] == read(case / 'peers/A/RESULTS.json')['rows']
    assert b['rows'] == read(case / 'peers/B/RESULTS.json')['rows']
    source_a = read(args.a / 'SOURCE_REPLAY.json')
    source_b = read(args.b / 'SOURCE_OPERATORS.json')
    for key_a, key_b in [('G12', 'Gcross'), ('Gsep', 'Gtotal'), ('G4', 'vacuum_G4')]:
        assert source_a[key_a] == source_b[key_b]
    epsilon = Q(a['epsilon'])
    assert epsilon == Q(b['epsilon'])
    assert len(a['rows']) == len(b['rows']) == 12
    rows = []
    for ra, rb in zip(a['rows'], b['rows']):
        assert (ra['row'], str(ra['mR']), ra['lane']) == (rb['row'], rb['mR'], rb['lane'])
        assert Q(ra['A_complete_connected_upper']) == Q(rb['original_formula_paid_upper'])
        assert Q(rb['refined_complete_paid_upper']) <= Q(ra['A_complete_connected_upper'])
        assert Q(rb['full_field_bounds'][1]) <= Q(ra['F_full_interval'][1])
        assert Q(rb['cross_self_CT_bounds'][1]) <= Q(ra['C_cross_interval'][1])
        assert Q(ra['C_cross_interval'][0]) > 0 and Q(rb['cross_self_CT_bounds'][0]) > 0
        ac = ra['intrinsic']['status'] == 'CERTIFIES_CONDITIONAL_INTERVAL'
        bc = rb['intrinsic_interval']['status'] == 'FINITE_CERTIFYING_INTERVAL'
        assert ac == bc
        row = dict(row=ra['row'], mR=str(ra['mR']), lane=ra['lane'],
                   intrinsic_certifies_both=ac,
                   positive_gate_certifies_either=False)
        assert ra['positive_gate']['status'] == 'NONCERTIFYING_ALL_TAU'
        assert rb['positive_gate_interval']['status'] == 'NO_INTERVAL_FROM_THIS_UPPER'
        if ac:
            aa = list(map(Q, ra['intrinsic']['tau_star_bracket']))
            bb = list(map(Q, rb['intrinsic_interval']['tau_root_bracket']))
            assert bb[1] < aa[0], 'Distinct bounds must not be called equal endpoints.'
            # A uses r=4*tau/delta and B uses r=tau/delta.
            r = Q(rb['intrinsic_interval']['r_root_bracket'][0])
            weights = [Q(1) / (1 + 4 * k * r) for k in range(4)]
            s1 = sum(weights)
            s2 = sum(x*x for x in weights)
            delta = epsilon * s1 / 4
            probability = s1*s1 / (4*s2)
            tau = epsilon * r * s1 / 4
            assert tau == bb[0]
            gap_a = Q(ra['A_complete_connected_upper']) + Q(ra['B_quadratic_relaxation_upper'])*(1-probability)-delta
            gap_b = Q(rb['refined_complete_paid_upper']) + Q(rb['Q_extra'])*(1-probability)-delta
            assert gap_a < 0 and gap_b < 0
            display = downward_display(tau)
            assert Q(display) <= tau
            row.update(a_endpoint_bracket=list(map(str, aa)),
                       b_endpoint_bracket=list(map(str, bb)),
                       a_endpoint_display=ra['intrinsic']['tau_star_bracket_decimal'],
                       b_endpoint_display=rb['intrinsic_interval']['tau_ceiling_decimal'],
                       common_guaranteed_interval=dict(lower='0', upper=str(tau), exclusive=True),
                       common_conservative_ceiling_display=display,
                       exact_a_gap_at_common_ceiling=str(gap_a),
                       exact_b_gap_at_common_ceiling=str(gap_b))
        rows.append(row)
    assert [r['row'] for r in rows if r['intrinsic_certifies_both']] == [8, 9, 10, 11]
    output = dict(schema='CR2_POST_BLIND_COMPARISON_V1', status='PASS',
                  provenance='Post-window host comparison; no new learner, native run or trial.',
                  separate_code_same_model=True, independence='I1', reproducibility='R2',
                  scope='Conditional exact-rational replay of bounds from frozen supplied continuum enclosures; no external replay.',
                  rows=rows,
                  checks=['Fresh A and B rows equal the respective blind reference rows exactly.',
                          'Full-source matrices agree exactly.',
                          'Original paid account agrees exactly; B retains its sharper norm bound.',
                          'All mass/lane and positive-gate controls agree.',
                          'Both gap bounds are strictly negative at the common conservative endpoint.',
                          'Different endpoint bounds and parameter conventions remain explicit.'],
                  replay_inputs={str(p): digest(p) for p in
                                 [args.a/'RESULTS.json', args.b/'RESULTS.json',
                                  case/'peers/A/replay.py', case/'peers/B/replay.py']})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(output, handle, indent=2)
        handle.write('\n')
    print(json.dumps(dict(status='PASS', certifying_rows=[8,9,10,11],
                         common_ceilings=[r['common_conservative_ceiling_display'] for r in rows if r['intrinsic_certifies_both']]), indent=2))


if __name__ == '__main__':
    main()
