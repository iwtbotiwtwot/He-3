# CR2 shared field covariance: HELD

No frozen target assertion failed. All six deliberately false mutations failed with exact nonzero witnesses, listed first below. The final separately authored replay passed **108/108 exact checks** and authenticated all **25 FREEZE-listed files**. The only operational failure was a read-only `python` preflight on a system providing `python3`. An unexecuted draft's possible integer-to-float elimination was corrected and retained before preregistration. Neither required a change to the mathematical statement or source normalization.

The result is **HELD**, at independence level **I1**: the same inherited model, a separate proof reconstruction, and new standard-library exact code. No previous executable, generator, replay, or native-program logic was read or run. This is not external verification. No physical current/profile selection or complete physical field payment is asserted.

## Failures exposed by the registered controls

Every number in this table is an exact normalized **D-current coefficient**, with the common unit profile weight and the source lane `U[:,0]/sqrt(6)`, unless the row names a different fixed witness. Multiplication by the inherited `epsilon^2` and a declared profile weight occurs only when forming the corresponding field term. The two original physical quadratures double the common-profile D-only coefficients.

| Mutation | Actual nonzero witness | Registered outcome |
|---|---|---|
| Replace incidences by scalar means and omit covariance | Correlated coefficient omitted: `922592/3 > 0` | `FAIL_FIELD_IDENTITY` |
| Delete offdiagonal covariance | Both mutated coefficients become `1845184/3`; mutated-minus-correct is `+922592/3` for correlated and `-922592/3` for anticorrelated | `FAIL_JOINT_PAYMENT` |
| Omit / twice apply the source-frame normalization | Correct `M` becomes `6M` / `M/6`. Lane-zero defects are `18451840/3` / `-9225920/9` | `FAIL_NORMALIZED_GRAM` |
| Replace the shared field by independent fields | The actual correlated full-current square is `1845184/3`; the independent self-only value is `3690368/3`. Lost shared mixed term: `-1845184/3` | `FAIL_HAMILTONIAN_TRANSFER` |
| Factor placement/internal expectations in the fixed entangled state | Exact joint-minus-product defect `-1600/3`; the conditioned-sector residual is exactly zero | `FAIL_PRODUCT_HYPOTHESIS` |
| Drop ordered mixed term 21 for actual `D12,C23` | Omitted-term defect is `-i*461296/3`; the mutated payment is not Hermitian | `FAIL_HERMITIAN_PAYMENT` |

Adding individual completed field Hamiltonians also duplicates their original photon-energy term. The nonzero mixed defect above already disproves that Hamiltonian transfer without relying on photon duplication. Complete matrices and both ordered terms are in `attempts/run_v002/CONTROLS.json`.

## Independent reconstruction of the placement operands

The owning source is `sources/light/HE3_INDEPENDENT_FRAGMENTS.json`, with the placement code list supplied by `HE3_PLACEMENT.json`. Primary row `(x,y,z)` carries the singleton address in cell A and the oriented PN pair `(y,z)` in cell B. Equal local digits across those cells are allowed. The retained literal code is `64x+8y+z`.

The new code reconstructs every entry from the source rule:

\[
H_{192}=\bigoplus_{24}h,\qquad h=18I_8-2A_{\rm cube}
                 =(6I_8-2A_{\rm cube})+12I_8.
\]

The reconstructed matrix equals the raw `full_source_H` exactly. A receiver column is the coordinate injection for its original connected placement code; the resulting `J192` equals the raw owning receiver, and `J192^T J192=I48`. All 24 oriented-pair fibres retain eight singleton addresses. Each receiver selects two vertices at cube distance two.

The declared witness uses two disjoint tagged copies of the first complete fibre: primary indices `0,...,7`, oriented pair `(0,1)`, and original receiving columns `12,24`. Its local receiver is

\[
J_8=(e_2,e_4),\quad P_8=J_8J_8^T,
\quad H_{64}=h\otimes I_8+I_8\otimes h,
\quad J_{64}=J_8\otimes J_8.
\]

