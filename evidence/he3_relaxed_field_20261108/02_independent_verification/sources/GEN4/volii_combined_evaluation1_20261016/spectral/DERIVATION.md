# Whole-spectrum massive recoil evaluation

This is a new conservative evaluation of the original sharp j2 form factor in the completed full-source Ritz account. It does not change that form factor, introduce a frequency cutoff, assign a physical neutron mass to the source chart, or identify the prepared separated vacuum with a free ground. The declared homogeneous Cartesian translation, all five STF directions, both helicities, complete counterterm, source complement, and four even offsets remain those of the frozen parent.

The actual radial density is |h_R(omega)|²=2 omega j2(omega R)²/(kappa pi), kappa=4/5, with mu0=1/(4R). The full massive translation cost of one physical constituent of mass m is T_m(k)=sqrt(m²+k²)−m in the compatible matter/wave-speed-one chart. In a photon total-momentum fiber the COM and relative shifts together change one physical constituent's momentum by k. The actual contact Gram has largest eigenvalue 3/2, so the previous recoil payment 3 epsilon² mu0 G4 can be replaced by 3 epsilon² M_m G4, where

    M_m(Delta,R)=integral_0^infinity T_m(omega)|h_R(omega)|²/(omega+Delta)² d omega.

For a centered momentum packet, concavity of sqrt gives <T_m(p+k)> <= sqrt(m²+<p²>+k²)−m <= <p²>/(2m)+T_m(k). The same positive self terms therefore retain the previous conservative packet kinetic coefficient 1+3 epsilon² b G4. This uses the exact massive kinetic form for the sharp dressed component; its divergent quadratic-momentum moment is never used as a finite kinetic bound. In a different speed chart the mass and wave momentum must first be converted consistently; the controls below explicitly use speed one.

Set a=mR>=1/2, X=2a>=1 and beta=Delta R>=0. The exact elementary inequality T_m(omega)<=min(omega²/(2m),omega) and (x+beta)²>=x² yield

    M_m <= 2/(kappa pi R) [ (1/X) integral_0^X x j2(x)² dx + integral_X^infinity j2(x)² dx ].

The split X is set by the physical kinetic majorant, and both sides of the split remain paid. The original integral representation supplies |j2(x)|<=x²/15. Its exact elementary formula supplies |j2(x)|<=1/x+3/x²+3/x³ for x>=1. Consequently the complete head and tail are bounded by

    head0 = 1/1350,
    head1(X) = log X + 6(1−1/X) + (15/2)(1−1/X²)
               + 6(1−1/X³) + (9/4)(1−1/X⁴),
    tail(X) = 1/X + 3/X² + 5/X³ + (9/2)/X⁴ + (9/5)/X⁵.

Their sum J=(head0+head1)/X+tail is exactly

    J(a) = [log X+91/4+1/1350]/X −3/X² −5/(2X³)
           −3/(2X⁴) −9/(20X⁵).

Thus M_m <= 2J/(kappa pi R) < 5J/(6R), using only pi>3. This deliberately conservative rational prefactor avoids an invented numerical pi operand. The bound is uniform in every nonnegative source gap; its source profile and infinite UV tail are retained. Its integral-majorant representation shows it decreases with a and tends to zero as log(a)/a. Thus a certified control also bounds every larger a within the same chart. At a<1/2 this formula is not used; the completed universal M_m<=mu0 remains available.

The three declared dimensionless controls are R=1 and mR=100,1000,1000000. They are exploratory members, not measured particle masses, physical radii, or a C13 calibration. Each uses the original epsilon=1/573049 and may use j=1, Delta=3epsilon; this bound is independent of that choice as long as Delta>=0. A native logarithmic evaluation returns U_m=5J/(6R), and a second evaluation returns 2mu0−3U_m. A positive second result removes the earlier coarse recoil obstruction; it is not by itself a negative full trial energy or physical binding prediction. All packet kinetic, readiness, quartic, bare offsets, and signed common references must still be included in a subsequent combined evaluation.

The installed GEN5_LOG_EVALUATE accepts source_binding, precision_bits, data, with data.expression containing an exact rational constant and weighted logarithms of positive rational arguments. It supplies Arb-directed certified intervals; it is not a new integration engine. Python prepares rational coefficients only. The independent verifier, run only after native returns exist, reconstructs the integrated head/tail coefficients and encloses logarithms with an independent exact rational atanh series.
