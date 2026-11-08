# Complete retained-trial payment — blind reconstruction A

The complete intrinsic-recipient upper certifies a conditional interval for each of the four retained `mR=1000000` lanes. It certifies no interval for the eight `mR=100` or `1000` controls. The positive crossing-gate recipient certifies no interval with this family and upper. Tau is left as a mathematical variable throughout. A noncertifying upper is not a lower bound on the trial or ground energy.

The calculation gives a **rigorous complete upper**, together with separate normalized enclosures for `F_full` and `C_cross`; it does not claim exact continuum values for those two expectations. All new numbers are generated in `RESULTS.json` and the append-only native/replay result directories. Exact rational strings, including endpoint brackets and all twelve payment rows, are authoritative; compact scientific notation in the tables below is rounded for reading.

## Frozen trial and reference

The trial is exactly the frozen product `phi_tau tensor chi_i`. The placement factor is the normalized full192 ground family of `tau H192-epsilon P192`, with all144 complementary placement directions retained. `P=J J^T` uses the literal connected receiving isometry. The source factor is the original normalized common eigenlane `u_i=U v_i/sqrt(6)` with `G4 v_i=g_i v_i`. For each unchanged mass and lane,

```
T0_i = u_i tensor vacuum,
T1_i = - integral h_R(omega)/(omega+Delta) A_full u_i one_boson,
chi_i = Gaussian tensor (T0_i+epsilon T1_i)/sqrt(D_i)
        tensor independent matched normal EDGE,
D_i = 1+epsilon^2 n_i g_i,
Delta=3epsilon, epsilon=1/573049, 0<=n_i<=3bU, bU=5/72.
```

The original Gaussian has Cartesian relative-position variance `ell^2`, `ell=R=1`, zero mean separation, and the whole massive COM/recoil form. The source control is `j=1, mu=nu=0`; mass controls are `100,1000,1000000`. The original normal EDGE has affine mean `1/2`, `zeta=1`, full gate variance `2`, and `gamma=1/10000000`. The changed signed ledger is the explicitly frozen zero chart. No new source, amplitude, packet width, gate, mass, field profile, or Fock truncation is selected.

The intrinsic recipient has `epsilon S23+epsilon P tensor S12`, complete `Hf(A_internal+P A_cross)`, placement hopping and the unchanged motion/EDGE/localized-gate terms. The comparison is to the **fragment lower** `12tau-epsilon+L_common`, with `L_common=0` in this chart. It is the valid whole-field completed-square lower. The retained free variational upper is not used as that lower.

The field profile remains `|h_R|^2=2 omega j2(omega R)^2/((4/5)pi)` on all positive frequencies, with the original full five-STF angular contraction and both physical helicities before incidence. The sharp UV tail, self and mixed counterterms, source complements, and unused full-Fock sectors remain present. The divergent sharp quadratic derivative moment is never assigned a finite nonrelativistic value.

## Full source reconstruction and separate field payments

The native real source currents are `D12,D23,R12,R23`, with physical Hermitian second quadrature `iR`. The literal full64 matrices establish

```
G12 = D12^T D12+R12^T R12 >=0,
G23 = D23^T D23+R23^T R23 >=0,
Gsep = G12+G23,
Tr(G12)=88498176, Tr(Gsep)=176996352,
U^T U=6I, U^T G12 U/6=U^T G23 U/6=G4.
```

All64 intermediates are retained. `R12 U=D12 U`, `R23 U=D23 U`; writing `X12=D12 U`, `X23=D23 U`, the exact contact Grams are `X12^T X12/6=X23^T X23/6=G4/2` and `X12^T X23/6=-G4/4`. Each current image has `Hex X=0`, while `Hex U=-3U`. Each exchange is a symmetric involution, so `I+S_ab` is positive. Native attempt003 checks these facts by sums of positive defect Grams and exact zero equality, in addition to the independent replay's individual checks.

Let `c,q,n` denote the actual original Gaussian-averaged continuum contractions, with `p_k=c-q=2F-Fcross`, `n=partial_Delta p_k`, and `q-Delta n` the free-photon moment. These symbols are continuum expectations on the original trial, not scalar static substitutions. Let `C1_full=<T1|CT_full_without_epsilon^2|T1>` and define `C1_int` similarly. Photon parity gives the exact normalized identities

