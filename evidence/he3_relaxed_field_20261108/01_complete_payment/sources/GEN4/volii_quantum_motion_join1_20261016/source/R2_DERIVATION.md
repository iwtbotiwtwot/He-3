# Complete counterterm on the actual one-boson source images

Prepare only after the actual R1 contact-resolved native return. Consume its full X=[D12U,D23U],64x8. Its contact/helicity identities and coefficientwise excitation equations determine whether a single3j source denominator is valid. The source lane does not replace a nonzero defect with that gap.

The real channel order is T=(D12,R12,D23,R23). Physical Hermitian helicity currents are S=(D12,iR12,D23,iR23), with phase q=(1,i,1,i). Build the FULL64x32 W=[D12X,R12X,D23X,R23X]. The exact32x32 matrix

    Quartic=W^T W/6

retains every full-source intermediate in the counterterm acting on a one-boson source image. Each channel block is8, each transition-contact subblock is4. This is a real-R Gram: field contraction must apply conjugate(q_alpha)*q_beta to the CT channels, and the additional emitted-photon helicity phases to both contact-transition indices. It is not silently the complex ordered C-current quartic.

Also construct on the complete64-source space

    Gsep=D12^2-R12^2+D23^2-R23^2 >=0,
    Norm8=X^T X/6,
    Gsep8=X^T Gsep X/6.

The original normalized full TT Gram for two identical profiles obeys0<=K_CT<=2mu0 I4, including mixed helicity directions. Consequently the complete CT source operator without epsilon^2 is <=2mu0Gsep and <=2mu0Tr(Gsep)I64. The task returns a native trace computed by exact diagonal/bit-permutation twirls, not host arithmetic. Its positive comparison is

    Tr(Gsep)Norm8-Gsep8 >=0.

This yields a rigorous coarse chi-counterterm bound C1<=2mu0Tr(Gsep)N. The full Quartic permits the sharper exact contraction of static K_CT with the retarded one-boson norm Gram K_N; these are different frequency weights and their physical source indices remain explicit.

For a prepared source eigenvector and the normal vacuum, write chi=(H0-E)^-1 V0|psi,0>, with actual certified contact gap in its denominator. The normalized0+1boson trial has norm1+epsilon^2N. Since the linear field changes boson number, its one-boson diagonal vanishes. The exact prepared relative Ritz numerator is epsilon^2(CT0-J)+epsilon^4C1, with the complete bare-source offset preserved. This is an exact variational trial identity; it does not replace the full ground Hamiltonian with a leading virtual potential. Across all four prepared lanes, keep the matrix norm, even coefficients and commutators unless the actual source-algebra covariance permits the stated specialization.

The motion lane retains the complete massive kinetic form and COM/relative/photon momentum shifts, whose additional moment is M<=mu0. The stronger NR H1 derivative domain is not assumed and no UV smoothing/cutoff is selected. Same source/free preparations, full total CT, both physical helicities, all5STF modes and all64 source states remain. Bound/free prepared-state contrast and full free-ground energy are different questions. Species assignment, physical current normalization and common energy/action/clock chart remain separate source inputs; no C13 fitting.

Output32x40: columns0..7 contain four8x8 blocks Trace(Gsep)I8,Norm8,Gsep8,positive comparison; columns8..39 contain full32x32 Quartic.