Tensor index `8x+y` is retained. Define `P1=P8 tensor I8`, `P2=I8 tensor P8`. Both are commuting orthogonal projections; `P1 P2=J64 J64^T`. The complete 64-dimensional placement fibre has receiver dimension 4 and complementary dimension 60. It occurs with multiplicity `24^2=576` in the full `192^2=36864` tensor parent. This multiplicity and the complete local complement are retained; no energy-convolution quotient is substituted.

As a check that the complement has not been discarded, its actual complementary drift Gram is

\[
J_{64}^TH_{64}(I-J_{64}J_{64}^T)H_{64}J_{64}
=\begin{pmatrix}24&8&8&0\\8&24&0&8\\8&0&24&8\\0&8&8&24\end{pmatrix},
\]

of rank 4. The eight cube Walsh vectors independently verify the full local spectrum `12+4*popcount(s)`. Thus `24I <= H64 <= 48I`; no `24I` reference shift was applied. These are geometric source energies, not physical free-nucleon or atomic endpoints.

The two supplied raw preparations rebuild as

\[
\phi_+=(e_0+e_{18})/\sqrt2,\qquad
\phi_-=(e_2+e_{16})/\sqrt2.
\]

Both raw squared norms are 2. Their means are `(1/2,1/2)`, their joint second moments are respectively

\[
Q_+=\begin{pmatrix}1/2&1/2\\1/2&1/2\end{pmatrix},\qquad
Q_-=\begin{pmatrix}1/2&0\\0&1/2\end{pmatrix}.
\]

Subtracting the mean outer product gives

\[
C_+=\tfrac14\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
C_-=\tfrac14\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
\]

These were computed from all 64 coordinates and reconstructed projections, rather than imported from the supplied covariance matrices. The generated comparison `TENSOR_TWO_OPERANDS.json` was used only to check the already reconstructed full `H64,J64` and declared fibre metadata.

## Independent full64 colour and signed-current account

The literal source order is `n=a+4b+16c`. For a named pair, the first named slot is fast. Only raw `data.operators` entries are decoded from the colour payload by the replay; its `program` and `output` members are excluded.

From the raw pair matrices, the code checks

\[
D_{16}=Q_{\rm second}-Q_{\rm first},\qquad
R_{16}=-D_{16}S_{16},\qquad C_{16}=iR_{16}.
\]

Here `S16` swaps the pair. `D` and `C` are Hermitian, `R` is real skew, and `D^T D=R^T R`. This retains both original quadratures and the original full-pair self counterterm `2 epsilon^2 D^2 integral |h|^2/omega`. The pair matrices also agree entry by entry with `COMPLETE_DC_PAIR.json`.

The replay independently constructs the alternating pair and triple frames from permutations. The triple columns, in the literal order, are the alternating `(012),(013),(023),(123)` triples. Their actual metric is

\[
U^TU=6I_4,\qquad W=U/\sqrt6,\qquad W^TW=I_4.
\]

Full 64-dimensional embeddings are built for every pair `12,23,13`. All six actual physical currents are retained in the order

`D12, C12=iR12, D23, C23=iR23, D13, C13=iR13`.

Every current image is formed in full dimension before contraction. In particular

\[
R_{ij}U=D_{ij}U,\quad U^TD_{ij}U=U^TC_{ij}U=0,
\quad (I-UU^T/6)J_\alpha U=J_\alpha U.
\]

Thus all current images lie in the retained 60-dimensional source complement. Compressing a current to the four-dimensional floor before squaring would incorrectly produce zero. No such compression enters this audit.

Define, without identifying it with any earlier `G4` or `M4`,

\[
\boxed{M=W^TD_{12}^TD_{12}W=U^TD_{12}^TD_{12}U/6.}
\]

The exact reconstructed matrix is

\[
M=\frac13\begin{pmatrix}
3690368&-107520&0&6400\\
-107520&3683968&16640&107520\\
0&16640&40832&279552\\
6400&107520&279552&3647104
\end{pmatrix}.
\]

Its four leading principal minors are

