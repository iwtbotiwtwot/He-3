# Independent proof from the frozen operands

All spaces in this audit have the Euclidean coefficient metric. Addresses are the integers 0 through 7, identified with three binary digits; addition of addresses in character formulas means bitwise XOR. All displayed energies are coefficients of one common nonnegative kinetic scale tau when a cost interpretation is made. The matrices themselves are dimensionless and exactly specified.

## 1. One source and the complete free pair

The raw `HE3_PLACEMENT.json/source/actions` contains 48 events. For every directed cube edge there are two events, and every address has six outgoing events. Their endpoint multiplicity matrix is `2 A(Q3)`. The stated source rule therefore gives

`h1 = 6 I8 - 2 A(Q3)`.

The event chirality/displacement values are retained and checked against their raw frame rules. They are not substituted for hopping multiplicities: the frozen hopping operator is the real Laplacian above, while signed response/field terms require their own declared receiver.

For a three-bit mask m define `chi_m(x) = (-1)^(popcount(m & x))`. The eight character vectors have Gram matrix `8 I8`, and

`h1 chi_m = 4 |m| chi_m`.

This proves the complete one-source spectrum: 0, 4, 8, 12 with multiplicities 1, 3, 3, 1. It also proves positivity, without a floating-point eigenvalue computation.

The pair basis is the complete ordered basis `(b,c)`, with address `8b+c`. Its operator is

`H = h1 tensor I8 + I8 tensor h1 = 12 I64 - 2 A(Q6)`.

Every entry is reconstructed by the tensor sum. Six-bit character vectors have Gram `64 I64` and eigenvalues `4k`, where k is the mask weight. The full spectrum is:

| Energy | 0 | 4 | 8 | 12 | 16 | 20 | 24 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Multiplicity | 1 | 6 | 15 | 20 | 15 | 6 | 1 |

The normalized constant vector has all 64 entries `1/8`, norm one, and energy zero. Thus the complete free floor is exactly zero. In particular, `H >= 12 I64` is false: its quadratic form on that vector equals `-12` after subtracting `12 I64`.

## 2. Actual adjacent preparation, metric and drift

Read the ordered pair `(b,c)` from each original independent-cell tuple `(a,b,c)`, retaining the order of first occurrence. This produces the 24 lexicographic oriented cube edges, not a generated injection from a prior report. The original tuple sequence is exactly pair-major and then `a=0..7`.

Define `J e_r = e_(b_r,c_r)`. The addresses are distinct, so `J*J=I24`. Every legal pair has odd relative parity and every one-coordinate hop flips that parity. No one-hop move stays among the adjacent pairs. The diagonal is 12, hence

`J* H J = 12 I24`.

For every complex coefficient vector u, the isometry and quadratic-form identities give

`||Ju||^2 = ||u||^2`,

`<Ju, H Ju> = 12 ||u||^2`.

For normalized supported preparations the energy is exactly `12 tau` above the geometric free floor. This says nothing comparable about arbitrary preparations in the full 64-dimensional parent.

Let Q be the coordinate injection of the other 40 addresses. In the orthonormal `[J,Q]` basis,

`H = [[12 I24, C*], [C,D]]`,

`C = Q* H J`, and `H J - J(12 I24) = Q C`.

These are the actual complement and true drift, with their original signs. For example `H[(0,0),(0,1)] = -2`, so the adjacent space is not invariant. There are 32 omitted addresses with an immediate coupling to the receiving space. The other eight omitted addresses are not thereby dark.

## 3. Analytic rank and cyclic-closure proof

Write `r=b XOR c` and Fourier transform in b. On the character sector s, a vector has the form `chi_s(b) f(r)` and the operator becomes

`H_s = 12 I8 - 4 sum_{j: s_j=0} X_j`,

where `X_j f(r)=f(r XOR e_j)`. The receiving space in every sector is the span of the three coordinate vectors at `r=e_1,e_2,e_3`.

If `w=|s|`, there are `3-w` moving bits and `2^w` disconnected relative cubes. This gives the following finite proof of all rank and cyclic counts. Dimensions in a row are per s; the multiplicity column counts s of that weight.

| w | Number of sectors | Cyclic dimensions through powers 0,1,2,3 | Drift rank | Dark dimension |
|---:|---:|---|---:|---:|
| 0 | 1 | 3, 6, 7, 8 | 3 | 0 |
| 1 | 3 | 3, 5, 6, 6 | 2 | 2 |
| 2 | 3 | 3, 6, 6, 6 | 3 | 2 |
| 3 | 1 | 3, 3, 3, 3 | 0 | 5 |

