# Independent derivation, before scientific execution

This is an analytical reconstruction of a complete sufficient account, rather
than a prescription to reproduce an earlier number. All computations below
will be executed only after the script hash and predictions are sealed.

Let e=epsilon, Delta=3e. On the normalized unchanged chi, define the completed
field-square vector B for A23+A12 and its crossing displacement Y. For product
placement with incidence P=P^2 and p=<P>, the square expands to

    F_P=p||B||^2+(1-p)||B-Y||^2
       =||B-(1-p)Y||^2+p(1-p)||Y||^2.

Consequently F_internal-F_full=||Y||^2-2Re<B,Y>, and Cauchy gives the stated
residual bound. These vectors live in the same direct-integral, full source,
full Fock Hilbert space, and their norms include the same chi normalization.

The literal full64 swaps obey I+S=(I+S)^2/2>=0. Their algebra gives

    Hex+3I-[(I+S23)+p(I+S12)]
       =(1-p)(I+S12)+(I+S13)>=0.

This proves promotion transfer on the whole source with arbitrary ancillas.
The raw frame U has U^TU=6I; all swaps act as -I on it. The actual current
images must have Hex eigenvalue zero before Delta=3e can be consumed.

Use the original full T1, not a new T1 for the path Hamiltonian. Write q for
its full drive coefficient, n for its norm coefficient, c for its full vacuum
CT, and kappa=c-q. The photon coefficient is m=q-Delta*n. Photon parity
counts that coefficient once. Equal self-drive contractions from the raw
signed contact Gram make each internal drive half the full one. Therefore

    D F_full=e^2*g*(kappa-Delta*n)+e^4*C1_full,
    D F_internal=e^2*g*(mu0-Delta*n)+e^4*C1_internal.

Both C1 are expectations on unscaled T1. Complete TT positivity bounds each
by 2mu0*Tr(G12+G23)*n*g, including every source intermediate. The transferred
promotion is at most Delta*e^2*n*g/D, cancelling the negative Delta*n in the
mixture. After this signed cancellation the numerator upper is positive, so
D>=1 may be used. This is not subtraction of guessed pieces from an aggregate.

The reconstructed full account is U=A+B(1-p), where

    A=K+3e^2*b*K*gU+e^2*kappaU*gU+3e^2*M_U*gU
      +6e^4*mu0*T*b*gU+4gamma*chiU+(45/2)gamma*e^2*b*gU,
    B=e^2*gU*(mu0-kappaU),  K=3/(4m),
    kappaU=2Delta*b-Fcross_lower, T=Tr(G12+G23).

Every term is reconstructed from its owning operand. The original trial gap,
full massive COM shift, normal EDGE and gate covariance remain unchanged.
The supplied scalar enclosures are premises, not recomputed continuum
integrals. Their geometry, norm and coefficient meanings will be audited.

Separately, on the same normalized chi,

    0<=F_full <=3e^2*Delta^2*b3*gU+6e^4*mu0*T*b*gU,
    e^2*mu0*gL/(1+3e^2*b*gU)<=C_cross
      <=e^2*mu0*gU*(1+3e^2*b*T).

The first inequality follows from the positive frequency integrand
Delta^2 |h|^2/[omega(omega+Delta)^2]*(2-A), bounded by 3Delta^2*b3.
The quadratic C_cross contains its vacuum g and one-boson source Gram; it is
not the quartic one-boson payment.

For full192, verify every raw H entry is 18I-2A_cube in each actual oriented
pair block. Verify J is its actual isometry and its two addresses have cube
distance two. Walsh diagonalization keeps all eight coordinates: energies
12+4k with binomial multiplicities. The symmetric receiving spectral weights
are (1/4,1/4,1/4,1/4); the antisymmetric weights are (0,1/2,1/2,0). Below 12tau,
the symmetric resolvent exceeds the antisymmetric one by

    16tau^2*(delta+6tau)/[delta(delta+4tau)(delta+8tau)(delta+12tau)]>0.

Birman-Schwinger on the full rank-two P in each cube therefore gives its
lowest root from (e/4)sum 1/(delta+4ktau)=1. All dark and nonreceiving
directions retain their energies. The exact ground is 12tau-e-delta, saturated
by the common antisymmetric colour frame. At connector absence H>=12 and
S23>=-I, while complete field, massive and gate forms are nonnegative; hence
12tau-e+L_common is a lower, with L_common=0 only in the frozen ledger chart.

Put r=tau/delta, a_k=(1+4kr)^-1 and S_j=sum a_k^j. Then
delta=e*S1/4, tau=e*r*S1/4, p=S1^2/(4S2), d(tau)/dr=e*S2/4>0.
The inequality S2^2<=S1*S3 proves p decreases. Thus
A+B(1-p)-delta increases strictly when B>0. Exact rational signs at an upper
bracket for r(tau_ceiling) certify the entire open interval below that ceiling.
This proof, rather than a grid of positive tau samples, is the all-interval
step. Positive gates add ep and leave formation ep-delta>=0. A changed paid
ledger +e loses the constructed certificate since delta<=e.

Form domain: start on finite-source, finite-photon smooth compact-frequency
vectors tensor smooth compact matter vectors and a core for normal EDGE.
The annihilation map a(sqrt(omega)) is closed from the H_F form domain to its
direct integral. The displacement h/sqrt(omega) times bounded finite-source
currents is a bounded map because mu0 is finite; translated phases have
modulus one. Their sum is closed on that same form domain. All identities
extend by form continuity. The original T1 has finite norm by b, finite
photon energy by mu0, finite CT by bounded full source Grams and finite massive
motion by the retained whole-spectrum majorant. The sharp nonrelativistic
second momentum moment is not assumed finite. Original gate/EDGE form-domain
membership and its correlated bound remain explicit inherited premises.
