# Signed account and hypotheses

This case bounds the same frozen product trial by two routes. Their different numerical thresholds are thresholds of sufficient uppers, not exact trial energies.

The owning trial, reference and parameters are `sources/TRIAL_FAMILY.json`, the original `volii_dressed_reference1_20261016/joint/DERIVATION.md`, and the `volii_quantum_motion_join1_20261016/field/R2_DERIVATION.md` and source packet, all retained under `sources/GEN4/`. New matrices and numbers live in `peers/` and `RESULTS/lead_replay/`.

Write e=epsilon, Delta=3e, mu0=1/4, b=5/72, nmax=3b. The normalized matter/source/Fock factor is the unchanged chi=(T0+e T1)/sqrt(D), including its Gaussian and normal EDGE factor, with D=1+e^2*n*g. The placement factor is the normalized full192 ground of tau*H-e*P, P=JJ^T. All placement and full64 source directions remain. The original all-frequency sharp profile is used; its convergent inverse moment is b3=R/42. No divergent positive-frequency derivative moment is substituted.

The actual full-source contact currents give positive Grams Gc=G12, Gi=G23 and Gt=Gc+Gi. The common normalized vacuum compression is G4 for either self Gram. The signed drive Grams have equal self parts G4/2 and mixed part -G4/4. The replays reconstruct these from the literal source operators. The exchange matrices are symmetric involutions. Hex*T0=-3*T0 and Hex*T1=0, hence the original one-boson source promotion is Delta*e^2*n*g/D.

Let kappa be the original paid kernel and C1 the full CT on unscaled T1, without e^2. Photon parity and the original continuum identities give

```
F_full = [e^2*g*(kappa-Delta*n)+e^4*C1_full]/D,
0 <= kappa-Delta*n <= 3*Delta^2*b3,
C_cross = e^2*mu0*[g+e^2*<T1|Gc|T1>]/D.
```

The whole positive TT/contact Gram gives CT_full/e^2 <=2*mu0*Gt, so C1_full<=2*mu0*Lt*n*g for any Lt>=||Gt||. Similarly <T1|Gc|T1><=Lc*n*g. A uses traces; B uses exact maximum absolute row sums of the full source matrices. For any self-adjoint Gram the maximum absolute row sum bounds its operator norm. Thus, with the retained positive eigenlane enclosure [gL,gU],

```
F_full <= 3*e^2*Delta^2*b3*gU + 6*e^4*mu0*Lt*b*gU,
C_cross <= e^2*mu0*gU*(1+3*e^2*b*Lc),
C_cross >= e^2*mu0*gL/(1+3*e^2*b*gU) >0.
```

A also retains a slightly tighter lower using the monotonic ratio at gL. The source/Fock norm is common in every exact identity; D>=1 is applied only after the relevant numerator upper is proved positive.

For p=<P>, the exact product-field expectation is

```
F_P = p*F_full+(1-p)*F_internal
    = <Hf(A_internal+p*A_cross)>+p*(1-p)*C_cross.
```

This is a projection identity for the complete square, not a mean-field approximation. For finite positive tau, 1/4<p<1, so its variance term is strictly positive. Source promotion obeys the full-space identity

```
(Hex+3I)-[(I+S23)+p*(I+S12)]
  = (1-p)*(I+S12)+(I+S13) >=0.
```

This identity is required before importing the signed old source/field account. An aggregate paid upper alone does not license subtracting guessed component values.

## Route A: direct signed cancellation

Equal contact drive contractions and photon parity give

```
F_internal=[e^2*g*(mu0-Delta*n)+e^4*C1_internal]/D.
```

The same whole positive allowance bounds each C1, and hence their p-mixture. The proved source-promotion upper cancels the negative Delta*n in that mixture. The original paid kernel upper is kappaU=2*Delta*b-Fcross_lower, a positive coefficient below mu0. With K=3/(4m), the original massive majorant M, localized gate bound chiU and gamma,

```
A_i = K+3*e^2*b*K*gU + e^2*kappaU*gU + 3*e^2*M*gU
      +6*e^4*mu0*Tr(Gt)*b*gU
      +4*gamma*chiU+(45/2)*gamma*e^2*b*gU,
B_i = e^2*gU*(mu0-kappaU) >0.
```

Every signed original component, including the negative retarded cross component, is reconstructed before the net positive coefficient is bounded. A_i reproduces the original connected-support upper under its already applied Dmin=1 rule. It is not divided again. The relaxed paid upper is A_i+B_i*(1-p).

## Route B: whole-source norm and residual Cauchy

B replaces only Tr(Gt) in A_i by the smaller certified row-sum norm upper Lt to obtain P_refined. Let Bfull be the completed-square vector on normalized chi and Y its crossing displacement. Then

```
F_internal-F_full = C_cross-2*Re<Bfull,Y>
                  <= Cbar+2*sqrt(Fbar*Cbar) = Q_i.
```

The signed mixed contraction has not been assigned a sign. A retained exact rational square-root upper makes Q_i rational. Together with the full-source promotion comparison, this yields the complete paid upper P_refined+(1-p)*Q_i. It retains all mixed counterterms and projector variance. It is a different valid inequality from route A, not a numerical estimate of A's coefficient.

## Fragment lower and conditional intervals

The receiving Hamiltonian is tau*H+e*S23+e*P*S12 plus the declared complete field, massive motion and original gate terms. Its frozen fragment lower is 12*tau-e+Lcommon, Lcommon=0 in the unchanged-ledger chart. This lower follows from the full source floor, S23>=-I and nonnegative complete field/motion/gate forms. No free variational upper replaces it.

The supplied full-source family has delta>0 solving (e/4)*sum_k 1/(delta+4*k*tau)=1 and formation tau*(<H>-12)=e*p-delta. The intrinsic source baseline contributes -e*p against that lower. Thus the sufficient total gaps are

```
f_A=A_i+B_i*(1-p)-delta,
f_B=P_refined+Q_i*(1-p)-delta.
```

For r=tau/delta, a_k=1/(1+4*k*r), S_j=sum_k a_k^j,

```
delta=e*S1/4, tau=e*r*S1/4, p=S1^2/(4*S2),
d(tau)/dr=e*S2/4>0.
```

Delta decreases and p decreases by S2^2<=S1*S3. Both sufficient gaps therefore increase strictly. Exact rational bisection brackets their unique zero when their endpoint signs differ. A uses r_A=4*r; the comparison explicitly handles this convention. The common sufficient endpoint is the smaller retained lower bracket, with both gap signs checked negative there.

The positive crossing gate is e*P*(I+S12), adding e*p. Its constructed gap is paid_upper+e*p-delta>=paid_upper>0 because formation is nonnegative. This is a failure of these sufficient gate certificates, not a lower bound obtained from a noncertifying upper.

The hypotheses are the frozen source/current and profile definitions, supplied inherited retarded/massive/gate enclosures, the unchanged normalized trial, the declared intrinsic recipient, and the common reference chart. Changing a source, profile, preparation, gate, signed work ledger or physical receiving assignment requires its own account. No isotope mass/radius, physical tau, action or ruler conversion is established here. Next: verify the shared conditional statement independently before using it as a standing volume result.