Here is why each row holds. At w=0, the first images of the three weight-one vertices lie in the four even vertices, with adjacency Gram `I3+2 11*`, which has eigenvalues 7,1,1. A second power supplies the missing odd vertex `111`; a third supplies the remaining even direction because the full odd/even cube adjacency is invertible (it is a permuted `11* - I4`, with eigenvalues 3,-1,-1,-1). At w=1, one Q2 component is reached from one corner, with cyclic dimensions 1,2,3, while the other is reached from two opposite corners, with dimensions 2,3,3. At w=2, the three receiving vertices occupy three different edges; each edge is fully reached in one step. At w=3, the operator is scalar and the three-dimensional receiving space is already invariant.

Summing these rows proves the cyclic dimensions

`24, 42, 46, 47`, then 47 permanently,

and true drift rank `3 + 3*2 + 3*3 = 18`. The new implementation independently computes an exact Krylov basis, retaining the original vector and power/column label for each of its 47 basis vectors.

The same blocks give the drift Gram spectrum

`112 (x1), 64 (x3), 32 (x3), 16 (x11), 0 (x6)`.

For w=0 the Gram block is `16(I3+2 11*)`; for w=1 it is `[32]` direct-sum `32 11*` on two coordinates; for w=2 it is `16I3`; for w=3 it is zero. Thus the drift norm squared is exactly 112 and its kernel has dimension six. The full unnormalized `C*C` is retained in PAIR_MATRICES.json, so no normalized receiving frame is substituted for the source norm.

## 4. Which complement directions are dark?

Let K be the cyclic closure of range(J) under H. It is invariant and contains the receiving space. Since H is self-adjoint, `K_perp` is invariant and lies in the 40-dimensional omitted complement. Conversely, every invariant subspace orthogonal to range(J) is orthogonal to all its H-powers, hence lies in `K_perp`. Therefore the largest invariant dark space has dimension `64-47=17`.

The omitted complement decomposes orthogonally as

`range(Q) = (K intersect range(J)_perp) direct-sum K_perp`,

of dimensions 23 and 17. The first 23 dimensions are dynamically hidden receiving directions; they are not an invariant dark sector. In particular, stopping after the rank-18 first drift would lose five additional reached dimensions.

A separate spectral construction restricts each complete Walsh eigenspace to the 24 receiving coordinates and takes its exact kernel. The ranks and dark multiplicities are:

| Energy | 0 | 4 | 8 | 12 | 16 | 20 | 24 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full multiplicity | 1 | 6 | 15 | 20 | 15 | 6 | 1 |
| Receiving rank | 1 | 6 | 12 | 9 | 12 | 6 | 1 |
| Dark multiplicity | 0 | 0 | 3 | 11 | 3 | 0 | 0 |

This matches the block proof: each weight-two s leaves an unused edge (one dark vector at 8 and one at 16); each weight-one s contributes two dark vectors at 12; weight three contributes five more at 12. The replay retains 17 independent exact dark eigenvectors and checks their zero receiving coordinates, eigen-equations and orthogonality to the exact Krylov basis.

No single omitted coordinate basis vector is dark. The uniform ground vector belongs to K (apply the zero-energy spectral projector polynomial in H to any retained basis vector), and it has nonzero inner product with every coordinate basis vector. The labels of the 40 omitted addresses must therefore not be confused with a basis of the 17-dimensional dark space.

## 5. Exact complement response and resolvent defect

For every `z>0`, positivity of H implies `D+zI>0`. Block elimination gives

`J*(H+zI)^(-1)J = [(12+z)I - Sigma(z)]^(-1)`,

`Sigma(z) = C*(D+zI)^(-1) C`.

The complement component for a receiving solution u is `-(D+zI)^(-1) C u`. The self-energy is positive semidefinite with rank 18, since its kernel equals ker(C). The effective Schur operator is positive definite. Because `(12+z)I` is scalar, the difference between the full receiving resolvent and `I/(12+z)` is positive semidefinite and has rank 18 for every positive z. The six zero directions are exactly the drift-kernel directions.

At the preregistered dimensionless `z=1`, the complete spectral inverse supplies

`[(H+I)^(-1)]_(a,a) = (1/64) sum_{k=0}^6 binom(6,k)/(4k+1) = 11989/116025`.

For the first retained coordinate, the compressed inverse has diagonal `1/13 = 8925/116025`. The retained exact defect is therefore

`3064/116025 > 0`.

The replay proves the full 64-by-24 resolvent solve, equality to the separately formed rational Schur inverse, nonzero complement response and defect rank 18. It retains all matrices, rational inverses and positive rational LDL pivots for `D+I` and the effective operator. Deleting the complement loses both this response and the self-energy; it is not a harmless relabeling.

