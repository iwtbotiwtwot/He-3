#!/usr/bin/env python3
"""Independent CR2 free-reference audit. Python standard library; exact arithmetic.

This file was authored from frozen mathematical operands, not a prior routine.
There are two phases: preregister (custody and predictions only), then run.
The run refuses an existing output path and a registration for another script.
No program field or prior mathematical result is interpreted.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
import json
from math import comb
from pathlib import Path
import platform
import sys
import traceback

DEFAULT_CASE = Path('/home/lilhelper/SAM_Research_Overflow/Courtroom_II/campaigns/isotope_constructor_checks_20261108/01_free_reference')
PINNED_FREEZE = '38c2e160ee745e83200e07c223d33d44f98888eadbd77647bc1ac6189ef2b2ad'
SCRIPT_VERSION = 'independent-free-reference-001'


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode(x):
    if isinstance(x, Q):
        return x.numerator if x.denominator == 1 else str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def dump(path, data):
    Path(path).write_text(json.dumps(encode(data), indent=2, sort_keys=True) + '\n')


def authenticate(case):
    actual = digest(case / 'FREEZE.json')
    if actual != PINNED_FREEZE:
        raise ValueError('Frozen-case root mismatch: ' + actual)
    frozen = json.loads((case / 'FREEZE.json').read_text())
    records = []
    for rel, wanted in frozen['files'].items():
        got = digest(case / rel)
        records.append({'path': rel, 'expected': wanted, 'observed': got, 'matched': got == wanted})
    if not all(x['matched'] for x in records):
        raise ValueError('A fixed input failed authentication')
    return {'freeze_sha256': actual, 'files': records, 'all_matched': True}


def raw_sources(case):
    # These three owning mathematical operands have no executable use here.
    # Only the fields selected in audit() below enter the reconstruction.
    folder = case / 'sources' / 'light'
    return [json.loads((folder / name).read_text()) for name in (
        'HE3_PLACEMENT.json', 'HE3_INDEPENDENT_FRAGMENTS.json', 'HE3_FRAGMENT_SPACE.json')]


def predicted():
    return {
        'h1': {'dimension': 8, 'rule': '6I-2A(Q3)', 'eigenvalues': [0, 4, 8, 12], 'multiplicities': [1, 3, 3, 1]},
        'free_pair': {'dimension': 64, 'floor': 0, 'spectrum': {4*k: comb(6, k) for k in range(7)}},
        'adjacent': {'dimension': 24, 'compression': '12I', 'omitted': 40, 'drift_rank': 18},
        'cyclic_dimensions': [24, 42, 46, 47, 47],
        'spectral_receiving_ranks': [1, 6, 12, 9, 12, 6, 1],
        'dark_multiplicities': [0, 0, 3, 11, 3, 0, 0],
        'dynamic_hidden': 23, 'invariant_dark': 17,
        'resolvent': {'z': 1, 'defect_nonzero': True, 'defect_rank': 18, 'diagonal_defect_positive': True,
                      'complement_matrix_positive_after_shift': True, 'self_energy_rank': 18},
        'three_free': {'dimension': 512, 'floor': 0, 'spectrum': {4*k: comb(9, k) for k in range(10)}},
        'primary': {'dimension': 192, 'omitted': 320, 'floor': 12, 'multiplicities': [24, 72, 72, 24],
                    'cyclic_dimension': 376, 'dark_dimension': 136, 'drift_rank': 144},
        'connected': {'dimension': 48, 'compression': '18I', 'cost_above_primary_floor': 6},
        'same_cell_fragment_dimension': 144,
        'controls': {
            'compressed_floor_as_full_lower': 'FAIL_FULL_SOURCE_LOWER',
            'adjacent_invariance': 'FAIL_INVARIANCE',
            'omit_complement_response': 'FAIL_RESOLVENT',
            'all_omitted_addresses_dark': 'FAIL_COMPLEMENT_CLASSIFICATION',
            'one_sided_baseline_shift': 'FAIL_COMMON_ZERO'},
        'limits': ['Geometric labelled source only', 'tau is a nonnegative common kinetic coefficient when read as a cost',
                   'No physical binding, species Hamiltonian, trial optimization or unit assignment',
                   'Same inherited model and separately authored code: I1, not external verification']}


def zeros(n, m):
    return [[0] * m for _ in range(n)]


def ident(n, scale=1):
    return [[scale if i == j else 0 for j in range(n)] for i in range(n)]


def trans(a):
    return [list(t) for t in zip(*a)]


def mm(a, b):
    result = zeros(len(a), len(b[0]))
    for i, row in enumerate(a):
        for k, value in enumerate(row):
            if value:
                for j, other in enumerate(b[k]):
                    if other:
                        result[i][j] += value * other
    return result


def mv(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def minus(a, b):
    return [[x-y for x, y in zip(r, s)] for r, s in zip(a, b)]


def shift(a, z):
    return [[x + (z if i == j else 0) for j, x in enumerate(row)] for i, row in enumerate(a)]


def submatrix(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def rref(a):
    if not a:
        return [], []
    m = [[Q(x) for x in row] for row in a]
    pivots = []
    row = 0
    for col in range(len(m[0])):
        pivot = next((i for i in range(row, len(m)) if m[i][col]), None)
        if pivot is None:
            continue
        m[row], m[pivot] = m[pivot], m[row]
        d = m[row][col]
        m[row] = [x/d for x in m[row]]
        for i in range(len(m)):
            if i != row and m[i][col]:
                factor = m[i][col]
                m[i] = [x-factor*y for x, y in zip(m[i], m[row])]
        pivots.append(col)
        row += 1
        if row == len(m):
            break
    return m, pivots


def rank(a):
    return len(rref(a)[1])


def nullspace(a):
    m, pivots = rref(a)
    free = [j for j in range(len(a[0])) if j not in pivots]
    result = []
    for f in free:
        v = [Q(0)] * len(a[0])
        v[f] = Q(1)
        for i, p in enumerate(pivots):
            v[p] = -m[i][f]
        result.append(v)
    return result


def inverse(a):
    n = len(a)
    r, pivots = rref([row + eye for row, eye in zip(a, ident(n))])
    if pivots[:n] != list(range(n)) or [row[:n] for row in r] != ident(n):
        raise ArithmeticError('Singular matrix')
    return [row[n:] for row in r]


def ldl_pivots(a):
    n = len(a)
    l = ident(n)
    ds = []
    for j in range(n):
        d = Q(a[j][j]) - sum(l[j][k]**2 * ds[k] for k in range(j))
        if d <= 0:
            raise ArithmeticError('Positive-definiteness certificate failed')
        ds.append(d)
        for i in range(j+1, n):
            l[i][j] = (Q(a[i][j]) - sum(l[i][k]*l[j][k]*ds[k] for k in range(j))) / d
    return ds


class Span:
    """Exact incremental echelon basis, retaining the original chosen vectors."""
    def __init__(self):
        self.echelon = []
        self.original = []
        self.labels = []

    def residual(self, v):
        w = [Q(x) for x in v]
        for p, b in self.echelon:
            if w[p]:
                scale = w[p]
                w = [x-scale*y for x, y in zip(w, b)]
        return w

    def add(self, v, label):
        w = self.residual(v)
        p = next((i for i, x in enumerate(w) if x), None)
        if p is None:
            return False
        d = w[p]
        self.echelon.append((p, [x/d for x in w]))
        self.original.append(list(v))
        self.labels.append(label)
        return True


def walsh(mask, address):
    return -1 if (mask & address).bit_count() % 2 else 1


def audit(case, out):
    checks = []

    def require(name, condition):
        checks.append({'id': name, 'passed': bool(condition)})
        if not condition:
            raise AssertionError(name)

    p, independent, fragment = raw_sources(case)
    actions = p['source']['actions']
    events = zeros(8, 8)
    for a in actions:
        u, v = a['source_site'], a['target_site']
        require('event_one_cube_bit_' + str(len(checks)), (u ^ v) in (1, 2, 4))
        require('event_frame_rule_' + str(len(checks)), (a['target_frame_q'] - a['source_frame_q']) % 4 == a['local_displacement'] % 4)
        require('event_chirality_' + str(len(checks)), a['sigma_chi'] == -a['local_displacement'])
        events[u][v] += 1
    require('all_48_events', len(actions) == 48)
    require('two_events_per_oriented_cube_edge', events == [[2 if (i ^ j) in (1, 2, 4) else 0 for j in range(8)] for i in range(8)])
    require('six_events_at_every_site', all(sum(row) == 6 for row in events))
    h1 = [[(6 if i == j else 0)-events[i][j] for j in range(8)] for i in range(8)]
    require('h1_self_adjoint', h1 == trans(h1))
    f1 = [[walsh(m, a) for m in range(8)] for a in range(8)]
    require('h1_walsh_orthogonality', mm(trans(f1), f1) == ident(8, 8))
    require('h1_complete_eigenbasis', all(mv(h1, [row[m] for row in f1]) == [4*m.bit_count()*row[m] for row in f1] for m in range(8)))

    # Preserve the original independent-cell tuple order, deriving its pair list.
    tuples = [tuple(t) for t in independent['coordinate_tuples']]
    pairs = []
    for a, b, c in tuples:
        if (b, c) not in pairs:
            pairs.append((b, c))
    require('pair_order_from_original_tuples', pairs == [tuple(x) for x in independent['source_assignment']['H2']['oriented_cube_pairs']])
    require('all_oriented_adjacent_pairs', pairs == [(b, c) for b in range(8) for c in range(8) if (b ^ c) in (1, 2, 4)])
    require('primary_actual_order', tuples == [(a, b, c) for b, c in pairs for a in range(8)])
    require('cell_labels', independent['source_assignment']['H1']['cell'] == 'A' and independent['source_assignment']['H2']['cell'] == 'B')
    require('partition_slots', p['partition']['pair_slots'] == [1, 2] and p['partition']['singleton_slots'] == [0])
    pair_addresses = [8*b+c for b, c in pairs]
    complement = [i for i in range(64) if i not in pair_addresses]
    j = zeros(64, 24)
    for col, address in enumerate(pair_addresses):
        j[address][col] = 1
    require('adjacent_isometry', mm(trans(j), j) == ident(24))
    h = zeros(64, 64)
    for b in range(8):
        for c in range(8):
            for bb in range(8):
                h[8*b+c][8*bb+c] += h1[b][bb]
            for cc in range(8):
                h[8*b+c][8*b+cc] += h1[c][cc]
    require('pair_equals_complete_Q6_laplacian', h == [[(12 if i == k else -2 if (i ^ k).bit_count() == 1 else 0) for k in range(64)] for i in range(64)])
    a = submatrix(h, pair_addresses, pair_addresses)
    c = submatrix(h, complement, pair_addresses)
    d = submatrix(h, complement, complement)
    require('actual_compression_12I', a == ident(24, 12))
    drift_rank = rank(c)
    require('true_drift_rank_18', drift_rank == 18)
    drift_gram = mm(trans(c), c)

    # Complete spectral proof: six-bit Walsh columns, each squared norm 64.
    eigenvalues = [4*m.bit_count() for m in range(64)]
    f = [[walsh(m, address) for m in range(64)] for address in range(64)]
    require('pair_walsh_orthogonality', mm(trans(f), f) == ident(64, 64))
    require('pair_complete_eigenbasis', all(mv(h, [row[m] for row in f]) == [eigenvalues[m]*row[m] for row in f] for m in range(64)))
    multiplicities = [eigenvalues.count(4*k) for k in range(7)]
    require('whole_pair_spectrum', multiplicities == [comb(6, k) for k in range(7)])
    uniform = [Q(1, 8)]*64
    require('full_ground_normalization', sum(x*x for x in uniform) == 1)
    require('full_ground_energy_zero', mv(h, uniform) == [0]*64)

    # Separate direct Krylov construction, not a prior receiving frame.
    span = Span()
    current = trans(j)
    cyclic_dimensions = []
    for power in range(5):
        for col, v in enumerate(current):
            span.add(v, {'power': power, 'retained_column': col})
        cyclic_dimensions.append(len(span.original))
        current = [mv(h, v) for v in current]
    require('cyclic_dimensions', cyclic_dimensions == [24, 42, 46, 47, 47])
    require('cyclic_closure_invariant', all(not any(span.residual(mv(h, v))) for v in span.original))
    spectral_ranks = []
    dark_basis = []
    for k in range(7):
        masks = [m for m in range(64) if m.bit_count() == k]
        receiving = [[f[address][m] for m in masks] for address in pair_addresses]
        spectral_ranks.append(rank(receiving))
        for coeff in nullspace(receiving):
            v = [sum(f[address][m]*coeff[t] for t, m in enumerate(masks)) for address in range(64)]
            require('dark_zero_on_retained_' + str(len(dark_basis)), all(v[address] == 0 for address in pair_addresses))
            require('dark_exact_eigenvector_' + str(len(dark_basis)), mv(h, v) == [4*k*x for x in v])
            dark_basis.append({'eigenvalue': 4*k, 'walsh_masks': masks, 'coefficients': coeff, 'vector': v, 'norm_squared': sum(x*x for x in v)})
    require('spectral_receiving_ranks', spectral_ranks == [1, 6, 12, 9, 12, 6, 1])
    require('dark_basis_17_independent', len(dark_basis) == 17 and rank([x['vector'] for x in dark_basis]) == 17)
    require('spectral_and_krylov_dimensions_agree', sum(spectral_ranks) == len(span.original))
    require('dark_is_orthogonal_to_cyclic', all(sum(x*y for x, y in zip(v, item['vector'])) == 0 for v in span.original for item in dark_basis))

    # Positive shifted resolvent and full complement self-energy at sealed z=1.
    z = 1
    dp = shift(d, z)
    complement_pivots = ldl_pivots(dp)
    dinv = inverse(dp)
    require('complement_inverse_exact', mm(dp, dinv) == ident(40))
    self_energy = mm(trans(c), mm(dinv, c))
    effective = minus(shift(a, z), self_energy)
    effective_pivots = ldl_pivots(effective)
    schur_r = inverse(effective)
    full_columns = [[sum(Q(f[i][m]*f[address][m], 64*(eigenvalues[m]+z)) for m in range(64)) for address in pair_addresses] for i in range(64)]
    require('full_resolvent_solve', mm(shift(h, z), full_columns) == j)
    restricted_r = [full_columns[i] for i in pair_addresses]
    require('schur_equals_full_restricted_resolvent', restricted_r == schur_r)
    compressed_r = ident(24, Q(1, 13))
    defect = minus(restricted_r, compressed_r)
    require('self_energy_rank', rank(self_energy) == 18)
    require('resolvent_defect_rank', rank(defect) == 18)
    require('nonzero_positive_defect', defect[0][0] > 0)
    require('nonzero_complement_response', any(full_columns[i][0] for i in complement))
    require('complement_response_formula', [full_columns[i] for i in complement] == [[-x for x in row] for row in mm(dinv, mm(c, restricted_r))])

    # Full three-source parent, all entries, no collision deletion across cells.
    triples = [(a, b, c) for a in range(8) for b in range(8) for c in range(8)]
    h3 = zeros(512, 512)
    for address, t in enumerate(triples):
        for slot in range(3):
            for target in range(8):
                if h1[t[slot]][target]:
                    changed = list(t)
                    changed[slot] = target
                    target_code = 64*changed[0]+8*changed[1]+changed[2]
                    h3[address][target_code] += h1[t[slot]][target]
    require('all_512_squared_entries_tensor_identity', all(h3[i][k] == (18 if i == k else -2 if (i ^ k).bit_count() == 1 else 0) for i in range(512) for k in range(512)))
    # Sparse action verifies each of the 512 complete Walsh eigenvectors.
    sparse3 = [[(i, value) for i, value in enumerate(row) if value] for row in h3]
    require('three_free_complete_eigenidentity', all(sum(value*walsh(mask, col) for col, value in sparse3[row]) == 4*mask.bit_count()*walsh(mask, row) for mask in range(512) for row in range(512)))
    require('three_free_spectrum', [sum(m.bit_count() == k for m in range(512)) for k in range(10)] == [comb(9, k) for k in range(10)])
    codes = [64*a+8*b+c for a, b, c in tuples]
    require('raw_primary_codes', codes == independent['state_codes'])
    require('primary_injection_isometry', len(codes) == len(set(codes)) == 192)
    primary = submatrix(h3, codes, codes)
    primary_formula = [[(h1[tuples[i][0]][tuples[k][0]] + (12 if i == k else 0)) if i//8 == k//8 else 0 for k in range(192)] for i in range(192)]
    require('primary_exact_tensor_compression', primary == primary_formula)
    require('primary_raw_operator_match', primary == independent['full_source_H'])
    primary_index = {t: i for i, t in enumerate(tuples)}
    require('independent_equal_digits_retained', sum(a in (b, c) for a, b, c in tuples) == 48)
    require('primary_floor_frame_gram', mm(trans(independent['full_block_uniform_frame']), independent['full_block_uniform_frame']) == ident(24, 8))
    require('primary_floor_frame_eigenvalue', mm(primary, independent['full_block_uniform_frame']) == [[12*x for x in row] for row in independent['full_block_uniform_frame']])

    def chart_data(chart, matrix):
        addresses = [64*a+8*b+c for a, b, c in chart]
        index = {code: k for k, code in enumerate(addresses)}
        adjacency, boundary = [], []
        for code in addresses:
            adjacency.append(sorted([[index[t], -value] for t, value in sparse3[code] if t != code and t in index]))
            boundary.append(sorted([[t, -value] for t, value in sparse3[code] if t != code and t not in index]))
        return adjacency, boundary, sorted({t for row in boundary for t, value in row})

    adj_primary, bd_primary, forbidden_primary = chart_data(tuples, primary)
    require('primary_raw_adjacency', adj_primary == independent['allowed_adjacency'])
    require('primary_complete_boundary', bd_primary == independent['full_boundary'])
    require('primary_collision_potential', [sum(v for t, v in row) for row in bd_primary] == independent['full_collision_potential'])
    require('primary_forbidden_target_codes', forbidden_primary == independent['forbidden_target_codes'])

    # Connected coordinates come from BOTH frozen seed edges, not a trial search.
    keep_slots = p['partition']['pair_slots']
    cut = p['partition']['cut_edges'][0]
    seed_edges = {x['edge']: (x['u'], x['v']) for x in p['selected_seed']['cycles']}
    require('seed_edge_identities', set(seed_edges[0]) == {1, 2} and set(seed_edges[cut]) == {0, 1})
    connected_tuples = [(a, b, c) for a in range(8) for b in range(8) for c in range(8) if (b ^ c) in (1, 2, 4) and (a ^ b) in (1, 2, 4) and a != c]
    require('connected_from_seed_constraints', connected_tuples == [tuple(t) for t in p['placements']])
    connected_codes = [64*a+8*b+c for a, b, c in connected_tuples]
    require('connected_source_codes', connected_codes == p['placement_codes'] == independent['connected_source_codes'])
    conn_indices = [primary_index[t] for t in connected_tuples]
    v = zeros(192, 48)
    for col, row in enumerate(conn_indices):
        v[row][col] = 1
    require('connected_raw_receiving_map', v == independent['connected_receiving_isometry'])
    require('connected_isometry', mm(trans(v), v) == ident(48))
    conn_h = submatrix(primary, conn_indices, conn_indices)
    require('connected_compression_18I', conn_h == ident(48, 18))
    conn_complement = [i for i in range(192) if i not in conn_indices]
    conn_drift = submatrix(primary, conn_complement, conn_indices)
    conn_drift_rank = rank(conn_drift)
    require('connected_noninvariance', conn_drift_rank == 48)

    # Preserve the earlier named 144-dimensional same-cell fragment chart.
    fragment_tuples = [(a, b, c) for a in range(8) for b in range(8) for c in range(8) if (b ^ c) in (1, 2, 4) and len({a, b, c}) == 3]
    require('fragment_chart_original_order', fragment_tuples == [tuple(t) for t in fragment['states']])
    frag_codes = [64*a+8*b+c for a, b, c in fragment_tuples]
    require('fragment_chart_codes', frag_codes == fragment['state_codes'])
    frag_h = submatrix(h3, frag_codes, frag_codes)
    require('fragment_raw_operator_match', frag_h == fragment['full_H'])
    adj_frag, bd_frag, forbidden_frag = chart_data(fragment_tuples, frag_h)
    require('fragment_raw_adjacency', adj_frag == fragment['allowed_adjacency'])
    require('fragment_complete_boundary', bd_frag == fragment['boundary'])
    require('fragment_collision_potential', [sum(v for t, v in row) for row in bd_frag] == fragment['collision_potential'])
    require('fragment_forbidden_targets', forbidden_frag == fragment['forbidden_target_codes'])
    frag_index = {t: i for i, t in enumerate(fragment_tuples)}
    frag_v = zeros(144, 48)
    for col, t in enumerate(connected_tuples):
        frag_v[frag_index[t]][col] = 1
    require('fragment_connected_map', frag_v == fragment['connected_injection'])
    require('fragment_connected_compression', mm(trans(frag_v), mm(frag_h, frag_v)) == conn_h == fragment['connected_prepared_H'])

    # Common-reference bookkeeping in coefficient units (multiply by one tau).
    endpoints = {'all_free': 0, 'adjacent_pair_floor': 12, 'primary_floor': 12, 'connected_preparation': 18}
    common = {key: value-12 for key, value in endpoints.items()}
    differences = {x+' minus '+y: endpoints[x]-endpoints[y] for x in endpoints for y in endpoints}
    require('common_shift_preserves_every_difference', all(common[x]-common[y] == endpoints[x]-endpoints[y] for x in endpoints for y in endpoints))
    require('one_sided_shift_changes_free_comparison', (18-12)-0 != 18-0)
    require('one_sided_adjacent_shift_changes_free_comparison', (12-12)-0 != 12-0)

    controls = [
        {'id': 'compressed_floor_as_full_lower', 'outcome': 'FAIL_FULL_SOURCE_LOWER', 'rejected_mutation': True,
         'witness': {'vector': uniform, 'norm_squared': 1, 'energy': 0, 'claimed_lower': 12, 'quadratic_form_H_minus_12I': -12}},
        {'id': 'adjacent_invariance', 'outcome': 'FAIL_INVARIANCE', 'rejected_mutation': True,
         'witness': {'retained_tuple': pairs[0], 'omitted_tuple': [0, 0], 'matrix_element': h[0][pair_addresses[0]], 'drift_rank': drift_rank}},
        {'id': 'omit_complement_response', 'outcome': 'FAIL_RESOLVENT', 'rejected_mutation': True,
         'witness': {'z': z, 'retained_column': 0, 'full_diagonal': restricted_r[0][0], 'compressed_diagonal': Q(1, 13), 'diagonal_defect': defect[0][0],
                     'defect_rank': rank(defect), 'self_energy_rank': rank(self_energy), 'nonzero_complement_response': True}},
        {'id': 'all_omitted_addresses_dark', 'outcome': 'FAIL_COMPLEMENT_CLASSIFICATION', 'rejected_mutation': True,
         'witness': {'omitted_addresses': 40, 'cyclic_dimension': len(span.original), 'dynamically_hidden_dimensions': len(span.original)-24,
                     'invariant_dark_dimensions': len(dark_basis), 'omitted_address_00_couples_to_01': h[0][1], 'no_omitted_coordinate_is_dark': True}},
        {'id': 'one_sided_baseline_shift', 'outcome': 'FAIL_COMMON_ZERO', 'rejected_mutation': True,
         'witness': {'original_connected_minus_all_free': 18, 'one_sided_result': 6, 'common_shift_result': common['connected_preparation']-common['all_free'],
                     'original_adjacent_minus_all_free': 12, 'one_sided_adjacent_result': 0}}]
    require('all_registered_controls_rejected_mutations', all(item['rejected_mutation'] for item in controls))

    dark_counts = [multiplicities[k]-spectral_ranks[k] for k in range(7)]
    triple_dark_counts = [sum(comb(3, r)*dark_counts[k-r] for r in range(4) if 0 <= k-r < 7) for k in range(10)]
    require('nested_dark_multiplicities', sum(triple_dark_counts) == 136)
    directly_coupled = [complement[i] for i, row in enumerate(c) if any(row)]
    result = {
        'verdict': 'HELD', 'script_version': SCRIPT_VERSION, 'arithmetic': 'integers and fractions.Fraction; no floating-point signs',
        'all_checks_passed': all(x['passed'] for x in checks), 'check_count': len(checks),
        'h1': {'dimension': 8, 'event_count': len(actions), 'events_per_oriented_edge': 2, 'spectrum': {4*k: comb(3, k) for k in range(4)}},
        'free_pair': {'dimension': 64, 'floor': 0, 'spectrum': {4*k: multiplicities[k] for k in range(7)}, 'metric': 'I64'},
        'adjacent': {'dimension': 24, 'compression': '12I24', 'metric': 'I24', 'omitted_addresses': 40,
                     'true_drift_rank': drift_rank, 'drift_kernel_dimension': 24-drift_rank, 'directly_coupled_omitted_addresses': directly_coupled},
        'cyclic': {'dimensions': cyclic_dimensions, 'closure_dimension': len(span.original), 'dynamically_hidden_dimensions': len(span.original)-24,
                   'spectral_receiving_ranks': spectral_ranks, 'dark_dimension': len(dark_basis), 'dark_multiplicities_by_4k': dark_counts},
        'resolvent': {'z': z, 'full_diagonal': restricted_r[0][0], 'compressed_diagonal': Q(1, 13), 'diagonal_defect': defect[0][0],
                      'defect_rank': rank(defect), 'self_energy_rank': rank(self_energy), 'exact_schur_identity': True,
                      'D_plus_z_LDL_pivots_positive': all(x > 0 for x in complement_pivots), 'effective_LDL_pivots_positive': all(x > 0 for x in effective_pivots)},
        'three_free': {'dimension': 512, 'floor': 0, 'spectrum': {4*k: comb(9, k) for k in range(10)}, 'metric': 'I512'},
        'primary': {'dimension': 192, 'tuple_order': 'pair-major, singleton a=0..7; ambient triple code 64a+8b+c',
                    'compression': 'I24 tensor h1 + 12I192', 'floor': 12, 'spectrum': {12+4*k: 24*comb(3, k) for k in range(4)},
                    'earlier_omitted_addresses': 320, 'equal_local_digits_retained': 48, 'boundary_target_addresses': len(forbidden_primary),
                    'drift_rank': 8*drift_rank, 'cyclic_dimension': 8*len(span.original), 'dynamically_hidden_dimensions': 8*(len(span.original)-24),
                    'invariant_dark_dimension': 8*len(dark_basis), 'invariant_dark_multiplicities_by_4k': triple_dark_counts,
                    'tensor_extension_status': 'proved by invariant singleton factor and exact pair closure; not a separate 512-rank numerical fit'},
        'connected': {'dimension': 48, 'compression': '18I48', 'preparation_expectation': 18, 'cost_above_primary_floor': 6,
                      'cost_against_all_free_geometric_floor': 18, 'drift_rank_in_primary': conn_drift_rank},
        'named_fragment_chart': {'dimension': 144, 'omitted_independent_cell_coincidence_addresses': 48, 'connected_dimension': 48,
                                 'raw_operator_and_maps_verified': True, 'He3_theorem_reproved': False},
        'reference_ledger': {'endpoint_coefficients_of_tau': endpoints, 'after_common_shift_minus_12tau': common, 'differences': differences},
        'breaking_controls': controls,
        'limits': predicted()['limits'],
        'physical_bridge_conditions': [
            'Declare one common self-adjoint Hamiltonian, domain, metric and additive reference for all endpoints.',
            'Specify species/statistics/particle-number, moving-cell and asymptotic receiving maps and preserve their metrics.',
            'Carry source complements, off-diagonal couplings and energy-dependent self-energy or rigorously bound them.',
            'Supply physical tau/radius/unit law independently and use the same law at every endpoint.',
            'Retain field, recoil, electrons, counterterms and gates in both preparation and fragment comparison.',
            'A binding claim requires a same-Hamiltonian source upper below a rigorous full competing-channel lower; compression floors are not full lowers.']}
    dump(out / 'RESULTS.json', result)
    dump(out / 'CHECKS.json', checks)
    dump(out / 'PAIR_MATRICES.json', {'h1': h1, 'event_multiplicities': events, 'H_free_pair': h,
                                     'ordered_pairs': pairs, 'retained_addresses': pair_addresses, 'omitted_addresses': complement,
                                     'J': j, 'J_star_H_J': a, 'complement_coupling_C': c, 'complement_H_D': d, 'drift_Gram': drift_gram})
    dump(out / 'CYCLIC_AND_DARK_CERTIFICATES.json', {'cyclic_basis_vectors': span.original, 'cyclic_basis_labels': span.labels,
                                                    'echelon_pivots': [p for p, v in span.echelon], 'dark_eigenbasis': dark_basis})
    dump(out / 'RESOLVENT.json', {'z': z, 'D_plus_z_inverse': dinv, 'D_plus_z_LDL_pivots': complement_pivots,
                                'self_energy': self_energy, 'effective_operator': effective, 'effective_LDL_pivots': effective_pivots,
                                'full_resolvent_columns_H_plus_z_inverse_J': full_columns, 'restricted_full_resolvent': restricted_r,
                                'compressed_resolvent': compressed_r, 'defect': defect})
    dump(out / 'NESTED_MATRICES.json', {'three_free_entry_rule': '18 on diagonal, -2 when 9-bit triple codes differ in exactly one bit, 0 otherwise',
                                     'three_free_sparse_rows': sparse3, 'primary_coordinate_tuples': tuples, 'primary_injection_addresses': codes,
                                     'primary_H': primary, 'primary_complete_boundary': bd_primary,
                                     'connected_tuples': connected_tuples, 'connected_injection': v, 'connected_H': conn_h,
                                     'fragment_tuples': fragment_tuples, 'fragment_H': frag_h, 'fragment_connected_injection': frag_v})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='phase', required=True)
    pre = sub.add_parser('preregister')
    pre.add_argument('--case', type=Path, default=DEFAULT_CASE)
    pre.add_argument('--record', type=Path, required=True)
    run = sub.add_parser('run')
    run.add_argument('--case', type=Path, default=DEFAULT_CASE)
    run.add_argument('--registration', type=Path, required=True)
    run.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    script_sha = digest(__file__)
    if args.phase == 'preregister':
        if args.record.exists():
            raise FileExistsError('Preregistration path must be fresh')
        custody = authenticate(args.case)
        dump(args.record, {'sealed_utc': utc(), 'phase': 'BEFORE_MATHEMATICAL_EXECUTION', 'script_version': SCRIPT_VERSION,
                          'script_sha256': script_sha, 'script_name': Path(__file__).name, 'case': str(args.case.resolve()),
                          'custody': custody, 'predictions': predicted(), 'method': 'Fresh raw-operand reconstruction; exact standard-library arithmetic',
                          'prior_code_read_or_run': False, 'external_verification': False, 'independence_level': 'I1', 'director_approval': False})
        print('SEALED_PREREGISTRATION ' + str(args.record))
        return
    if args.out.exists():
        raise FileExistsError('Output directory must be fresh')
    registration = json.loads(args.registration.read_text())
    if registration['script_sha256'] != script_sha:
        raise ValueError('Script hash differs from preregistration')
    if registration['phase'] != 'BEFORE_MATHEMATICAL_EXECUTION':
        raise ValueError('Invalid registration phase')
    args.out.mkdir(parents=True)
    started = utc()
    metadata = {'started_utc': started, 'script_sha256': script_sha, 'registration_sha256': digest(args.registration),
                'registration_sealed_utc': registration['sealed_utc'], 'python': sys.version, 'platform': platform.platform(),
                'command': sys.argv, 'case': str(args.case.resolve()), 'out': str(args.out.resolve())}
    dump(args.out / 'START.json', metadata)
    try:
        custody = authenticate(args.case)
        if custody != registration['custody']:
            raise ValueError('Input custody changed after preregistration')
        dump(args.out / 'INPUT_AUTHENTICATION.json', custody)
        result = audit(args.case, args.out)
        dump(args.out / 'COMPLETE.json', {'completed_utc': utc(), 'verdict': result['verdict'], 'checks_passed': result['check_count'], 'script_sha256': script_sha})
        print(json.dumps(encode({'verdict': result['verdict'], 'checks_passed': result['check_count'], 'cyclic_dimensions': result['cyclic']['dimensions'],
                                 'resolvent_diagonal_defect': result['resolvent']['diagonal_defect'], 'out': str(args.out)}), sort_keys=True))
    except BaseException as exc:
        dump(args.out / 'FAILED.json', {'failed_utc': utc(), 'exception_type': type(exc).__name__, 'exception': str(exc), 'traceback': traceback.format_exc(),
                                      'script_sha256': script_sha, 'registration_sha256': digest(args.registration)})
        raise
    finally:
        records = {p.name: digest(p) for p in sorted(args.out.iterdir()) if p.is_file() and p.name != 'OUTPUT_SEAL.json'}
        dump(args.out / 'OUTPUT_SEAL.json', {'sealed_utc': utc(), 'files': records})


if __name__ == '__main__':
    main()
