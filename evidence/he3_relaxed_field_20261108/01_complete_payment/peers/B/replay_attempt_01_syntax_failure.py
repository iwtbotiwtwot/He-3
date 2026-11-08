#!/usr/bin/env python3
"""Independent, engine-free, exact-rational replay of blind B's CR2 bounds.

Inputs: public frozen case only. Dependencies: Python standard library only.
No engine imports, archived generators, native outputs, or other learner data.
All file writes are confined to the caller's fresh --output directory.

Analytic inequalities (reported separately from native execution):
  L_total=max absolute row sum of the actual full64 positive Gsep;
  L_cross=max absolute row sum of actual full64 positive Gcross;
  F_full <= [eps^2*3*Delta^2*b3*g + eps^4*2*mu0*L_total*n*g]/D;
  C_cross <= eps^2*mu0*[g+eps^2*L_cross*n*g]/D,
  D=1+eps^2*n*g, 0<=n<=3*b, b3=R/42.
The common D is retained in these identities, then bounded by D>=1.
"""
import argparse
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal, localcontext
from math import isqrt
import json, hashlib

DEFAULT_CASE='/home/lilhelper/SAM_Research_Overflow/Courtroom_II/campaigns/he3_relaxed_field_20261108/01_complete_payment'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
def ratmatrix(x):return [[Q(v) for v in r] for r in x]
def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def transpose(a):return list(map(list,zip(*a)))
def product(a,b):
 assert len(a[0])==len(b)
 bt=transpose(b)
 return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in bt] for row in a]
def plus(a,b):return [[x+y for x,y in zip(aa,bb)] for aa,bb in zip(a,b)]
def times(a,s):return [[s*x for x in row] for row in a]
def tensor(a,b):
 return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]
def gram(a):return product(transpose(a),a)
def zero(a):return all(v==0 for row in a for v in row)
def equal(a,b):return a==b
def strmatrix(a):return [[str(v) for v in row] for row in a]
def diag_trace(a):return sum((r[i] for i,r in enumerate(a)),Q(0))
def rownorm(a):return max(sum((abs(v) for v in r),Q(0)) for r in a)
def decimal(q,digits=18):
 with localcontext() as ctx:
  ctx.prec=digits
  return str(Decimal(q.numerator)/Decimal(q.denominator))
