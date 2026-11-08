#!/usr/bin/env python3
"""Independent host verifier. Python standard library; rational arithmetic only.

This file was authored for the frozen 02_independent_verification case. It reads
raw source operands and scalar premises, never a prior executable or result
implementation. --out must be a directory that does not exist.
"""
from __future__ import annotations

import argparse
import datetime as dt
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import sys
import time


def load(base, rel):
    return json.loads((base / rel).read_text())


def matrix(a):
    return [[Q(x) for x in row] for row in a]


def zeros(n, m):
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def ident(n):
    a = zeros(n, n)
    for i in range(n):
        a[i][i] = Q(1)
    return a


def transpose(a):
    return list(map(list, zip(*a)))


def scale(c, a):
    return [[c * x for x in row] for row in a]


def add(*terms):
    return [[sum(xs, Q(0)) for xs in zip(*rows)] for rows in zip(*terms)]


def mul(a, b):
    c = zeros(len(a), len(b[0]))
    sparse_b = [[(j, x) for j, x in enumerate(row) if x] for row in b]
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in sparse_b[k]:
                    c[i][j] += x * y
    return c


def gram(a, b=None):
    return mul(transpose(a), a if b is None else b)


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Q(0))


def rank(a):
    a = [row[:] for row in a]
    i = 0
    for j in range(len(a[0])):
        pivot = next((k for k in range(i, len(a)) if a[k][j]), None)
        if pivot is None:
            continue
        a[i], a[pivot] = a[pivot], a[i]
        d = a[i][j]
        a[i] = [x / d for x in a[i]]
        for k in range(i + 1, len(a)):
            d = a[k][j]
            if d:
                a[k] = [x - d * y for x, y in zip(a[k], a[i])]
        i += 1
        if i == len(a):
            break
    return i


def charpoly(a):
    """Faddeev-LeVerrier, returned in ascending coefficient order."""
    n = len(a)
    b = ident(n)
    descending = [Q(1)]
    for k in range(1, n + 1):
        ab = mul(a, b)
        c = -trace(ab) / k
        descending.append(c)
        b = add(ab, scale(c, ident(n)))
    assert not any(x for row in b for x in row)
    return descending[::-1]


def trim(p):
    p = p[:]
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def peval(p, x):
    y = Q(0)
    for c in reversed(p):
        y = y * x + c
    return y


def rem(p, q):
    p = trim(p)
    while len(p) >= len(q) and any(p):
        k = len(p) - len(q)
        c = p[-1] / q[-1]
        for i, x in enumerate(q):
            p[k + i] -= c * x
        p = trim(p)
    return p


def sturm(p):
    s = [trim(p), trim([i * p[i] for i in range(1, len(p))])]
    while len(s[-1]) > 1:
        s.append([-x for x in rem(s[-2], s[-1])])
    return s


def variations(s, x):
    signs = [1 if v > 0 else -1 for p in s if (v := peval(p, x))]
    return sum(x != y for x, y in zip(signs, signs[1:]))