```
F_full = [epsilon^2 g (p_k-Delta*n)+epsilon^4 C1_full]/D,
F_int  = [epsilon^2 g (mu0-Delta*n)+epsilon^4 C1_int]/D,
mu0=1/4.
```

The first identity follows by summing the complete vacuum CT `epsilon^2 c g`, linear drive `-2epsilon^2 q g`, and free-photon term `epsilon^2(q-Delta*n)g`. The identical two contact self-Grams and their signed cross Gram give half of the total linear drive for the internal contact. Its vacuum CT is `epsilon^2 mu0 g`. The one-boson CT terms remain separate and positive.

For the **quadratic crossing self-counterterm**, the same normalized trial gives

```
C_cross = epsilon^2 mu0 [g+epsilon^2 M12]/D,
M12=<T1|G12|T1>, 0<=M12<=Tr(G12)*n*g.
```

This is a new contraction of the actual quadratic operator `G12`. It is not the old quartic CT column. With `gL<=g<=gU`, `nmax=3bU`, valid enclosures are

```
0 <= F_full <= epsilon^2*gU*3*Delta^2/42
              +2epsilon^4*mu0*Tr(Gsep)*nmax*gU,
epsilon^2*mu0*gL/(1+epsilon^2*nmax*gL) <= C_cross
  <= epsilon^2*mu0*gU*(1+epsilon^2*Tr(G12)*nmax).
```

The field bound uses positivity of the complete square and
`0<=p_k-Delta*n<=3Delta^2 b3`, `b3=R/42`. This is the convergent inverse-moment inequality on the entire original profile. The full TT/contact Gram bounds `0<=CT_full<=2mu0 Gsep` and `0<=CT_int<=mu0 G23` give `C1_full,C1_int<=2mu0 Tr(Gsep)n g`. They retain mixed channels through a whole positive operator inequality, rather than assigning a sign to an individual mixed term. The norm in every exact identity is the same `D`; its bounds are applied only after the numerator's sign is known.

These field/self enclosures are independent of the mass control; every mass repeats its lane's enclosure. All twelve copies and actual norm upper bounds are in `RESULTS.json`.

| Lane | F_full upper, approximately | C_cross enclosure, rounded display |
| --- | ---: | --- |
| 0 | 2.19657609896E-12 | [9.78085181925E-9, 9.78140104297E-9] |
| 1 | 4.36746827045E-10 | [1.94473076159E-6, 1.94484309994E-6] |
| 2 | 4.20133295298E-10 | [1.87075473274E-6, 1.87086268250E-6] |
| 3 | 4.01818918814E-10 | [1.78920524408E-6, 1.78930836652E-6] |

## Exact incidence and positive source promotion

Write `rho=<phi_tau|P|phi_tau>`. Since `P` is a projection and commutes with the other factors, the exact field expectation on the product is

```
F_P = rho F_full+(1-rho)F_int
    = {epsilon^2*g[rho*p_k+(1-rho)*mu0-Delta*n]
       +epsilon^4[rho*C1_full+(1-rho)*C1_int]}/D.
```

For comparison, replacing the operator incidence by its mean gives a different field. The exact difference is

```
F_P - <Hf(A_internal+rho*A_cross)> = rho(1-rho) C_cross.
```

`C_cross` has a strictly positive lower enclosure in every lane. For finite positive tau the retained ground family has `1/4<rho<1`, so the variance payment is nonzero. Replay retains explicit algebra controls and variance-payment enclosures; no scalar mean substitution enters the bound.

The intrinsic source expectation is exactly `-epsilon(1+rho)` plus the normalized positive one-boson promotion

```
R_src(rho) = epsilon^3/D *
 <T1| (I+S23)+rho*(I+S12) |T1>.
```

On the **full source**, positivity gives
`(I+S23)+rho(I+S12) <= (I+S12)+(I+S23)+(I+S13)=Hex+3I`.
On the actual retained current images this yields
`0<=R_src(rho)<=3epsilon^3 n g/D=epsilon^2 Delta n g/D`.
Thus the signed `-Delta*n` in the field is canceled only against a proved upper for the actual source promotion. It is not discarded or hidden in a changed reference. At connected support, this comparison is the full-source identity transfer from the old `Hex` paid account to the intrinsic path account; `I+S13` supplies its positive remainder.

## Complete signed payment and normalization

The frozen paid kernel satisfies
`p_k<=pU=2Delta*bU-Fcross_lower`, with the actual `Fcross_lower` and original whole-spectrum massive majorants from the frozen input rows. Set `K=3/(4m)`. After the preceding exact decomposition and source comparison, the complete positive numerator is bounded by