`3690368/3`, `13583637069824/9`, `553625244315680768/27`,
`959520557272475134590976/81`.

They are all strictly positive. Sylvester's criterion therefore proves `M>0`, with no floating point sign decision. The full signed current Gram obeys

\[
W^TD_{23}^TD_{23}W=W^TD_{13}^TD_{13}W=M,
\quad W^TD_{12}^TD_{23}W=-M/2,
\]

and the `12/13` and `23/13` mixed blocks are `+M/2`. Also `D13=D12+D23` on the complete source, not just on the floor.

For pair order `12,23,13` and quadrature order `D,C`, the complete 24-by-24 block Gram is exactly

\[
\begin{pmatrix}1&-1/2&1/2\\-1/2&1&1/2\\1/2&1/2&1\end{pmatrix}
\otimes\begin{pmatrix}1&i\\-i&1\end{pmatrix}\otimes M.
\]

Its rank is 8, and it is the Gram of full source-current images, hence positive semidefinite. Both signs and both ordered mixed blocks are retained. The helicity convention

\[
H_\pm=(D\pm iC)/\sqrt2
\]

is checked on the full64 operators: the sum of their self Grams equals the sum for `D,C`. On `U`, `H+ U=0`, `H- U=sqrt(2) D U`; the surviving normalized source Gram is `2M`. Reversing a declared helicity convention exchanges the labels and conjugates the corresponding mixed signs; it cannot justify deleting one order.

## Rebuilt covariance proof and common-domain extension

Let `K` contain the complete source, matter and original shared Fock factors. It need not factor further. With photon-mode measure `dmu` including every physical polarization, let

\[
T\chi=\{\sqrt{\omega(k)}a_\lambda(k)\chi\}_{\lambda,k},\qquad
L_i\chi=\{A_{i,\lambda}(k)\chi/\sqrt{\omega(k)}\}_{\lambda,k}.
\]

The original completed field is the quadratic form

\[
q_A[\chi]=\|(T+\epsilon L_A)\chi\|^2.
\]

This displays the photon-energy term once. Expansion gives its linear source terms and **all** ordered `epsilon^2 A_i^dagger A_j/omega` counterterms. A sign change in the displacement convention is absorbed consistently into all amplitudes and does not alter the covariance result.

Take normalized `phi tensor chi`, with placement independent of that complete normalized `chi`. Let the placement incidences be bounded self-adjoint `Pi`, `pi=<phi,Pi phi>`, and `delta Pi=Pi-pi I`. Put

\[
B_{\rm mean}\chi=(T+\epsilon L_0+\epsilon\sum_i p_iL_i)\chi.
\]

The full-square vector is

\[
\phi\otimes B_{\rm mean}\chi
 +\epsilon\sum_i\delta P_i\phi\otimes L_i\chi.
\]

Every cross term with the first vector vanishes because `<phi,delta Pi phi>=0`. Squaring the second vector proves, including both mixed orders,

\[
\boxed{q_{A_0+\sum_iP_i A_i}[\phi\otimes\chi]
 -q_{A_0+\sum_i p_i A_i}[\chi]
=\epsilon^2\sum_{ij}
(\langle P_iP_j\rangle-p_ip_j)
\sum_\lambda\int\frac{\langle\chi,A_{i,\lambda}^\dagger A_{j,\lambda}\chi\rangle}{\omega}\,d\mu.}
\]

The right side is a squared norm and is nonnegative. This derivation does not require `chi` to be a vacuum, an undressed source vector, or a matter/Fock product. It requires the **same** normalized complete `chi` in every contraction.

For the form-domain claim, assume `omega>0` almost everywhere and that each displacement map `Li:K -> direct-integral K` is bounded. A concrete sufficient profile condition for finite bounded currents and bounded unitary translation phases is

\[
\sum_\lambda\int |h_{i,\lambda}(k)|^2/\omega(k)\,d\mu(k)<\infty
\]