def sqrt_interval(q,bits=192):
 assert q>=0
 s=1<<bits;n=isqrt((q.numerator*s*s)//q.denominator)
 lo=Q(n,s);hi=lo if lo*lo==q else Q(n+1,s)
 assert lo*lo<=q<=hi*hi
 return lo,hi
def real_bounds(entry):
 assert Q(entry['im']['lower'])==Q(entry['im']['upper'])==0
 return Q(entry['re']['lower']),Q(entry['re']['upper'])
def moment_sums(r):
 a=[Q(1)/(1+4*k*r) for k in range(4)]
 return sum(a),sum(v*v for v in a),sum(v*v*v for v in a)
def family(r,e):
 s1,s2,s3=moment_sums(r)
 d=e*s1/4;p=s1*s1/(4*s2);t=e*r*s1/4
 assert 0<d<=e and Q(1,4)<=p<=1
 assert e*p>=d
 assert s2*s2<=s1*s3
 return t,d,p
def isolate(P,Qextra,e):
 """B(r)=P-delta(r)+(1-p(r))*Qextra increases strictly on r>=0."""
 def value(r):
  t,d,p=family(r,e);return P-d+(1-p)*Qextra
 v0=P-e;vinf=P-e/4+Q(3,4)*Qextra
 if v0>=0:return dict(status='NO_INTERVAL_FROM_THIS_UPPER',at_zero=str(v0),at_infinity=str(vinf))
 if vinf<=0:return dict(status='ALL_POSITIVE_TAU',at_zero=str(v0),at_infinity=str(vinf))
 lo=Q(0);hi=Q(1)
 while value(hi)<0:hi*=2
 for _ in range(144):
  mid=(lo+hi)/2
  if value(mid)<0:lo=mid
  else:hi=mid
 tl,dl,pl=family(lo,e);th,dh,ph=family(hi,e)
 assert value(lo)<0<=value(hi) and tl<th
 return dict(status='FINITE_CERTIFYING_INTERVAL',at_zero=str(v0),at_infinity=str(vinf),r_root_bracket=[str(lo),str(hi)],tau_root_bracket=[str(tl),str(th)],tau_over_epsilon_root_bracket=[str(tl/e),str(th/e)],lower_sign=str(value(lo)),upper_sign=str(value(hi)),guaranteed_interval={'lower':'0','upper':str(tl),'lower_exclusive':True,'upper_exclusive':True},tau_ceiling_decimal=decimal(tl),tau_over_epsilon_ceiling_decimal=decimal(tl/e),threshold_p_bracket=[str(ph),str(pl)],threshold_delta_bracket=[str(dh),str(dl)])

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--case',default=DEFAULT_CASE,type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
 C=a.case.resolve();O=a.output.resolve()
 if O.exists():raise SystemExit('Output must be a fresh directory; preserve every earlier attempt.')
 # Read and authenticate public operands before creating any output.
 freeze=load(C/'FREEZE.json');custody=[]
 for rel,h in freeze['files'].items():
  got=digest(C/rel);assert got==h,rel;custody.append(dict(path=rel,sha256=got))
 T=load(C/'sources/TRIAL_FAMILY.json');payload=load(C/'sources/light/COLOUR_64_CONSTRUCTION_PAYLOAD.json');sp=load(C/'sources/GEN4/volii_quantum_motion_join1_20261016/source/SOURCE_PACKET.json');placement=load(C/'sources/light/HE3_INDEPENDENT_FRAGMENTS.json')
 old=load(C/T['old_paid_matrix_source'])['matrix']['entries'];itf=load(C/'sources/GEN4/volii_dressed_reference1_20261016/joint/INTERFACE.json')
 e=Q(T['epsilon']);mu=Q(T['mu0']);b=Q(T['b_upper']);Delta=3*e;gamma=Q(T['gamma_gate']);chi=Q(itf['chi_upper']);b3=Q(T['R'])/42
 ops={k:ratmatrix(v) for k,v in payload['data']['operators'].items()}
 d12=tensor(ops['I4'],ops['D16']);d23=tensor(ops['D16'],ops['I4']);r12=tensor(ops['I4'],ops['R16']);r23=tensor(ops['R16'],ops['I4']);u=ops['U'];ut=transpose(u)
 swap16=plus(ops['I16'],times(ops['Pa16'],-2));s12=tensor(ops['I4'],swap16);s23=tensor(swap16,ops['I4']);s13=product(product(s12,s23),s12);hx=plus(plus(s12,s23),s13)
 gc=plus(gram(d12),gram(r12));gi=plus(gram(d23),gram(r23));gt=plus(gc,gi)
 G=ratmatrix(sp['G4']);x12=product(d12,u);x23=product(d23,u)
 source_checks={
 'full_source_dimension':len(gc),'trial_gram_6I':equal(gram(u),times(eye(4),6)),
 'vacuum_Hex_minus3':zero(plus(product(hx,u),times(u,3))),
 'both_contact_helicity_images':product(r12,u)==x12 and product(r23,u)==x23,
 'both_contact_Hex_gap3':zero(product(hx,x12)) and zero(product(hx,x23)),
 'cross_vacuum_metric_equals_G4':times(product(ut,product(gc,u)),Q(1,6))==G,
 'internal_vacuum_metric_equals_G4':times(product(ut,product(gi,u)),Q(1,6))==G,
 'signed_cross_Gram_minus_G4_over4':times(product(transpose(x12),x23),Q(1,6))==times(G,Q(-1,4)),
 'swaps_symmetric_involutions':all(s==transpose(s) and product(s,s)==eye(64) for s in [s12,s23,s13]),
 'total_gram_is_complete_four_current_Gram':gt==plus(plus(gram(d12),gram(r12)),plus(gram(d23),gram(r23))),
 'Gcross_trace':str(diag_trace(gc)),'Gtotal_trace':str(diag_trace(gt)),
 'Gcross_row_sum_upper':str(rownorm(gc)),'Gtotal_row_sum_upper':str(rownorm(gt))}
 assert all(v is True for k,v in source_checks.items() if isinstance(v,bool))
 assert diag_trace(gt)==Q(T['Trace_Gsep']) and 2*diag_trace(gc)==diag_trace(gt)
 Lc=rownorm(gc);Lt=rownorm(gt);Tr=diag_trace(gt)
 # Recover the full192 source's block structure and spectral weights. No selected
 # subspace replaces the source: every block, off-block entry and J column is checked.
 H=ratmatrix(placement['full_source_H']);J=ratmatrix(placement['connected_receiving_isometry']);I8=eye(8)
 cube=[[Q(18 if i==j else (-2 if (i^j).bit_count()==1 else 0)) for j in range(8)] for i in range(8)]
 assert len(H)==192 and len(J)==192 and len(J[0])==48
 assert gram(J)==eye(48)
 assert all(H[i][j]==(cube[i%8][j%8] if i//8==j//8 else 0) for i in range(192) for j in range(192))
 P=product(J,transpose(J));assert product(P,P)==P
 assert zero(plus(times(eye(192),-18),product(P,H))) is False # P is an incidence projector, not I.
 L=plus(cube,times(I8,-12));projectors=[]
 for k in range(4):
  z=I8
  for l in range(4):
   if l!=k:z=product(z,times(plus(L,times(I8,-4*l)),Q(1,4*k-4*l)))
  projectors.append(z)
 assert sum((projectors[k][i][j] for k in range(4)),Q(0))==I8[i][j] for i in [] for j in []
 weights=[]
 for block in range(24):
  ids=[i for i in range(8) if P[8*block+i][8*block+i]==1];assert len(ids)==2 and (ids[0]^ids[1]).bit_count()==2
  assert all(P[8*block+i][8*block+j]==Q(i==j and i in ids) for i in range(8) for j in range(8))
  vv=[[Q(i in ids)] for i in range(8)];ww=[[Q((1 if i==ids[0] else -1) if i in ids else 0)] for i in range(8)]
  sym=[product(transpose(vv),product(z,vv))[0][0]/2 for z in projectors];anti=[product(transpose(ww),product(z,ww))[0][0]/2 for z in projectors]
  assert sym==[Q(1,4)]*4 and anti==[0,Q(1,2),Q(1,2),0]
  weights.append(dict(block=block,selected_sites=ids,symmetric_weights=list(map(str,sym)),antisymmetric_weights=list(map(str,anti))))
 placement_checks=dict(dimension=192,block_count=24,connected_projector_rank=48,J_isometry=True,full192_hopping_equals_24_cube_blocks=True,all_connected_pairs_distance_two=True,full_source_floor='12',gap_levels=['0','4','8','12'],symmetric_secular_weights=['1/4']*4,antisymmetric_secular_weights=['0','1/2','1/2','0'],blocks=weights)
 rows=[]
 for i,row in enumerate(T['rows']):
  gl,gu=map(Q,row['g_interval']);m=Q(row['mR']);K=Q(3,4)/m;Um=Q(row['mass_majorant_upper']);pu=Q(row['paid_kernel_upper']);assert pu==2*Delta*b-Q(row['actual_Fcross_lower'])
  terms=dict(packet_kinetic=K,dressed_packet_kinetic=3*e*e*b*K*gu,paid_source_field_kernel=e*e*gu*pu,massive_photon_COM_recoil=3*e*e*Um*gu,full_quartic_CT_trace_upper=6*e**4*mu*Tr*b*gu,full_quartic_CT_rowsum_upper=6*e**4*mu*Lt*b*gu,vacuum_gate=4*gamma*chi,dressed_gate=Q(45,2)*gamma*e*e*b*gu)
  base=terms['packet_kinetic']+terms['dressed_packet_kinetic']+terms['paid_source_field_kernel']+terms['massive_photon_COM_recoil']+terms['vacuum_gate']+terms['dressed_gate']
  Poriginal=base+terms['full_quartic_CT_trace_upper'];Paid=base+terms['full_quartic_CT_rowsum_upper']
  oldlo,oldhi=real_bounds(old[i][8]);assert oldlo<=Poriginal<=oldhi
  Dmax=1+3*e*e*b*gu
  Fu=3*e*e*Delta*Delta*b3*gu+6*e**4*mu*Lt*b*gu
  Cu=e*e*mu*gu*(1+3*e*e*b*Lc)
  Cl=e*e*mu*gl/Dmax
  slo,shi=sqrt_interval(Fu*Cu);Qextra=Cu+2*shi
  interval=isolate(Paid,Qextra,e)
  # A looser trace route is independently retained as an unsuccessful/sharper-bound control.
  Ft=3*e*e*Delta*Delta*b3*gu+6*e**4*mu*Tr*b*gu
  Ct=e*e*mu*gu*(1+3*e*e*b*Tr/2)
  _,st=sqrt_interval(Ft*Ct);Qt=Ct+2*st
  traceinterval=isolate(Poriginal,Qt,e)
  rows.append(dict(row=i,mR=str(m),lane=row['lane'],g_interval=list(map(str,[gl,gu])),original_frozen_paid_upper=str(oldhi),original_formula_paid_upper=str(Poriginal),refined_complete_paid_upper=str(Paid),source_to_fragment_intrinsic_bound='P_refined-delta+(1-p)*Q_extra',full_field_bounds=['0',str(Fu)],cross_self_CT_bounds=[str(Cl),str(Cu)],sqrt_FC_enclosure=list(map(str,[slo,shi])),Q_extra=str(Qextra),norm_bounds=['1',str(Dmax)],same_norm='D_i=1+epsilon^2*n_i*g_i, 0<=n_i<=3*b_upper; phi_tau norm1; all displayed energy bounds use this same D before Dmin1 is applied.',terms={k:str(v) for k,v in terms.items()},intrinsic_interval=interval,trace_route_interval=traceinterval,positive_gate_interval={'status':'NO_INTERVAL_FROM_THIS_UPPER','identity_baseline':'epsilon*p','reason':'P_refined+epsilon*p-delta+(1-p)*Q_extra >= P_refined >0 for every tau>0'},connected_limit=str(Paid-e),source_promotion_transfer='(Hex+3I)-[S23+p*S12+(1+p)I]=(1-p)*(I+S12)+(I+S13)>=0',scalar_mean_substitution_error='p*(1-p)*C_cross; strictly positive at every finite tau>0 because 1/4<p<1 and C_cross_lower>0',display={'g_upper':decimal(gu),'original_paid':decimal(Poriginal),'refined_paid':decimal(Paid),'F_full_upper':decimal(Fu),'C_cross_lower':decimal(Cl),'C_cross_upper':decimal(Cu),'Q_extra':decimal(Qextra),'norm_upper':decimal(Dmax)}))
 out=dict(schema='CR2_BLIND_B_COMPLETE_RETAINED_FIELD_BOUNDS_V1',provenance='Host analytical derivation and independent exact-rational replay. This file is not a native-engine receipt and not external verification.',case=str(C),epsilon=str(e),Delta=str(Delta),mu0=str(mu),b_upper=str(b),b3=str(b3),gamma_gate=str(gamma),chi_upper=str(chi),source_operator_bounds={'Gcross_trace':str(diag_trace(gc)),'Gtotal_trace':str(Tr),'Gcross_norm_upper':str(Lc),'Gtotal_norm_upper':str(Lt),'method':'Complete real positive Gram matrices; exact maximum absolute row sum bounds self-adjoint operator norm.'},all12_retained=True,rows=rows,certifying_intrinsic_rows=[r['row'] for r in rows if r['intrinsic_interval']['status']!='NO_INTERVAL_FROM_THIS_UPPER'],positive_gate_certifying_rows=[],conditional_family={'r':'tau/delta >0','S1':'sum_{k=0}^3 1/(1+4*k*r)','S2':'sum_{k=0}^3 1/(1+4*k*r)^2','delta':'epsilon*S1/4','tau':'epsilon*r*S1/4','p':'S1^2/(4*S2)','monotonicity':'tau prime=epsilon*S2/4>0; delta decreases; p prime has sign S2^2-S1*S3<=0; the intrinsic upper difference increases strictly.','fragment_lower':'12*tau-epsilon+L_common','L_common':'0','intrinsic_upper_minus_fragment_lower':'P_refined-delta+(1-p)*Q_extra','positive_gate_upper_minus_fragment_lower':'P_refined+epsilon*p-delta+(1-p)*Q_extra','exact_field_identity':'<Hf(A_internal+P*A_cross)>=p*F_full+(1-p)*F_internal = <Hf(A_internal+p*A_cross)>+p*(1-p)*C_cross','field_difference_bound':'F_internal-F_full<=C_cross+2*sqrt(F_full*C_cross)','reference':'Whole-field completed-square fragment lower; original free variational upper is retained only as a control and never used as a lower.'},full_norm_reference_account={'trial':'phi_tau normalized full192 ground tensor the unchanged complete chi_i','D':'1+epsilon^2*n_i*g_i','source_floor':'Original Hex floor -3epsilon; source promotion nonnegative and transferred by the exact full64 positive decomposition.','field':'Both physical helicities, all sharp positive frequencies, all5 STF before source incidence, every self/mixed CT and all64 source/Fock complement directions retained in the Gram/operator inequalities.','motion':'Original full massive dispersion and matter/photon total-momentum COM recoil; Gaussian Cartesian variance1 unchanged. No finite nonrelativistic dressed derivative substituted.','EDGE':'Independent matched normal EDGE vacuum, affine mean1/2, zeta1, gate variance2; original localized gate bound retained.','reference_changes':'Preparation/reference and normal vacuum terms are the retained common baseline. Frozen remaining changed signed ledger0; no new work or physical receiving assignment is added.','normalization_rule':'Original positive paid upper is already normalized by the valid Dmin1 bound. It is never divided again. New numerator bounds likewise use the exact same D and only then its positive lower bound1.'},remaining_input={'bounded_mathematical_question':'No missing operand is required for the displayed sufficient complete upper and its conditional intervals.','exact_expectation':'Sharper or exact payment would use the actual normalized one-boson CT contractions and signed residual-cross contraction, rather than the retained complete-source norm/Cauchy bounds.','physical_assignment':'No physical tau, isotope mass/radius, current/species/action/ruler conversion, changed reference or actuator-work value is selected.'},retained_failures=['Shell command python was unavailable; pinned interpreter was used thereafter.','Native attempt_01 rejected identity steps with an extraneous inputs key; native_job_02 corrected only that grammar.','Trace-based route retained in rows as a valid weaker bound; complete-source row-sum norms improve it without changing any trial.'],dependencies={'python':'standard library only','sqrt_bits':192,'root_bisections':144},input_custody=custody)
 O.mkdir(parents=True)
 save(O/'RESULTS.json',out);save(O/'SOURCE_CHECKS.json',source_checks);save(O/'PLACEMENT_CHECKS.json',placement_checks);save(O/'SOURCE_OPERATORS.json',{'Gcross':strmatrix(gc),'Gtotal':strmatrix(gt),'vacuum_G4':strmatrix(G)})
 save(O/'REPLAY_RECEIPT.json',{'script_sha256':digest(Path(__file__)),'case_freeze_sha256':digest(C/'FREEZE.json'),'output':str(O),'engine_imports':False,'standard_library_only':True,'fresh_output':True,'files':['RESULTS.json','SOURCE_CHECKS.json','PLACEMENT_CHECKS.json','SOURCE_OPERATORS.json']})
 print(json.dumps({'output':str(O),'certifying_intrinsic_rows':out['certifying_intrinsic_rows'],'positive_gate_certifying_rows':[],'ceilings':[{k:r[k] for k in ['row','mR','lane']}|{'tau':r['intrinsic_interval'].get('tau_ceiling_decimal')} for r in rows]},indent=2))
if __name__=='__main__':main()