```
A_i+B_i(1-rho),
A_i=K+3epsilon^2 bU K gU + epsilon^2 pU gU
    +3epsilon^2 M_upper gU +6epsilon^4 mu0 Tr(Gsep)bU gU
    +4gamma chi_upper +(45/2)gamma epsilon^2 bU gU,
B_i=epsilon^2 gU (mu0-pU)>0.
```

This includes packet kinetic, dressed packet kinetic, signed self/cross paid field/source response, whole massive photon recoil including COM, full quartic CT on the one-boson source image, vacuum gate and dressed gate. The actual normal EDGE covariance and gate cross terms enter the retained `chi_upper` and dressed-gate payment. The full positive one-boson CT allowance is uniform in `rho`, so the same coarse allowance pays the internal/full mixture.

Each of the eight signed components and their sum was reconstructed coefficientwise from the owning definitions, evaluated natively, and enclosed by its corresponding original paid matrix entry. In particular, `epsilon^2 pU gU` is the sum of the positive self column and the **negative** actual cross column. The negative column is not divided out of an aggregate bound. `Pold=A_i` reproduces the old complete connected-support upper at `rho=1`.

The numerator above is positive; hence using `D>=1` gives the normalized energy upper `A_i+B_i(1-rho)`. The old `A_i` already used this legitimate `Dmin=1` payment bound. It is never divided by `D` again. All exact field identities, source promotion and CT inequalities first use the actual same full Gram.

For the supplied placement ground, `tau(<H>-12)=epsilon*rho-delta`. The intrinsic source baseline therefore cancels the `epsilon*rho` exactly. Against the fragment **lower**, the final sufficient upper is

```
U_i-L_frag <= f_i(tau)
             = -delta(tau)+A_i+B_i(1-rho(tau)).
```

This bound is direct and complete. It need not sum separate worst-case `F_full` and `C_cross` enclosures, because doing so would lose the proved signed source/field cancellation.

## All twelve controls and conditional intervals

| Row | mR | Lane | A_i, approximately | B_i, approximately | Intrinsic tau_star, approximately; certificate 0<tau<tau_star |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 100 | 0 | 7.50012561401E-3 | 9.78082431246E-9 | none |
| 1 | 100 | 1 | 7.50285037195E-3 | 1.94472842820E-6 | none |
| 2 | 100 | 2 | 7.50274620021E-3 | 1.87075237278E-6 | none |
| 3 | 100 | 3 | 7.50263136368E-3 | 1.78920286540E-6 | none |
| 4 | 1000 | 0 | 7.50113333426E-4 | 9.78082431246E-9 | none |
| 5 | 1000 | 1 | 7.50408614495E-4 | 1.94472842820E-6 | none |
| 6 | 1000 | 2 | 7.50397325441E-4 | 1.87075237278E-6 | none |
| 7 | 1000 | 3 | 7.50384880646E-4 | 1.78920286540E-6 | none |
| 8 | 1000000 | 0 | 8.61844889900E-7 | 9.78082431246E-9 | 2.52997992945E-7 |
| 9 | 1000000 | 1 | 8.62647792206E-7 | 1.94472842820E-6 | 1.46873493961E-7 |
| 10 | 1000000 | 2 | 8.62617096003E-7 | 1.87075237278E-6 | 1.48491876817E-7 |
| 11 | 1000000 | 3 | 8.62583257212E-7 | 1.78920286540E-6 | 1.50353801227E-7 |

No physical tau is selected. Exact endpoint enclosures for the successful rows are:

| Lane, mR=1000000 | Outward decimal enclosure of tau_star |
| --- | --- |
| 0 | [2.529979929446277943743963518E-7, 2.529979929446277943743963519E-7] |
| 1 | [1.468734939606523193555693997E-7, 1.468734939606523193555693998E-7] |
| 2 | [1.484918768174176292192350521E-7, 1.484918768174176292192350522E-7] |
| 3 | [1.503538012274039180872957056E-7, 1.503538012274039180872957057E-7] |

The eight lighter controls have `A_i>=epsilon`, already nonnegative at the connected-support limit. For these rows the displayed complete upper is nonnegative for all tau. This gives no energy lower bound and no exclusion of a better bound on the same trial.