for every included current and `A0`. Mixed integrals are then finite by Cauchy-Schwarz. The annihilation map `T` is closed on `D(Hph^(1/2))`; bounded perturbations `T+epsilon L` are closed on that same domain. Their graph norms are equivalent, by `||T psi|| <= ||(T+epsilon L)psi||+|epsilon| ||L|| ||psi||` and its reverse. The positive completed squares therefore are closed forms with a common form domain. A finite-photon form core remains a core after the bounded perturbation. Approximation in this graph norm extends the displayed identity from the core to the whole common domain.

No new ultraviolet/infrared cutoff or physical profile parameter is selected. This identity needs the inverse-first profile moment above. Implementing the shift by a Weyl unitary would separately require the inverse-second moment `integral |h|^2/omega^2`; that implementation is not assumed here. Massive motion, gates, electronic forms, and a particular complete composite trial may require further input. Their membership or payments do not follow from this covariance identity.

As an independent coordinate check of the algebra, the replay uses the original `epsilon=1/573049`, actual full64 colour images, `A0` on pair13, and the exact core Fock vector `|00>+|10>+|01>` in the two quadrature modes. Its raw Fock norm is 3 and its normalized photon energy is `2/3`, counted once. Including the raw placement norm 2 and source norm 6 gives complete norm 36. The directly squared full-minus-mean values are respectively

`1845184/985155469203` and `1845184/328385156401`.

They equal the independently contracted two-quadrature covariance expressions exactly. These finite-mode calculations test the algebra; the common-domain argument above establishes the general form identity. They do not evaluate a continuum physical profile payment.

## Precise factor-three scope and arbitrary complex profiles

For the actual normalized source frame and the declared common equal profile weight, contraction with `C+` and `C-` gives

\[
V_+=M/4,\qquad V_-=3M/4.
\]

On lane zero the coefficients are `922592/3` and `922592`, strictly positive and in the exact ratio 3. Both physical quadratures, or their unitary helicity basis, give twice these values when the same profile contract applies to them.

For arbitrary **scalar external** D-current profiles define the Hermitian profile Gram

\[
\Gamma_{ij}=\sum_\lambda\int
 \overline{h_{i,\lambda}(k)}h_{j,\lambda}(k)/\omega(k)\,d\mu(k).
\]

No mixed order is omitted. With `S=Gamma11+Gamma22` and `z=Gamma12`, the complete D-current matrices become

\[
V_+(\Gamma)=\tfrac14(S-\operatorname{Re}z)M,\qquad
V_-(\Gamma)=\tfrac14(S+\operatorname{Re}z)M.
\]

Thus ratio 3 requires the declared common equal profile contract; it does not survive arbitrary separated/translated profiles. Orthogonal profiles, explicitly a changed hypothesis, give ratio 1. Opposite equal profiles give ratio `1/3`. A complex example with diagonal 1 and `Gamma12=i/2` also gives D-current ratio 1, while its complex phases change a D/C mixed-current payment; both orders there contribute to the real answer.

A useful strengthened coefficient statement follows without a profile fit. Since `Gamma>=0`, `|Re z|<=sqrt(Gamma11 Gamma22)<=S/2`. For `S>0`, the ratio under this separable D-current profile contract lies in `[1/3,3]`. The endpoints require the corresponding equal aligned/opposite profiles. This bound concerns these two source-current coefficients, not a complete field expectation or a physical binding interval.

If translations or profiles are matter operators rather than scalar external functions, their products stay **inside** the common `chi` expectation. The original integrated ordered-Gram formula still applies; pulling out a scalar profile Gram would be an additional factorization hypothesis.

## Entanglement and the correct conditioned account

For commuting projections, write their simultaneous sector projections as `E_sigma`. A general normalized entangled `Psi` has sector weights

\[
w_\sigma=\|(E_\sigma\otimes I)\Psi\|^2.
\]

Let `rho_sigma` be the normalized internal density obtained by tracing the sector state over placement. It can be mixed when a sector has multiplicity; equivalently retain a purification and its sector ancilla. The exact account is

\[
q_{\rm full}[\Psi]
=\sum_\sigma w_\sigma\,
\operatorname{Tr}\rho_\sigma q_{A_0+\sum_i\sigma_i A_i}.
\]

