#!/usr/bin/env python3
"""Independent CR2 shared-field reconstruction; Python standard library only.

Only owning mathematical operand fields enter calculations. In particular the
colour file's data.program and data.output are never decoded or evaluated.
Every run requires an existing, script-hash-matching execution preregistration
and a new output directory. All finite arithmetic is rational or Gaussian
rational. Unit profile examples are coefficient diagnostics, not physical fits.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
import traceback


@dataclass(frozen=True, eq=False)
class QC:
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "re", F(self.re))
        object.__setattr__(self, "im", F(self.im))

    @staticmethod
    def cast(x):
        return x if isinstance(x, QC) else QC(F(x), F(0))

    def __add__(self, x):
        x = self.cast(x)
        return QC(self.re + x.re, self.im + x.im)

    __radd__ = __add__

    def __neg__(self):
        return QC(-self.re, -self.im)

    def __sub__(self, x):
        return self + (-self.cast(x))

    def __rsub__(self, x):
        return self.cast(x) - self

    def __mul__(self, x):
        x = self.cast(x)
        return QC(self.re * x.re - self.im * x.im,
                  self.re * x.im + self.im * x.re)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = self.cast(x)
        den = x.re * x.re + x.im * x.im
        return QC((self.re * x.re + self.im * x.im) / den,
                  (self.im * x.re - self.re * x.im) / den)

    def __rtruediv__(self, x):
        return self.cast(x) / self

    def __bool__(self):
        return bool(self.re or self.im)

    def __eq__(self, x):
        try:
            x = self.cast(x)
        except (TypeError, ValueError):
            return False
        return self.re == x.re and self.im == x.im

    def conjugate(self):
        return QC(self.re, -self.im)


I = QC(0, 1)


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def exact_json(x):
    if isinstance(x, float):
        raise TypeError("Floating point is not permitted in exact artifacts")
    if isinstance(x, QC):
        return {"re": str(x.re), "im": str(x.im)}
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): exact_json(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [exact_json(v) for v in x]
    return x


def write_json(path, obj):
    Path(path).write_text(json.dumps(exact_json(obj), indent=2, sort_keys=True) + "\n")


def real_matrix(a):
    return [[F(x) for x in row] for row in a]


def zeros(n, m=None):
    return [[0] * (n if m is None else m) for _ in range(n)]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(x) for x in zip(*a)]


def dagger(a):
    return [[x.conjugate() for x in row] for row in transpose(a)]


def mm(a, b):
    assert len(a[0]) == len(b)
    ans = zeros(len(a), len(b[0]))
    brows = [[(j, x) for j, x in enumerate(row) if x] for row in b]
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in brows[k]:
                    ans[i][j] += x * y
    return ans


def scale(a, c):
    return [[c * x for x in row] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a, b):
    return add(a, scale(b, -1))


def kron(a, b):
    return [[a[i][j] * b[k][l]
             for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def mv(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def dot(a, b):
    return sum(x.conjugate() * y for x, y in zip(a, b))


def norm2(v):
    return dot(v, v)


def expect(v, a):
    return dot(v, mv(a, v)) / norm2(v)


def gram(a, b=None):
    return mm(dagger(a), a if b is None else b)


def rank(a):
    a = [[x if isinstance(x, QC) else F(x) for x in row] for row in a]
    piv = 0
    for j in range(len(a[0])):
        row = next((i for i in range(piv, len(a)) if a[i][j]), None)
        if row is None:
            continue
        a[piv], a[row] = a[row], a[piv]
        c = a[piv][j]
        a[piv] = [x / c for x in a[piv]]
        for i in range(piv + 1, len(a)):
            c = a[i][j]
            if c:
                a[i] = [x - c * y for x, y in zip(a[i], a[piv])]
        piv += 1
        if piv == len(a):
            break
    return piv


def determinant(a):
    a = [[x if isinstance(x, QC) else F(x) for x in row] for row in a]
    ans = F(1)
    for j in range(len(a)):
        row = next((i for i in range(j, len(a)) if a[i][j]), None)
        if row is None:
            return F(0)
        if row != j:
            a[j], a[row] = a[row], a[j]
            ans = -ans
        c = a[j][j]
        ans *= c
        for i in range(j + 1, len(a)):
            c = a[i][j] / a[j][j]
            if c:
                a[i] = [x - c * y for x, y in zip(a[i], a[j])]
    return ans


def real(x):
    if isinstance(x, QC):
        assert not x.im
        return x.re
    return F(x)


def embed_pair(b, slots):
    """Literal n=a+4b+16c; first named pair slot is fast."""
    a = zeros(64)
    for col in range(64):
        digits = [col % 4, (col // 4) % 4, col // 16]
        pair_col = digits[slots[0]] + 4 * digits[slots[1]]
        for pair_row in range(16):
            v = b[pair_row][pair_col]
            if v:
                rd = list(digits)
                rd[slots[0]] = pair_row % 4
                rd[slots[1]] = pair_row // 4
                a[rd[0] + 4 * rd[1] + 16 * rd[2]][col] = v
    return a


def exterior_frame(arity):
    combos = list(itertools.combinations(range(4), arity))
    a = zeros(4 ** arity, len(combos))
    for j, combo in enumerate(combos):
        for perm in itertools.permutations(combo):
            inversions = sum(perm[i] > perm[k] for i in range(arity)
                             for k in range(i + 1, arity))
            row = sum((4 ** i) * x for i, x in enumerate(perm))
            a[row][j] = (-1) ** inversions
    return a


def load_colour_operators(path):
    """Decode only data.operators, stopping before output/program members."""
    raw = Path(path).read_text()
    m = re.search(r'"data"\s*:\s*\{\s*"operators"\s*:', raw)
    if m is None:
        raise ValueError("Frozen colour data.operators location changed")
    operators, _end = json.JSONDecoder().raw_decode(raw[m.end():].lstrip())
    return {k: real_matrix(v) for k, v in operators.items()}


def contraction(cov, blocks, profile=None):
    a = zeros(4)
    for i in range(len(cov)):
        for j in range(len(cov)):
            weight = cov[i][j]
            if profile is not None:
                weight *= profile[i][j]
            a = add(a, scale(blocks[i][j], weight))
    return a


def main(args, out):
    checks = []

    def check(label, actual, expected):
        ok = actual == expected
        checks.append({"id": label, "passed": ok, "actual": actual,
                       "expected": expected})
        return ok

    case = Path(args.case).resolve()
    prereg = json.loads(Path(args.preregistration).read_text())
    script_sha = digest(__file__)
    if prereg["script_sha256"] != script_sha:
        raise ValueError("Preregistration does not authenticate this replay script")
    frozen = json.loads((case / "FREEZE.json").read_text())
    custody = []
    for rel, expected in frozen["files"].items():
        got = digest(case / rel)
        custody.append({"file": rel, "expected_sha256": expected,
                        "actual_sha256": got, "passed": got == expected})
    if not all(x["passed"] for x in custody):
        write_json(out / "INPUT_AUTHENTICATION.json", custody)
        raise ValueError("Frozen input authentication failed before computation")
    check("all_frozen_file_hashes", len(custody), 25)
    write_json(out / "INPUT_AUTHENTICATION.json", {
        "authenticated_utc": utc(), "files": custody,
        "FREEZE_sha256": digest(case / "FREEZE.json"),
        "script_sha256": script_sha,
        "execution_preregistration_sha256": digest(args.preregistration),
        "program_fields_consumed": False,
    })

    # Owning placement operands only. No generated full64 matrix is an input.
    primary = json.loads((case / "sources/light/HE3_INDEPENDENT_FRAGMENTS.json").read_text())
    placement = json.loads((case / "sources/light/HE3_PLACEMENT.json").read_text())
    multi = json.loads((case / "sources/MULTI_FIELD_OPERANDS.json").read_text())
    tuples = [tuple(x) for x in primary["coordinate_tuples"]]
    codes = [64 * x + 8 * y + z for x, y, z in tuples]
    check("primary_literal_source_codes", codes, primary["state_codes"])
    check("primary_full_dimension", len(tuples), 192)
    state_tuples = [(s["H1_site"], s["H2_proton_site"], s["H2_neutron_site"])
                    for s in primary["states"]]
    check("primary_tuples_match_cell_labelled_states", state_tuples, tuples)
    receiving_codes = placement["placement_codes"]
    check("connected_codes_match_owning_placement", primary["connected_source_codes"], receiving_codes)
    check("connected_tuples_match_owning_placement", [64*x+8*y+z for x,y,z in placement["placements"]], receiving_codes)
    h192 = [[(18 if i == j else -2 if a[1:] == b[1:] and
               (a[0] ^ b[0]).bit_count() == 1 else 0)
              for j, b in enumerate(tuples)] for i, a in enumerate(tuples)]
    check("complete_H192_from_cube_rule_and_baseline", h192,
          real_matrix(primary["full_source_H"]))
    j192 = [[int(code == rc) for rc in receiving_codes] for code in codes]
    check("complete_J192_from_connected_address_codes", j192,
          real_matrix(primary["connected_receiving_isometry"]))
    check("J192_isometry", gram(j192), eye(48))
    p192 = mm(j192, transpose(j192))
    pair0 = tuples[0][1:]
    fibre_indices = [i for i, t in enumerate(tuples) if t[1:] == pair0]
    h8 = [[h192[i][j] for j in fibre_indices] for i in fibre_indices]
    recv_cols = [j for j in range(48) if any(j192[i][j] for i in fibre_indices)]
    j8 = [[j192[i][j] for j in recv_cols] for i in fibre_indices]
    p8 = mm(j8, transpose(j8))
    receiving_local = [i for i in range(8) if p8[i][i]]
    check("first_fibre_has_all_eight_addresses", [tuples[i][0] for i in fibre_indices], list(range(8)))
    check("first_fibre_receiving_addresses", receiving_local, [2, 4])
    check("receiving_cube_distance", (receiving_local[0] ^ receiving_local[1]).bit_count(), 2)
    pair_labels = list(dict.fromkeys(t[1:] for t in tuples))
    fibre_audit = []
    for pair in pair_labels:
        inds = [i for i,t in enumerate(tuples) if t[1:] == pair]
        rec = [tuples[i][0] for i in inds if p192[i][i]]
        hh = [[h192[i][j] for j in inds] for i in inds]
        valid = (len(inds) == 8 and hh == h8 and len(rec) == 2
                 and (rec[0] ^ rec[1]).bit_count() == 2)
        fibre_audit.append({"pair": pair, "indices": inds, "receiving": rec,
                            "valid": valid})
    check("all_24_full_fibres_and_receivers", all(x["valid"] for x in fibre_audit), True)
    check("actual_pair_label_count", len(pair_labels), 24)
    h64 = add(kron(h8, eye(8)), kron(eye(8), h8))
    j64 = kron(j8, j8)
    p1, p2 = kron(p8, eye(8)), kron(eye(8), p8)
    pjoint = mm(j64, transpose(j64))
    q64 = sub(eye(64), pjoint)
    check("J64_isometry", gram(j64), eye(4))
    check("P1_projection", mm(p1, p1), p1)
    check("P2_projection", mm(p2, p2), p2)
    check("P1_P2_commute", mm(p1, p2), mm(p2, p1))
    check("joint_receiver_equals_P1P2", pjoint, mm(p1, p2))
    check("full_placement_complement_dimension", rank(q64), 60)
    leakage = mm(mm(q64, h64), j64)
    check("retained_complete_receiving_leakage_rank", rank(leakage), 4)
    walsh_ok = True
    h8_spectrum = []
    for s in range(8):
        v = [(-1) ** ((s & x).bit_count()) for x in range(8)]
        eigen = 12 + 4 * s.bit_count()
        walsh_ok &= mv(h8, v) == [eigen*x for x in v]
        h8_spectrum.append(eigen)
    check("all_eight_full_fibre_Walsh_eigenvectors", walsh_ok, True)
    # Comparison operands are read only after construction is complete.
    prior_tensor = json.loads((case / "prior/TENSOR_TWO_OPERANDS.json").read_text())
    check("declared_fibre_indices", fibre_indices, prior_tensor["source_fibre_indices"])
    check("declared_receiving_columns", recv_cols, prior_tensor["receiving_columns"])
    check("reconstructed_H64_matches_frozen_comparison", h64, real_matrix(prior_tensor["full_H"]))
    check("reconstructed_J64_matches_frozen_comparison", j64, real_matrix(prior_tensor["receiver"]))
    preparations = {}
    for name in ("correlated", "anticorrelated"):
        v = [F(x) for x in multi[name + "_unnormalized"]]
        means = [expect(v, p) for p in (p1, p2)]
        moments = [[expect(v, mm(a,b)) for b in (p1,p2)] for a in (p1,p2)]
        cov = [[moments[i][j]-means[i]*means[j] for j in range(2)] for i in range(2)]
        sign = 1 if name == "correlated" else -1
        check(name + "_raw_norm", norm2(v), 2)
        check(name + "_means", means, [F(1,2),F(1,2)])
        check(name + "_covariance", cov, [[F(1,4),F(sign,4)],[F(sign,4),F(1,4)]])
        preparations[name] = {"raw": v, "raw_norm_squared": norm2(v),
                              "means": means, "joint_moments": moments, "covariance": cov}
    write_json(out / "PLACEMENT_OPERANDS.json", {
        "source_order": "literal primary192; tensor index 8*x+y for two tagged copies of its first fibre",
        "full_primary_dimension": 192, "tensor_full_parent_dimension": 192**2,
        "pair_multiplicity": 24**2, "pair0": pair0,
        "first_fibre_indices": fibre_indices, "receiving_columns": recv_cols,
        "fibre_audit": fibre_audit, "H192": h192, "J192": j192,
        "H8": h8, "J8": j8, "P8": p8,
        "H64": h64, "J64": j64, "P1": p1, "P2": p2,
        "joint_receiver": pjoint, "complete_receiver_complement": q64,
        "true_complementary_drift_Gram": gram(leakage),
        "H8_spectrum": h8_spectrum, "H64_floor": 24,
        "H64_top": 48, "source_reference_shift_applied": 0,
        "preparations": preparations,
    })

    # Literal-order full64 colour operators, rebuilt from raw pair entries.
    ops = load_colour_operators(case / "sources/light/COLOUR_64_CONSTRUCTION_PAYLOAD.json")
    pair = json.loads((case / "sources/light/COMPLETE_DC_PAIR.json").read_text())
    d16, r16, q4 = ops["D16"], ops["R16"], ops["Q4"]
    check("D16_matches_owning_complete_pair", d16, real_matrix(pair["D"]))
    check("R16_matches_owning_complete_pair", r16, real_matrix(pair["C_over_i"]))
    d_from_q = [[(q4[b][bb] if a == aa else 0) - (q4[a][aa] if b == bb else 0)
                 for bb in range(4) for aa in range(4)] for b in range(4) for a in range(4)]
    check("D16_is_Q_second_minus_Q_first", d16, d_from_q)
    swap16 = [[int(a == bb and b == aa) for bb in range(4) for aa in range(4)]
              for b in range(4) for a in range(4)]
    check("R16_is_minus_D16_swap", r16, scale(mm(d16, swap16), -1))
    check("D16_Hermitian", d16, dagger(d16))
    check("R16_skew", r16, scale(dagger(r16), -1))
    check("C16_iR16_Hermitian", scale(r16,I), dagger(scale(r16,I)))
    check("both_physical_quadrature_full_self_Grams", gram(d16), gram(r16))
    upair = exterior_frame(2)
    u = exterior_frame(3)
    check("independently_rebuilt_pair_exterior_frame", upair, ops["Upair"])
    check("independently_rebuilt_triple_exterior_frame", u, ops["U"])
    check("pair_exterior_metric", gram(upair), scale(eye(6),2))
    check("pair_lower_projection", scale(mm(upair,transpose(upair)),F(1,2)), ops["Pa16"])
    check("complete_pair_lower_projection", ops["Pa16"], real_matrix(pair["P_lower"]))
    check("triple_source_metric", gram(u), scale(eye(4),6))
    pu = scale(mm(u,transpose(u)), F(1,6))
    qu = sub(eye(64), pu)
    check("complete_colour_complement_dimension", rank(qu), 60)
    full_real = {}
    physical = {}
    images = {}
    slots = {"12": (0,1), "23": (1,2), "13": (0,2)}
    names = []
    for lab, sl in slots.items():
        d, r = embed_pair(d16,sl), embed_pair(r16,sl)
        full_real["D"+lab], full_real["R"+lab] = d,r
        physical["D"+lab], physical["C"+lab] = d,scale(r,I)
        for name in ("D"+lab,"C"+lab):
            names.append(name)
            check(name+"_full_Hermitian", physical[name], dagger(physical[name]))
            images[name] = mm(physical[name],u)
            check(name+"_source_complement_retained", mm(qu,images[name]),images[name])
            check(name+"_compression_is_zero", mm(transpose(u),images[name]),zeros(4))
        check("R"+lab+"_U_equals_D"+lab+"_U", mm(r,u),mm(d,u))
    blocks = [[scale(gram(images[a],images[b]),F(1,6)) for b in names] for a in names]
    complete_gram = [[blocks[a//4][b//4][a%4][b%4] for b in range(24)] for a in range(24)]
    m = blocks[0][0]
    check("M_equal_D23_self", m, blocks[2][2])
    check("M_equal_D13_self", m, blocks[4][4])
    check("D12_D23_signed_cross", blocks[0][2], scale(m,F(-1,2)))
    check("D12_D13_signed_cross", blocks[0][4], scale(m,F(1,2)))
    check("D23_D13_signed_cross", blocks[2][4], scale(m,F(1,2)))
    check("D13_full_operator_sum", full_real["D13"], add(full_real["D12"],full_real["D23"]))
    check("physical_source_Gram_Hermitian", complete_gram, dagger(complete_gram))
    check("complete_signed_current_Gram_rank", rank(complete_gram), 8)
    minors = [determinant([row[:n] for row in m[:n]]) for n in range(1,5)]
    check("M_strictly_positive_by_all_leading_principal_minors", all(real(x)>0 for x in minors), True)
    helicity = {}
    for lab in slots:
        # H+/-=(D +/- i C)/sqrt(2). Keep unnormalized raw numerators,
        # then divide their Grams by two, avoiding any irrational arithmetic.
        d,c = physical["D"+lab],physical["C"+lab]
        hp,hm = add(d,scale(c,I)),sub(d,scale(c,I))
        check("helicity_"+lab+"_full64_unitary_sum",
              scale(add(gram(hp),gram(hm)),F(1,2)),add(gram(d),gram(c)))
        check("helicity_"+lab+"_plus_source_image_zero",mm(hp,u),zeros(64,4))
        check("helicity_"+lab+"_minus_source_image",mm(hm,u),scale(images["D"+lab],2))
        helicity[lab] = {"plus_normalized_source_Gram":scale(gram(mm(hp,u)),F(1,12)),
                         "minus_normalized_source_Gram":scale(gram(mm(hm,u)),F(1,12))}
    write_json(out / "COLOUR_OPERANDS.json", {
        "source_order": "n=a+4b+16c; pair index first+4*second",
        "U_independent_exterior_frame": u, "U_metric": gram(u),
        "normalized_U": "U/sqrt(6), represented exactly by Gram division once",
        "source_projection": pu, "source_complement": qu,
        "full64_real_operators": full_real,
        "physical_current_convention": "Cij=i Rij; both D and C are Hermitian",
        "physical_currents": physical, "full_source_current_images": images,
        "current_order": names, "normalized_Gram_blocks": blocks,
        "normalized_complete_signed_Gram": complete_gram,
        "M_definition": "U^T D12^T D12 U/6, full64 current image before contraction",
        "M": m, "M_leading_principal_minors": minors,
        "Gram_rank": rank(complete_gram),
        "both_quadrature_self_coefficient": scale(m,2),
        "helicity_convention":"H+/-=(D +/- i C)/sqrt(2); raw numerator Grams divided by2 and source metric6",
        "helicity_source_Grams":helicity,
    })

    dblocks = [[blocks[0][0], blocks[0][2]],[blocks[2][0], blocks[2][2]]]
    plus = preparations["correlated"]["covariance"]
    minus = preparations["anticorrelated"]["covariance"]
    vplus, vminus = contraction(plus,dblocks), contraction(minus,dblocks)
    vdiag = contraction([[F(1,4),0],[0,F(1,4)]],dblocks)
    check("correlated_coefficient_M_over_4", vplus, scale(m,F(1,4)))
    check("anticorrelated_coefficient_3M_over_4", vminus, scale(m,F(3,4)))
    check("factor_three_common_profile", vminus, scale(vplus,3))
    check("diagonal_only_same_for_both", vdiag, scale(m,F(1,2)))
    check("factor_three_denominator_positive", real(vplus[0][0])>0, True)

    # Coordinate-level completed squares on an exact finite-photon core vector.
    # Two modes are a diagnostic realization of the D/C quadrature sum. No
    # continuum profile, physical frequency or cutoff is selected by this test.
    epsilon = F(pair["epsilon"])
    u0 = [row[0] for row in u]
    fock = {(0,0):F(1),(1,0):F(1),(0,1):F(1)}
    fock_norm = sum(x*x for x in fock.values())
    photon_expectation = sum(sum(occupations)*amp*amp for occupations,amp in fock.items())/fock_norm
    check("core_Fock_raw_norm",fock_norm,3)
    check("one_shared_photon_energy_in_two_modes",photon_expectation,F(2,3))

    def completed_square(phi, values):
        raw = 0
        for mode,prefix in enumerate(("D","C")):
            y0 = [row[0] for row in images[prefix+"13"]]
            y1 = [row[0] for row in images[prefix+"12"]]
            y2 = [row[0] for row in images[prefix+"23"]]
            for p,pc in enumerate(phi):
                if not pc:
                    continue
                inc1,inc2 = values(p)
                for photons,fc in fock.items():
                    upper = list(photons)
                    upper[mode] += 1
                    # Occupation is at most one in this chosen core vector.
                    ann = fock.get(tuple(upper),0)
                    for c in range(64):
                        amp = pc*(ann*u0[c] + epsilon*fc*(y0[c]+inc1*y1[c]+inc2*y2[c]))
                        raw += amp.conjugate()*amp
        return real(raw)/(norm2(phi)*norm2(u0)*fock_norm)

    direct_squares = {}
    for name,prep in preparations.items():
        phi,means = prep["raw"],prep["means"]
        full = completed_square(phi,lambda p:(p1[p][p],p2[p][p]))
        mean = completed_square(phi,lambda p:tuple(means))
        cov_entry = contraction(prep["covariance"],dblocks)[0][0]
        check(name+"_coordinate_full_square_identity", full-mean,2*epsilon**2*cov_entry)
        direct_squares[name] = {"full":full,"mean_replacement":mean,
                               "difference":full-mean,
                               "covariance_two_quadrature_rhs":2*epsilon**2*cov_entry,
                               "normalization":norm2(phi)*norm2(u0)*fock_norm,
                               "photon_energy_counted_once":photon_expectation}

    # Arbitrary complex profile Gram, retaining both mixed orders. These
    # alternate Grams are declared counterexamples to a universal ratio only.
    profile_examples = {}
    for name,gamma in {
        "common_equal": [[1,1],[1,1]],
        "orthogonal_changed_hypothesis": [[1,0],[0,1]],
        "opposite_phase_changed_hypothesis": [[1,-1],[-1,1]],
        "complex_changed_hypothesis": [[1,I/F(2)],[-I/F(2),1]],
    }.items():
        vp,vm = contraction(plus,dblocks,gamma),contraction(minus,dblocks,gamma)
        profile_examples[name] = {"profile_Gram":gamma,"correlated":vp,
                                   "anticorrelated":vm,
                                   "e0_ratio":vm[0][0]/vp[0][0]}
    check("orthogonal_profile_ratio_is_one", profile_examples["orthogonal_changed_hypothesis"]["e0_ratio"],1)
    check("opposite_phase_profile_ratio_is_one_third",profile_examples["opposite_phase_changed_hypothesis"]["e0_ratio"],F(1,3))

    # Registered entangled control, using first two actual U columns and the
    # actual 00/11 placement sectors. No search for a favourable state occurs.
    u1 = [row[1] for row in u]
    check("entangled_branch_internal_orthogonality",dot(u0,u1),0)
    on0 = [x+y for x,y in zip([r[0] for r in images["D12"]],[r[0] for r in images["D23"]])]
    on1 = [x+y for x,y in zip([r[1] for r in images["D12"]],[r[1] for r in images["D23"]])]
    onnorms = [norm2(on0)/norm2(u0),norm2(on1)/norm2(u1)]
    actual_joint = onnorms[1]/2
    factorized_joint = sum(onnorms)/4
    same_state_mean_square = sum(onnorms)/8
    actual_difference = actual_joint-same_state_mean_square
    false_covariance_product = sum(onnorms)/8
    entangled_defect = actual_difference-false_covariance_product
    conditioned_joint = F(1,2)*0 + F(1,2)*onnorms[1]
    check("entangled_conditioned_sector_identity",actual_joint,conditioned_joint)
    check("entangled_product_mutation_exposed",bool(entangled_defect),True)
    entangled = {
        "raw_state": "e_0 tensor U[:,0] + e_18 tensor U[:,1] on placement64 tensor colour64",
        "raw_norm_squared":norm2(u0)+norm2(u1),
        "normalized_state": "raw/sqrt(12), photon vacuum; D coefficient reported",
        "sector_weights":[F(1,2),F(1,2)],"sector_labels":[[0,0],[1,1]],
        "conditioned_internal_states":["U[:,0]/sqrt(6)","U[:,1]/sqrt(6)"],
        "placement_reduced_purity":F(1,2),"means":[F(1,2),F(1,2)],
        "on_sector_current_norms":onnorms,
        "joint_current_square":actual_joint,
        "conditioned_sector_square":conditioned_joint,
        "factorized_same_marginals_square":factorized_joint,
        "joint_factorization_defect":actual_joint-factorized_joint,
        "same_entangled_state_scalar_mean_square":same_state_mean_square,
        "actual_full_minus_mean":actual_difference,
        "false_product_covariance_rhs":false_covariance_product,
        "false_covariance_defect":entangled_defect,
        "two_physical_quadratures": "D and C each give this coefficient on the actual U sectors; sum doubles it",
    }
    write_json(out / "ENTANGLED_CONTROL.json",entangled)

    # Registered loss of one complex mixed order, on actual D12 and C23.
    dcblocks = [[blocks[0][0],blocks[0][3]],[blocks[3][0],blocks[3][3]]]
    dc_complete = contraction(plus,dcblocks)
    dc_missing_21 = sub(dc_complete,scale(dcblocks[1][0],plus[1][0]))
    complex_defect = sub(dc_missing_21,dc_complete)
    check("actual_D_C_cross_is_nonzero_imaginary",bool(QC.cast(dcblocks[0][1][0][0]).im),True)
    check("complete_D_C_payment_is_Hermitian",dc_complete,dagger(dc_complete))
    check("one_order_omission_not_Hermitian",dc_missing_21==dagger(dc_missing_21),False)
    dc_complex_profile = contraction(plus,dcblocks,[[1,I/F(2)],[-I/F(2),1]])
    check("complex_profile_both_orders_real_contribution",dc_complex_profile,scale(m,F(5,8)))

    # Additional ordered-covariance test: noncommuting full64 projections do
    # not possess joint sectors, but the ordered product identity survives.
    qnc = zeros(64)
    for a in (0,16):
        for b in (0,16):
            qnc[a][b]=F(1,2)
    phinc = [QC(0) for _ in range(64)]
    phinc[0],phinc[16]=QC(1),I
    nc_ops = [p1,qnc]
    nc_means = [expect(phinc,p) for p in nc_ops]
    nc_cov = [[expect(phinc,mm(a,b))-nc_means[i]*nc_means[j]
               for j,b in enumerate(nc_ops)] for i,a in enumerate(nc_ops)]
    nc_rhs = contraction(nc_cov,dcblocks)[0][0]
    x1,x2 = mv(p1,phinc),mv(qnc,phinc)
    y1 = [r[0] for r in images["D12"]]
    y2 = [r[0] for r in images["C23"]]
    direct_nc = [x1[p]*y1[c]+x2[p]*y2[c] for p in range(64) for c in range(64)]
    mean_nc = [nc_means[0]*y1[c]+nc_means[1]*y2[c] for c in range(64)]
    nc_difference = norm2(direct_nc)/(norm2(phinc)*norm2(u0))-norm2(mean_nc)/norm2(u0)
    check("noncommuting_Q_is_projection",mm(qnc,qnc),qnc)
    check("noncommuting_ordered_covariance_identity",nc_difference,nc_rhs)
    check("noncommuting_actual_commutator_entry",sub(mm(p1,qnc),mm(qnc,p1))[0][16],F(-1,2))
    noncommuting = {"incidence_1":"actual P1", "incidence_2":"Q=|e0+e16><e0+e16|/2",
                   "raw_placement":"e0+i e16", "covariance":nc_cov,
                   "current_order":["D12","C23"],"difference":nc_difference,
                   "ordered_covariance_rhs":nc_rhs,"joint_sector_available":False}

    shared_ct = scale(m,F(1,2))
    independent_ct = m
    controls = {
        "scalar_mean_only": {
            "outcome":"FAIL_FIELD_IDENTITY",
            "omitted_correlated_matrix":vplus,
            "e0_omission":vplus[0][0],
            "witness_nonzero":bool(vplus[0][0]),
        },
        "diagonal_covariance_only": {
            "outcome":"FAIL_JOINT_PAYMENT",
            "mutated_correlated_and_anticorrelated":vdiag,
            "mutated_minus_correct_correlated":sub(vdiag,vplus),
            "mutated_minus_correct_anticorrelated":sub(vdiag,vminus),
            "witness_nonzero":bool((sub(vdiag,vplus))[0][0]),
        },
        "wrong_source_norm": {
            "outcome":"FAIL_NORMALIZED_GRAM",
            "correct_M":m,"normalization_omitted":scale(m,6),
            "normalization_applied_twice":scale(m,F(1,6)),
            "omitted_e0_defect":5*m[0][0],
            "twice_e0_defect":F(-5,6)*m[0][0],
            "witness_nonzero":bool(m[0][0]),
        },
        "independent_fields_substitution": {
            "outcome":"FAIL_HAMILTONIAN_TRANSFER",
            "shared_correlated_full_current_square":shared_ct,
            "independent_correlated_full_current_square":independent_ct,
            "shared_mixed_counterterm":sub(shared_ct,independent_ct),
            "shared_variance":vplus,"independent_variance":vdiag,
            "additional_defect":"Adding completed single-source Hamiltonians also repeats the original photon-energy term",
            "witness_nonzero":bool((sub(shared_ct,independent_ct))[0][0]),
        },
        "entangled_product_factorization": {
            "outcome":"FAIL_PRODUCT_HYPOTHESIS",
            "joint_factorization_defect":actual_joint-factorized_joint,
            "full_minus_mean_defect":entangled_defect,
            "conditioned_identity_residual":actual_joint-conditioned_joint,
            "witness_nonzero":bool(entangled_defect),
        },
        "omit_complex_mixed_order": {
            "outcome":"FAIL_HERMITIAN_PAYMENT",
            "actual_D12_C23_ordered_Gram":dcblocks,
            "complete":dc_complete,"omit_21":dc_missing_21,
            "omission_defect":complex_defect,
            "e0_imaginary_defect":QC.cast(complex_defect[0][0]).im,
            "complex_profile_complete":dc_complex_profile,
            "witness_nonzero":bool(QC.cast(complex_defect[0][0]).im),
        },
    }
    check("all_six_registered_mutations_have_nonzero_witnesses",all(c["witness_nonzero"] for c in controls.values()),True)
    write_json(out / "CONTROLS.json",controls)
    write_json(out / "FIELD_COEFFICIENTS.json",{
        "M":m,"correlated":vplus,"anticorrelated":vminus,
        "two_quadrature_correlated":scale(vplus,2),
        "two_quadrature_anticorrelated":scale(vminus,2),
        "direct_completed_squares":direct_squares,
        "inherited_epsilon":epsilon,
        "profile_formula_D_D":{
            "correlated":"M*(Gamma11+Gamma22-Re(Gamma12))/4",
            "anticorrelated":"M*(Gamma11+Gamma22+Re(Gamma12))/4",
            "assumption":"Gamma21=conjugate(Gamma12); scalar external profiles; general operator-valued profiles stay inside chi expectation",
        },
        "profile_examples":profile_examples,
        "noncommuting_ordered_covariance_example":noncommuting,
        "coefficient_only":True,"physical_payment_computed":False,
    })
    # Large matrices stay in their operand artifacts, while every check is
    # still exact and retained. This is a mathematical reconstruction audit,
    # not a floating point agreement test or an external verification claim.
    write_json(out / "CHECKS.json",checks)
    passed = all(c["passed"] for c in checks)
    result = {
        "verdict":"HELD" if passed else "BROKE",
        "completed_utc":utc(),"case":"02_shared_field_covariance",
        "checks_total":len(checks),"checks_passed":sum(c["passed"] for c in checks),
        "failed_check_ids":[c["id"] for c in checks if not c["passed"]],
        "fixed_input_hashes_authenticated":len(custody),
        "M":m,"M_leading_principal_minors":minors,
        "correlated_e0":vplus[0][0],"anticorrelated_e0":vminus[0][0],
        "factor_three_scope":"Actual normalized D-current coefficient, common equal profile weight; both physical quadratures double both coefficients",
        "registered_controls":{name:{"outcome":c["outcome"],"witness_nonzero":c["witness_nonzero"]}
                               for name,c in controls.items()},
        "entangled_defect":entangled_defect,
        "complex_order_e0_defect":QC.cast(complex_defect[0][0]).im,
        "proof_required_in_REPORT":True,"script_sha256":script_sha,
        "independence":"I1: same inherited model, newly authored separate proof/code; no external verification",
        "program_fields_consumed":False,"new_Duck_or_model_service":False,
        "director_approval":False,"physical_binding_or_profile_selection":False,
    }
    write_json(out / "RESULTS.json",result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case",required=True,type=Path)
    parser.add_argument("--preregistration",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("--output must be a fresh, nonexistent directory")
    args.output.mkdir(parents=True,exist_ok=False)
    write_json(args.output / "RUN_START.json",{
        "started_utc":utc(),"command":sys.argv,"python":sys.version,
        "script_sha256":digest(__file__),"case":str(args.case.resolve()),
        "preregistration":str(args.preregistration.resolve()),
    })
    try:
        result = main(args,args.output)
        write_json(args.output / "RUN_STATUS.json",{
            "finished_utc":utc(),"execution":"COMPLETE",
            "verdict":result["verdict"],"checks_passed":result["checks_passed"],
            "checks_total":result["checks_total"],
        })
        print(json.dumps({k:result[k] for k in ("verdict","checks_total","checks_passed","failed_check_ids")},sort_keys=True))
        sys.exit(0 if result["verdict"] == "HELD" else 2)
    except Exception as exc:
        write_json(args.output / "RUN_STATUS.json",{
            "finished_utc":utc(),"execution":"FAILED",
            "exception":repr(exc),"traceback":traceback.format_exc(),
        })
        traceback.print_exc()
        sys.exit(1)