For reproducibility and a proof that the successful intervals have one endpoint, use the conditional variable `r=4tau/delta`, with `a_k=1/(1+kr)`, `S=sum a_k`, `T=sum a_k^2`, `U=sum a_k^3`. Then

```
delta=epsilon S/4, rho=S^2/(4T), tau=epsilon*r*S/16,
dtau/dr=epsilon T/16>0,
drho/dr = S*(T^2-S*U)/(2r*T^2)<=0  (r>0).
```

The last inequality is Cauchy-Schwarz. Delta decreases strictly, so `f_i` increases strictly. Its limits are `A_i-epsilon` and `A_i+3B_i/4-epsilon/4`. Each successful row has opposite endpoint signs; exact rational bisection brackets its unique root. Replay also checks the literal full192 H/J, all placement complements and the symmetric spectral weights underlying this supplied ground family, plus exact Sturm root counts for the four G4 eigenlane intervals.

The **positive crossing-gate** term is `epsilon P tensor(I+S12)` and adds its mandatory normalized identity baseline `epsilon*rho`. Its sufficient upper becomes

```
f_gate=-delta+epsilon*rho+A_i+B_i(1-rho)
      =tau(<H>-12)+A_i+B_i(1-rho)>0.
```

No interval is certified for any of the twelve positive-gate controls. This is the actual baseline difference, counted once. The intrinsic and positive-gate recipients have not been identified with each other.

## Execution, replay and scope

The qualified unchanged runtime is `ironclad-235-source-clock-20261105T181633Z`, with its `.venv/bin/python`, core `0.11.3`, and native `SLC-GEN5-R1`. Actual source-bound native execution consists of twelve `GEN3_SOURCE_OPERATOR_WORD` calls in three append-only attempts. Every job carries the exact capsule source binding, hashed sources, a nonempty objective, explicit operation program and checks. All three receipts are `PASSED`; original sources and runtime code were read-only.

- `native/A/attempt_001`: full64 `G12,G23,Gsep`, native bit-twirl traces, source G4 and initial source defects.
- `native/A/attempt_002`: all156 exact coefficients in the twelve-by-thirteen complete-payment table.
- `native/A/attempt_003`: strict positive source defect-Gram sums and literal G4 semantic equality checks.

`SOURCE_OPERATION_MAP.json` identifies the exact input paths, hashes, payloads, outputs and analytic transfers. Capability selection used the frozen installed menu and supplied contracts. Exact source words directly fit the full64 operands. The advertised recoil operation has a different moment contract; the sharp continuum is retained through the owning inverse-moment/whole-frequency inequalities rather than represented as a finite quadrature or a native arithmetic claim.

`replay.py` uses only Python3's standard library, exact `fractions.Fraction`, and decimal display rounding. It reconstructs source matrices and source identities, full192 placement checks, eigenlane Sturm enclosures, every new payment coefficient, separate field/self enclosures, variance controls and endpoint brackets from frozen public inputs. It has no engine imports. An optional native directory only compares retained native results against these independently reconstructed values. `replay_002` passes all native comparisons; a fresh `replay_003_engine_free` using only frozen public inputs reproduces the complete mathematical result exactly.

```
python3 -B replay.py --case /path/to/01_complete_payment --out /new/output/directory
```

All output directories must be new. All discovered failures and display/proof corrections remain in `NOTES.md`, `RESULTS.json`, old replay outputs and versioned source; no failed/corrected attempt was overwritten. No timed Duck window, external peer, fit, source/engine change, manuscript edit or publication occurred.

This was a blind reconstruction A from frozen owning definitions. B, other learner scratch/reports and prior A1 field-payment solutions were not read. Agreement between native arithmetic and this separately arranged replay is same-model computational agreement, not external verification.

No mathematical operand is missing for this conservative complete upper. Exact continuum `n` and more precise full/mixed one-boson CT contractions would sharpen the separate enclosures and intervals without changing the trial. The unassigned physical source/colour/species, action/ruler and tau mapping remain receiving inputs, as do any subsequently changed signed common-reference or formation-work ledgers. The present zero-changed-ledger comparison makes no nuclear mass/radius assignment or binding fit.

The bounded closing spin read contributed the methodological reminder to preserve a whole mixed Gram and its signed entries before bounding it; that structure is already used here. No spin operand enters the new numbers. No additional potentially helpful source fact was uncovered beyond the complete payment, variance term, recipient baseline difference and explicit sharpening operands reported above.

NEGATIVE DRIFT CHECK — COMPLETION: CLEAR.