The photon term is counted once because the sector weights sum to 1 and the conditional states carry the actual photon correlations. Replacing all `rho_sigma` by one unconditioned state is unjustified. The scalar-mean square on the same entangled state is instead `sum_sigma w_sigma Tr rho_sigma q_(A0+sum pi Ai)`. Their difference generally includes conditioned linear terms, so the product-state covariance reduction cannot be recovered from placement means and an internal marginal alone.

The exact counterexample uses only actual operands:

\[
\Psi=(e_0\otimes U_0+e_{18}\otimes U_1)/\sqrt{12}.
\]

Both source branches have squared norm 6 and are orthogonal. Placement reduced purity is `1/2`, so the state is genuinely entangled. The sectors are `00,11`, each of weight `1/2`, and the means remain `1/2,1/2`. Take `A0=0`, actual D currents `D12,D23`, and the photon vacuum; report the common-weight coefficient of `epsilon^2`.

The on-sector source norms are `M00=3690368/3` and `M11=3683968/3`. Exact joint and conditioned calculations both give `M11/2=1841984/3`. A product of the same placement and internal marginals gives `(M00+M11)/4=614528`, differing by `-1600/3`. On the same entangled state the scalar-mean square is `307264`; the actual full-minus-mean value is `920192/3`, whereas unjustified covariance factorization predicts `307264`. The defect is again `-1600/3`. Keeping both physical quadratures doubles all these coefficient statements without repairing the factorization.

Commutation belongs to the joint-sector account, not to every covariance formula. The product-state proof above extends to arbitrary bounded self-adjoint incidences if `Cij=<delta Pi delta Pj>` is kept **ordered**; it may be complex. The replay additionally tests actual `P1` against `Q=|e0+e16><e0+e16|/2` on full64 placement, with normalized placement proportional to `e0+i e16`. Their commutator has entry `-1/2`, their covariance has offdiagonals `-i/4,+i/4`, and actual `D12,C23` give the exact positive difference `922592/3`. The ordered covariance identity holds although simultaneous sectors do not exist. A noncommutativity objection alone would therefore be too broad.

## What can be carried into bridge/action work

Bridge construction can use the proved common-domain covariance identity, the reconstructed complete placement incidences, the normalized full64 six-current signed Gram, and the sector-conditioned rule for entangled states. It must carry source complements, both mixed orders, both physical quadratures, common norm, one photon energy, and the original energy reference.

The exact factor-three diagnostic may be used only with its declared common equal profile contract. An arbitrary receiving profile must be inserted into the general ordered Gram. No existing complete He3 trial upper, old paid scalar, or independent-copy field payment was transplanted to this composite source.

Remaining physical input includes a PP/PN/NN-to-colour/current/species receiver, the action/current normalization, physical geometry/profile and ruler/clock law, complete matter/recoil/electronic/gate terms, and connected/fragment/free atomic endpoints computed with the same Hamiltonian and energy zero. This audit selects none of those inputs and supplies no physical binding fit or atomic endpoint.

## Replay and retained evidence

From this verifier directory, choose an output path which does not yet exist:

```sh
python3 replay.py \
  --case /home/lilhelper/SAM_Research_Overflow/Courtroom_II/campaigns/isotope_constructor_checks_20261108/02_shared_field_covariance \
  --preregistration EXECUTION_PREREGISTRATION_V002.json \
  --output attempts/replay_fresh
```

Only the Python standard library is required. The script authenticates its preregistered hash and all fixed inputs before calculation; an existing output directory is refused. `attempts/run_v001` and `attempts/run_v002` remain separate and unchanged. All script versions, execution preregistrations, control matrices, operand matrices, checks, runtime/status receipts, custody records and final hashes are retained. `HYPOTHESES.md` separates rebuilt facts from inherited or unselected input; `NOTES.md` records the complete attempt/correction history. Director approval remains false. No Duck, service/model launch, source optimization, Git/engine/manuscript change, or peer exchange occurred.