def pair_embed(a, slots):
    """Literal n=a+4b+16c order; preserve the spectator coordinate."""
    out = zeros(64, 64)
    for n in range(64):
        ns = [n % 4, (n // 4) % 4, n // 16]
        r = ns[slots[0]] + 4 * ns[slots[1]]
        for s in range(16):
            if a[r][s]:
                ms = ns[:]
                ms[slots[0]], ms[slots[1]] = s % 4, s // 4
                m = ms[0] + 4 * ms[1] + 16 * ms[2]
                out[n][m] = a[r][s]
    return out


def swap(slots):
    a = zeros(64, 64)
    for n in range(64):
        xs = [n % 4, (n // 4) % 4, n // 16]
        xs[slots[0]], xs[slots[1]] = xs[slots[1]], xs[slots[0]]
        a[n][xs[0] + 4 * xs[1] + 16 * xs[2]] = Q(1)
    return a


def log_enclosure(x, terms=192):
    """Exact atanh series, binary range reduction, explicit positive tail."""
    assert x >= 1
    k = 0
    while x >= 2:
        x /= 2
        k += 1

    def inner(y):
        t = (y - 1) / (y + 1)
        power = t
        value = Q(0)
        for j in range(terms):
            value += 2 * power / (2 * j + 1)
            power *= t * t
        tail = 2 * power / ((2 * terms + 1) * (1 - t * t))
        return value, value + tail

    lo, hi = inner(x)
    l2, u2 = inner(Q(2))
    return lo + k * l2, hi + k * u2


def scalar_mass_enclosure(m):
    x = 2 * m
    l, u = log_enclosure(x)
    c = Q(91, 4) + Q(1, 1350)
    rest = -3 / x**2 - Q(5, 2) / x**3 - Q(3, 2) / x**4 - Q(9, 20) / x**5
    return Q(5, 6) * ((l + c) / x + rest), Q(5, 6) * ((u + c) / x + rest)


def placement(r, e):
    xs = [1 / (1 + 4 * k * r) for k in range(4)]
    s1, s2, s3 = (sum((x**j for x in xs), Q(0)) for j in (1, 2, 3))
    d = e * s1 / 4
    return {'r': r, 'delta': d, 'tau': r * d, 'p': s1**2 / (4 * s2),
            'S1': s1, 'S2': s2, 'S3': s3}


def gap(r, e, a, b):
    z = placement(r, e)
    return a + b * (1 - z['p']) - z['delta']


def isolate_gap(e, a, b):
    lo, hi = Q(0), Q(1)
    assert gap(lo, e, a, b) < 0
    while gap(hi, e, a, b) <= 0:
        hi *= 2
    for _ in range(112):
        mid = (lo + hi) / 2
        if gap(mid, e, a, b) < 0:
            lo = mid
        else:
            hi = mid
    return {'r_lower': lo, 'r_upper': hi,
            'tau_lower': placement(lo, e)['tau'],
            'tau_upper': placement(hi, e)['tau'],
            'gap_at_lower': gap(lo, e, a, b),
            'gap_at_upper': gap(hi, e, a, b)}


def ceiling_witness(tau, e, a, b):
    """Upper bracket r(tau); monotonicity gives gap(tau)<=gap(r_upper)."""
    lo, hi = Q(0), Q(1)
    while placement(hi, e)['tau'] < tau:
        hi *= 2
    for _ in range(112):
        mid = (lo + hi) / 2
        if placement(mid, e)['tau'] < tau:
            lo = mid
        else:
            hi = mid
    return {'tau': tau, 'r_lower': lo, 'r_upper': hi,
            'tau_at_lower': placement(lo, e)['tau'],
            'tau_at_upper': placement(hi, e)['tau'],
            'gap_upper': gap(hi, e, a, b)}


def serial(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def run(case):
    checks = []

    def check(name, truth, evidence=None):
        checks.append({'id': name, 'passed': bool(truth), 'evidence': evidence})
        if not truth:
            raise AssertionError(name)

    freeze = load(case, 'FREEZE.json')
    custody = []
    for rel, expected in freeze['files'].items():
        actual = hashlib.sha256((case / rel).read_bytes()).hexdigest()
        check('hash:' + rel, actual == expected)
        custody.append({'path': rel, 'sha256': actual})

    trial = load(case, 'sources/TRIAL_FAMILY.json')
    claim = load(case, 'CLAIM.json')
    e, b, mu0 = map(Q, [trial['epsilon'], trial['b_upper'], trial['mu0']])
    delta0, gamma = 3 * e, Q(trial['gamma_gate'])
    check('frozen_parameters', (e, b, mu0) == (Q(1, 573049), Q(5, 72), Q(1, 4)))
    check('original_trial_gap', Q(trial['original_trial_gap']) == delta0)
    check('zero_changed_ledger', trial['remaining_changed_signed_ledger'] == '0')

    # Only data.operators is consumed; native program and output are ignored.
    op = load(case, 'sources/light/COLOUR_64_CONSTRUCTION_PAYLOAD.json')['data']['operators']
    raw_pair = load(case, 'sources/light/COMPLETE_DC_PAIR.json')
    d16, r16, u = (matrix(op[k]) for k in ['D16', 'R16', 'U'])
    check('literal_D16', d16 == matrix(raw_pair['D']))
    check('literal_R16', r16 == matrix(raw_pair['C_over_i']))
    check('source_symmetry', transpose(d16) == d16 and transpose(r16) == scale(-1, r16))
    check('source_vacuum_metric', gram(u) == scale(6, ident(4)))
    s12, s23, s13 = (swap(s) for s in [(0, 1), (1, 2), (0, 2)])
    i64 = ident(64)
    check('pair_projector_owns_swap',
          pair_embed(add(ident(16), scale(-2, matrix(op['Pa16']))), (0, 1)) == s12)
    for name, s in [('12', s12), ('23', s23), ('13', s13)]:
        check('swap_involution_' + name, mul(s, s) == i64 and transpose(s) == s)
        positive = add(i64, s)
        check('positive_swap_square_' + name, mul(positive, positive) == scale(2, positive))
        check('floor_frame_' + name, mul(s, u) == scale(-1, u))
    hx = add(s12, s23, s13)
    d12, d23 = (pair_embed(d16, s) for s in [(0, 1), (1, 2)])
    r12, r23 = (pair_embed(r16, s) for s in [(0, 1), (1, 2)])
    x12, x23 = mul(d12, u), mul(d23, u)
    check('helicity_images_12', mul(r12, u) == x12)
    check('helicity_images_23', mul(r23, u) == x23)
    for name, x in [('12', x12), ('23', x23)]:
        check('actual_old_gap_' + name, mul(hx, x) == zeros(64, 4))
    g4 = scale(Q(1, 3), gram(x12))
    source_packet = load(case, 'sources/GEN4/volii_quantum_motion_join1_20261016/source/SOURCE_PACKET.json')
    check('original_vacuum_frame', matrix(source_packet['U']) == u)
    check('actual_G4', g4 == matrix(source_packet['G4']))
    check('equal_self_drive', gram(x12) == gram(x23))
    check('signed_contact_drive', scale(Q(1, 6), gram(x12, x23)) == scale(Q(-1, 4), g4))
    gc = add(mul(d12, d12), scale(-1, mul(r12, r12)))
    gi = add(mul(d23, d23), scale(-1, mul(r23, r23)))
    gt = add(gc, gi)
    check('crossing_vacuum_gram', scale(Q(1, 6), gram(u, mul(gc, u))) == g4)
    check('internal_vacuum_gram', scale(Q(1, 6), gram(u, mul(gi, u))) == g4)
    tr = trace(gt)
    check('full_source_trace', tr == Q(trial['Trace_Gsep']))
    check('positive_gram_construction',
          gc == add(gram(d12), gram(r12)) and gi == add(gram(d23), gram(r23)))
    # Operator promotion equality is affine in p, so two endpoints prove it.
    for p in [Q(0), Q(1)]:
        lhs = add(hx, scale(3, i64), scale(-1, add(i64, s23)), scale(-p, add(i64, s12)))
        rhs = add(scale(1-p, add(i64, s12)), add(i64, s13))
        check('full_source_promotion_endpoint_' + str(p), lhs == rhs)

    gpoly = charpoly(g4)
    sequence = sturm(gpoly)
    eigen_checks = []
    for row in trial['rows'][:4]:
        l, h = map(Q, row['g_interval'])
        count = variations(sequence, l) - variations(sequence, h)
        check('raw_G4_lane_' + str(row['lane']), l > 0 and h > l and count == 1)
        eigen_checks.append({'lane': row['lane'], 'lower': l, 'upper': h, 'root_count': count})
    ordered = sorted(eigen_checks, key=lambda x: x['lower'])
    check('all_four_lanes_disjoint', all(a['upper'] < z['lower'] for a, z in zip(ordered, ordered[1:])))

    raw = load(case, 'sources/light/HE3_INDEPENDENT_FRAGMENTS.json')
    h, j = matrix(raw['full_source_H']), matrix(raw['connected_receiving_isometry'])
    tuples = [tuple(x) for x in raw['coordinate_tuples']]
    check('placement_dimensions', len(h) == 192 and len(j) == 192 and len(j[0]) == 48)
    check('placement_injection', gram(j) == ident(48))
    for n, (a, bp, c) in enumerate(tuples):
        for m, (aa, bb, cc) in enumerate(tuples):
            expected = Q(18) if n == m else Q(-2) if bp == bb and c == cc and (a ^ aa) in (1, 2, 4) else Q(0)
            if h[n][m] != expected:
                check('literal_full_cube_rule', False, [n, m])
    check('literal_full_cube_rule', True)
    check('all_independent_cell_addresses', len(set(tuples)) == 192)
    hj = mul(h, j)
    compressed = mul(transpose(j), hj)
    check('connected_first_moment', compressed == scale(18, ident(48)))
    leak = add(hj, scale(-1, mul(j, compressed)))
    leakgram = gram(leak)
    check('nonzero_full_placement_leakage', rank(leak) == 48)
    block_records = []
    for bp, c in sorted(set((b0, c0) for _, b0, c0 in tuples)):
        inds = [n for n, (_, b0, c0) in enumerate(tuples) if (b0, c0) == (bp, c)]
        visible = [(n, col) for n in inds for col, v in enumerate(j[n]) if v]
        check('two_receiving_positions_' + str((bp,c)), len(visible) == 2)
        (n1, c1), (n2, c2) = visible
        a1, a2 = tuples[n1][0], tuples[n2][0]
        check('receiving_distance_two_' + str((bp,c)), (a1 ^ a2).bit_count() == 2)
        check('actual_complement_moment_' + str((bp,c)),
              [[leakgram[a][z] for z in (c1,c2)] for a in (c1,c2)] == matrix([[12,8],[8,12]]))
        plus, minus = [Q(0)]*4, [Q(0)]*4
        for w in range(8):
            f1 = (-1)**((w & a1).bit_count())
            f2 = (-1)**((w & a2).bit_count())
            plus[w.bit_count()] += Q((f1 + f2)**2, 16)
            minus[w.bit_count()] += Q((f1 - f2)**2, 16)
        check('full_Walsh_receiving_weights_' + str((bp,c)),
              plus == [Q(1,4)]*4 and minus == [Q(0),Q(1,2),Q(1,2),Q(0)])
        block_records.append({'pair':[bp,c], 'visible_singletons':[a1,a2], 'plus_weights':plus, 'minus_weights':minus})

    inter = load(case, 'sources/GEN4/volii_dressed_reference1_20261016/joint/INTERFACE.json')
    chi = Q(inter['chi_upper'])
    check('gate_scalar_range', 0 < chi < 1)
    check('unchanged_gate_probe', Q(inter['control']['gamma']) == gamma)
    check('unchanged_retarded_geometry', inter['control']['d_mean'] == '0' and inter['control']['ell'] == '1')
    masses = {}
    for ms in trial['masses']:
        m = Q(ms)
        lo, hi = scalar_mass_enclosure(m)
        given = Q(next(x for x in trial['rows'] if x['mR']==ms)['mass_majorant_upper'])
        check('mass_full_head_tail_' + ms, 0 < hi <= given)
        masses[ms] = {'rederived_majorant_lower':lo, 'rederived_majorant_upper':hi,
                       'inherited_upper':given, 'inherited_upper_minus_rederived_upper':given-hi}

    rows = []
    for src in trial['rows']:
        m, gL, gU = Q(src['mR']), Q(src['g_interval'][0]), Q(src['g_interval'][1])
        mass = Q(src['mass_majorant_upper'])
        cross = Q(src['actual_Fcross_lower'])
        kap = 2*delta0*b - cross
        check('retarded_kernel_derived_' + str(src['row']), kap == Q(src['paid_kernel_upper']) and 0 < kap < mu0)
        check('mass_row_custody_' + str(src['row']), mass == masses[src['mR']]['inherited_upper'])
        check('same_retarded_lower_' + str(src['row']), cross == Q(inter['actual_Fcross_lower']))
        kinetic = Q(3,4)/m
        components = {
            'packet_kinetic':kinetic,
            'dressed_packet_kinetic':3*e**2*b*kinetic*gU,
            'signed_paid_kernel':e**2*kap*gU,
            'massive_recoil':3*e**2*mass*gU,
            'full_source_one_boson_CT':6*e**4*mu0*tr*b*gU,
            'normal_vacuum_gate':4*gamma*chi,
            'dressed_correlated_gate':Q(45,2)*gamma*e**2*b*gU,
        }
        a = sum(components.values(), Q(0))
        bpay = e**2*gU*(mu0-kap)
        check('all_complete_coefficients_positive_' + str(src['row']), all(v>0 for v in components.values()) and bpay>0)
        dmax = 1+3*e**2*b*gU
        fbar = 3*e**2*delta0**2*Q(1,42)*gU + 6*e**4*mu0*tr*b*gU
        cbar = e**2*mu0*gU*(1+3*e**2*b*tr)
        clower = e**2*mu0*gL/dmax
        record = {'row':src['row'], 'mR':src['mR'], 'lane':src['lane'],
                  'g_lower':gL, 'g_upper':gU, 'components':components, 'A':a, 'B':bpay,
                  'D_min':Q(1), 'D_max':dmax, 'F_full_upper':fbar,
                  'C_cross_lower':clower, 'C_cross_upper':cbar,
                  'gap_at_r0':a-e, 'gap_at_r_infinity':a+Q(3,4)*bpay-e/4,
                  'positive_gate_gap_lower':a, 'changed_paid_epsilon_gap_lower':a}
        if src['mR'] == '1000000':
            root = isolate_gap(e, a, bpay)
            record['unique_zero'] = root
            ceil = Q(next(x for x in claim['intervals'] if x['lane']==src['lane'])['tau_ceiling'])
            witness = ceiling_witness(ceil, e, a, bpay)
            check('full_claim_interval_' + str(src['lane']), witness['gap_upper'] < 0 and ceil < root['tau_lower'])
            record['claim_ceiling_witness'] = witness
            beyond = placement(Q(1), e)
            beyond_gap = gap(Q(1), e, a, bpay)
            check('beyond_sufficient_interval_' + str(src['lane']), beyond_gap > 0 and beyond['tau'] > root['tau_upper'])
            record['beyond_control'] = {'point':beyond,'gap':beyond_gap, 'classification':'NONCERTIFYING_UPPER'}
            record['classification'] = 'CERTIFIES_CLAIM_INTERVAL'
        else:
            check('lighter_noncertifying_' + str(src['row']), a-e > 0)
            record['classification'] = 'NONCERTIFYING_UPPER_ALL_POSITIVE_TAU'
        p = placement(Q(1), e)['p']
        record['omitted_variance_lower_at_r1'] = p*(1-p)*clower
        check('strict_actual_variance_' + str(src['row']), record['omitted_variance_lower_at_r1'] > 0)
        rows.append(record)

    # Breaking controls use actual source defects or exact counterexamples.
    flipped = scale(Q(-1,6), gram(x12,x23))
    old_signed = scale(Q(-1,4), g4)
    sign_defect = add(flipped, scale(-1,old_signed))
    check('flip_signed_contact_gram_control', sign_defect == scale(Q(1,2),g4) and trace(sign_defect)>0)
    # Chi_aux=(|0>+epsilon|1>)/sqrt(1+epsilon^2); numerator is exact.
    dactual, dauxmax = 1+e**2, 1+2*e**2
    wrong_pos, good_neg, wrong_neg = dactual/dauxmax, -dactual/dauxmax, -dactual
    check('wrong_positive_norm_endpoint_control', wrong_pos < 1)
    check('negative_norm_endpoint_control', wrong_neg < -1 < good_neg)
    # Coefficient identity: projector square p vs scalar square p^2.
    p = placement(Q(1),e)['p']
    check('projection_identity_cross_coefficient', p-p*p == p*(1-p))
    controls = {
        'drop_incidence_variance':{'classification':'FAIL_IDENTITY','r':Q(1), 'p':p,
           'actual_positive_witnesses':[{'row':x['row'],'omitted_term_lower':x['omitted_variance_lower_at_r1']} for x in rows]},
        'positive_gate_baseline':{'classification':'NONCERTIFYING_UPPER_ALL_ROWS', 'identity_baseline':'epsilon*p',
           'proof':'gap=A+B*(1-p)+(epsilon*p-delta)>=A>0'},
        'truncate_placement':{'classification':'FAIL_INVARIANCE','full_leakage_rank':rank(leak),
           'leakage_Gram_diagonal':list(dict.fromkeys(leakgram[i][i] for i in range(48)))),
           'one_pair_leakage_Gram':[[12,8],[8,12]]},
        'flip_signed_contact_gram':{'classification':'FAIL_SOURCE_HYPOTHESIS', 'defect':sign_defect,
           'trace_defect':trace(sign_defect),'new_contact_drive_gram':flipped},
        'wrong_norm_endpoint':{'classification':'FAIL_NORMALIZED_BOUND','auxiliary_trial':'(|0>+epsilon|1>)/sqrt(1+epsilon^2)',
           'actual_D':dactual, 'D_interval':[Q(1),dauxmax], 'positive_operator':'I', 'actual_expectation':Q(1),
           'positive_numerator_upper':dactual, 'wrong_positive_upper':wrong_pos,
           'negative_operator':'-I', 'actual_negative_expectation':Q(-1),
           'valid_negative_upper':good_neg, 'wrong_negative_upper':wrong_neg},
        'changed_paid_ledger':{'classification':'NONCERTIFYING_UPPER_ALL_ROWS','added_payment':e,
           'proof':'gap_changed=A+B*(1-p)+epsilon-delta>=A>0'},
        'beyond_sufficient_interval':{'classification':'NONCERTIFYING_UPPER_ALL_FOUR_HEAVY_LANES','r':Q(1)},
    }
    return {'status':'PASS', 'verdict':'HELD', 'method':'new standard-library host exact arithmetic and analytic proof; inherited continuum/gate premises explicit',
            'independence':'I1 same inherited model, separate code; not external verification',
            'checks':checks, 'input_hashes':custody, 'raw_G4':g4, 'raw_G4_charpoly_ascending':gpoly,
            'full_source_TraceGsep':tr, 'eigenlane_isolations':eigen_checks, 'placement_blocks':block_records,
            'mass_audit':masses, 'rows':rows, 'breaking_controls':controls,
            'inherited_premises':['sharp-profile inverse moments and full TT mode Gram',
                'Gaussian-averaged full retarded cross lower at mean0/ell1/Delta3epsilon',
                'normal-EDGE gate overlap and complete correlated gate bound'],
            'boundary':'Conditional mathematical sufficient upper for the frozen recipient and zero changed ledger; no actual-energy lower from noncertifying rows and no physical tau/species/ruler assignment.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--case',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args = ap.parse_args()
    # Fail before any arithmetic or write if this is not a fresh destination.
    args.out.mkdir(parents=False,exist_ok=False)
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    mono = time.monotonic()
    record = {'started_utc':start,'script':str(Path(__file__).resolve()),
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'argv':sys.argv,'python':sys.version,'platform':platform.platform(),'case':str(args.case.resolve())}
    try:
        result = run(args.case)
        (args.out/'RESULTS.json').write_text(json.dumps(serial(result),indent=2)+'\n')
        record['status'] = 'PASS'
        print('PASS: full proof operands, twelve complete accounts, four open intervals, and seven breaking controls.')
    except BaseException as exc:
        record['status'] = 'FAILED'
        record['exception'] = repr(exc)
        (args.out/'FAILURE.json').write_text(json.dumps(record,indent=2)+'\n')
        raise
    finally:
        record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        record['elapsed_seconds'] = time.monotonic()-mono
        (args.out/'EXECUTION.json').write_text(json.dumps(record,indent=2)+'\n')


if __name__ == '__main__':
    main()