## 6. Full three-free parent and actual primary order

The complete triple basis is `(a,b,c)` with ambient code `64a+8b+c`, dimension 512. Construct

`H3 = h1 tensor I8 tensor I8 + I8 tensor h1 tensor I8 + I8 tensor I8 tensor h1`.

Every one of its `512^2` entries equals 18 on the diagonal, -2 for codes differing in exactly one of nine bits, and zero otherwise. The nine-bit character basis proves the complete spectrum `4k` with multiplicity `binom(9,k)`, k=0..9; its floor is zero.

In the actual primary order `(pair r, singleton a)`, define `U e_(r,a) = e_(a,b_r,c_r)`. It is isometric. Its compression is exactly

`U* H3 U = I24 tensor h1 + 12 I192`.

All entries match the raw `full_source_H`. Its floor is 12, with multiplicity 24, witnessed by the 24 singleton-uniform block vectors (raw Gram `8I24`). The other eigenvalues are 16,20,24 with multiplicities 72,72,24.

The primary chart leaves `512-192=320` earlier omitted addresses. Its signed complete forbidden boundary has 256 directly reached target addresses, with entries -2 and collision row sum 12. Those 256 targets do not exhaust the 320-address complement. There are 48 retained tuples with `a=b` or `a=c`; these equal local digits across different cells are legal and are retained exactly.

The full singleton factor is invariant, so the primary cyclic closure in H3 is exactly `C8 tensor K`. One inclusion follows from invariance; the converse follows by commuting the singleton operator with H3 and subtracting its action to generate the pair powers. Consequently this closure has dimension 376, its dynamically hidden complement has dimension 184, its invariant dark space has dimension 136, and its true drift rank is 144. The dark multiplicities at energies `4k`, k=0..9, are

`0,0,3,20,45,45,20,3,0,0`,

obtained by convolution with the singleton multiplicities `1,3,3,1`. These are tensor consequences of the proved pair result, not a fitted 512-dimensional rank calculation.

## 7. Connected preparation and the named older chart

The frozen seed keeps the edge on slots 1,2 and cuts the edge on slots 0,1. Reconstruct the connected tuples by

`b XOR c` is a unit bit; `a XOR b` is a unit bit; `a != c`.

Their lexicographic order matches all 48 frozen placements. For each fixed oriented pair `(b,c)`, there are two allowed singleton addresses a. Their injection V into the primary chart is isometric and matches the raw `connected_receiving_isometry`. A hop in a changes its parity and cannot stay among the neighbors of b. Hence

`V* (U*H3U) V = 18 I48`.

Every normalized connected preparation therefore has expectation `18 tau`: exactly `6 tau` above the primary floor and `18 tau` above the complete three-free floor. V is itself noninvariant; the exact drift rank inside the primary source is 48.

The older fragment chart has 144 all-distinct tuples `(a,b,c)` with `(b,c)` adjacent. It excludes the 48 primary tuples with equal singleton/pair local digits. Its ordering, complete operator, signed boundary, collision terms, connected map and connected compression have all been independently reconstructed and matched to HE3_FRAGMENT_SPACE.json. This identifies the named chart used by the inherited He3 theorem. The prior He3 theorem is not reproved here and is not silently restated with an all-free physical threshold.

## 8. Common-reference ledger and conditional physical transfer

For this geometric Hamiltonian the reference ledger is:

| Endpoint | Original coefficient of tau | After shifting every endpoint by -12 tau |
|---|---:|---:|
| Complete free floor | 0 | -12 |
| Adjacent pair preparation / primary floor | 12 | 0 |
| Connected preparation | 18 | 6 |

Thus the nested additional preparation is six, while the complete all-free comparison pays eighteen. Subtracting twelve only from the connected endpoint changes `18-0` to `6-0`. Subtracting twelve only from the adjacent endpoint changes `12-0` to `0-0`. Both are false common-reference comparisons. A shift of every endpoint leaves every difference unchanged.

If further terms are supplied, a valid conditional ledger has the form

`E_endpoint = E_common_reference + tau * e_geometric_endpoint + v_endpoint`.

Differences include `v_source-v_fragment`; they cannot be inferred from the geometric coefficients. The further terms must belong to one declared self-adjoint Hamiltonian and common metric/domain/reference. Species and statistics, receiving maps including motion/asymptotics, field and recoil, electrons, gates, counterterms, and physical units must be supplied on both endpoints. Full complement couplings must travel or be bounded rigorously. A physical binding assertion additionally needs an admissible source upper and a rigorous lower for every relevant full competing channel of that same Hamiltonian. The adjacent or primary compression floor supplies no such full-channel lower.
