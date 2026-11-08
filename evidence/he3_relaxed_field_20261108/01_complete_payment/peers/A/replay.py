#!/usr/bin/env python3
"""Engine-free exact replay of CR2 A's complete retained-trial upper.
Dependencies: Python3 standard library only. No engine/native imports.
Usage: python3 -B replay.py --case FROZEN_CASE --out NEW_DIRECTORY [--native OWN_NATIVE_A]
The optional native directory is only read to compare retained receipts; all
mathematics and new bounds reconstruct from the frozen public inputs.
"""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dec(x,rounding=None):
 with localcontext() as c:
  c.prec=28
  if rounding:c.rounding=rounding
  return str(Decimal(x.numerator)/Decimal(x.denominator))
def encode(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {k:encode(v)for k,v in x.items()}
 if isinstance(x,list):return [encode(v)for v in x]
 return x

def mat(m):return [[Q(x)for x in row]for row in m]
def eye(n):return [[Q(int(i==j))for j in range(n)]for i in range(n)]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):
 assert len(a[0])==len(b)
 z=[[Q(0)for _ in b[0]]for _ in a]
 bs=[[(j,v)for j,v in enumerate(row)if v]for row in b]
 for i,row in enumerate(a):
  for k,v in enumerate(row):
   if v:
    for j,w in bs[k]:z[i][j]+=v*w
 return z

def add(a,b):return [[x+y for x,y in zip(r,s)]for r,s in zip(a,b)]
def sc(a,c):return [[x*c for x in r]for r in a]
def sub(a,b):return add(a,sc(b,-1))
def tensor(a,b):return [[x*y for x in ar for y in br]for ar in a for br in b]
def zero(a):return all(not x for row in a for x in row)
def trace(a):return sum(a[i][i]for i in range(len(a)))
def gram(a):return mul(tr(a),a)

def polytrim(p):
 while len(p)>1 and not p[-1]:p.pop()
 return p

def polydiff(p):return [i*p[i]for i in range(1,len(p))]or[Q(0)]
def polyrem(a,b):
 a=a[:]
 while len(a)>=len(b)and any(a):
  c=a[-1]/b[-1];k=len(a)-len(b)
  for i,x in enumerate(b):a[k+i]-=c*x
  polytrim(a)
 return a

def polyval(p,x):
 v=Q(0)
 for c in reversed(p):v=v*x+c
 return v

def sturm(p):
 ss=[p,polydiff(p)]
 while any(ss[-1]):
  rr=[-x for x in polyrem(ss[-2],ss[-1])]
  if not any(rr):break
  ss.append(rr)
 return ss

def variation(ss,x):
 signs=[1 if v>0 else -1 for p in ss if (v:=polyval(p,x))]
 return sum(a!=b for a,b in zip(signs,signs[1:]))
def charpoly(a):
 n=len(a);b=eye(n);cs=[Q(1)]
 for k in range(1,n+1):
  ab=mul(a,b);c=-trace(ab)/k;cs.append(c);b=add(ab,sc(eye(n),c))
 return list(reversed(cs))

def placement(C):
 d=read(C/'sources/light/HE3_INDEPENDENT_FRAGMENTS.json');H=d['full_source_H'];J=d['connected_receiving_isometry']
 assert len(H)==192 and all(len(r)==192 for r in H)
 assert len(J)==192 and all(len(r)==48 for r in J)
 cols=[[]for _ in range(48)];selected=[]
 for i,row in enumerate(J):
  nz=[j for j,x in enumerate(row)if x]
  if nz:
   assert len(nz)==1 and row[nz[0]]==1;cols[nz[0]].append(i);selected.append(i)
 assert all(len(x)==1 for x in cols) and len(selected)==48
 h0=[[Q(6 if i==j else -2 if (i^j)in (1,2,4)else 0)for j in range(8)]for i in range(8)]
 for i,row in enumerate(H):
  for j,x in enumerate(row):assert x==((12 if i==j else 0)+(h0[i%8][j%8]if i//8==j//8 else 0))
 # Every8-state block has two connected coordinates at Hamming distance2.
 # Symmetric rank-one channel has equal weights at0,4,8,12; antisymmetric
 # channel has weights0,1/2,1/2,0. No placement complement is deleted.
 projs=[]
 for k in range(4):
  p=eye(8)
  for j in range(4):
   if j!=k:p=sc(mul(p,sub(h0,sc(eye(8),4*j))),Q(1,4*(k-j)))
  projs.append(p)
 for block in range(24):
  ids=[i%8 for i in selected if i//8==block];assert len(ids)==2 and (ids[0]^ids[1]).bit_count()==2
  for k,p in enumerate(projs):
   plus=(p[ids[0]][ids[0]]+p[ids[1]][ids[1]]+2*p[ids[0]][ids[1]])/2
   minus=(p[ids[0]][ids[0]]+p[ids[1]][ids[1]]-2*p[ids[0]][ids[1]])/2
   assert plus==Q(1,4) and minus==([0,Q(1,2),Q(1,2),0][k])
 return dict(full_dimension=192,retained_dimension=48,complement_dimension=144,blocks=24,block_dimension=8,symmetric_spectral_weights=['1/4']*4,antisymmetric_spectral_weights=['0','1/2','1/2','0'],full192_literal_H_and_J_checks='PASS')

def reconstruct_source(C):
 orig=read(C/'sources/light/COLOUR_64_CONSTRUCTION_PAYLOAD.json')['data']['operators'];op={k:mat(v)for k,v in orig.items()};I=eye(64)
 swap=sub(op['I16'],sc(op['Pa16'],2));s12=tensor(op['I4'],swap);s23=tensor(swap,op['I4']);s13=mul(mul(s12,s23),s12);hx=add(add(s12,s23),s13)
 d12=tensor(op['I4'],op['D16']);d23=tensor(op['D16'],op['I4']);r12=tensor(op['I4'],op['R16']);r23=tensor(op['R16'],op['I4']);u=op['U'];ut=tr(u)
 assert gram(u)==sc(eye(4),6)
 for s in (s12,s23,s13):assert s==tr(s) and mul(s,s)==I and zero(add(mul(s,u),u))
 for d,r in ((d12,r12),(d23,r23)):
  assert d==tr(d) and tr(r)==sc(r,-1) and mul(r,u)==mul(d,u) and zero(mul(hx,mul(d,u)))
 x=mul(d12,u);y=mul(d23,u);b=sc(gram(x),Q(1,6));assert gram(y)==gram(x) and mul(tr(x),y)==sc(gram(x),Q(-1,2))
 g4=sc(b,2);assert g4==mat(read(C/'sources/GEN4/volii_quantum_motion_join1_20261016/source/SOURCE_PACKET.json')['G4'])
 g12=add(gram(d12),gram(r12));g23=add(gram(d23),gram(r23));gs=add(g12,g23)
 assert sc(mul(mul(ut,g12),u),Q(1,6))==g4
 assert sc(mul(mul(ut,g23),u),Q(1,6))==g4
 T12=trace(g12);T=trace(gs)
 assert T12*2==T
 polynomial=charpoly(g4);ss=sturm(polynomial)
 t=read(C/'sources/TRIAL_FAMILY.json');intervals=[]
 for r in t['rows'][:4]:
  lo,hi=map(Q,r['g_interval']);assert lo>0 and variation(ss,lo)-variation(ss,hi)==1;intervals.append([lo,hi])
 ordered=sorted(intervals);assert all(a[1]<b[0]for a,b in zip(ordered,ordered[1:]))
 return dict(G12=g12,G23=g23,Gsep=gs,G4=g4,Trace_G12=T12,Trace_Gsep=T,charpoly_G4_ascending=polynomial,source_checks='PASS',source_dimension=64,source_preparation_columns=4,norm_U='6I4',eigenlane_interval_sturm_root_counts=[1]*4)

def st(r):
 aa=[Q(1,1+k*r)for k in range(4)]
 S=sum(aa);T=sum(a*a for a in aa);return S,T

def param(r,eps):
 S,T=st(r);return eps*S/4,S*S/(4*T),eps*r*S/16

def boundary(A,B,eps):
 def f(r):
  d,p,tau=param(r,eps);return A+B*(1-p)-d
 f0=A-eps;finf=A+3*B/4-eps/4
 if f0>=0:return dict(status='NONCERTIFYING',reason='Monotone complete upper is nonnegative already at the connected-support limit.',connected_upper_minus_lower=f0,large_tau_upper_limit=finf,interval=None)
 assert finf>0
 lo=Q(0);hi=Q(1)
 while f(hi)<0:hi*=2
 for _ in range(120):
  mid=(lo+hi)/2
  if f(mid)<0:lo=mid
  else:hi=mid
 dl,pl,tl=param(lo,eps);dh,ph,th=param(hi,eps)
 assert f(lo)<0<=f(hi) and tl<th
 return dict(status='CERTIFIES_CONDITIONAL_INTERVAL',interval='0 < tau < tau_star; unique root of A+B(1-p(tau))-delta(tau)=0',r_star_bracket=[lo,hi],tau_star_bracket=[tl,th],tau_star_bracket_decimal=[dec(tl,ROUND_FLOOR),dec(th,ROUND_CEILING)],f_at_r_bracket=[f(lo),f(hi)],delta_at_r_bracket=[dl,dh],p_at_r_bracket=[pl,ph],connected_upper_minus_lower=f0,large_tau_upper_limit=finf)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--case',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--native',type=Path);a=ap.parse_args();C=a.case.resolve();out=a.out.resolve();assert not out.exists(),'Use a new output directory; retain every attempt.'
 fr=read(C/'FREEZE.json');custody=[]
 for rel,h in fr['files'].items():assert sha(C/rel)==h;custody.append(dict(path=rel,sha256=h))
 src=reconstruct_source(C);place=placement(C);tf=read(C/'sources/TRIAL_FAMILY.json');inter=read(C/'sources/GEN4/volii_dressed_reference1_20261016/joint/INTERFACE.json');old=read(C/'sources/GEN4/volii_dressed_reference1_20261016/joint/ACTUAL_RETURN.json')['matrix']['entries']
 e=Q(tf['epsilon']);delta=3*e;b=Q(tf['b_upper']);mu=Q(tf['mu0']);gam=Q(tf['gamma_gate']);nmax=3*b;T=src['Trace_Gsep'];T12=src['Trace_G12'];assert T==Q(tf['Trace_Gsep']);chi=Q(inter['chi_upper']);fx=Q(inter['actual_Fcross_lower']);pu=2*delta*b-fx;assert pu==Q(inter['paid_kernel_upper']) and 0<pu<mu
 columns=['K','K_dress','paid_self','signed_cross','recoil','quartic','gatevac','gatedress','Pold','Brelax','FfullU','CcrossU','Dmax'];rows=[];tables=[]
 for i,r in enumerate(tf['rows']):
  gl,gu=map(Q,r['g_interval']);K=Q(3,4*int(r['mR']));M=Q(r['mass_majorant_upper'])
  vals=[K,3*e*e*b*K*gu,2*e*e*delta*b*gu,-e*e*fx*gu,3*e*e*M*gu,6*e**4*mu*T*b*gu,4*gam*chi,Q(45,2)*gam*e*e*b*gu]
  A=sum(vals);B=e*e*gu*(mu-pu);F=e*e*gu*3*delta*delta/Q(42)+vals[5];Clo=e*e*mu*gl/(1+e*e*nmax*gl);Cup=e*e*mu*gu*(1+e*e*T12*nmax);Dmax=1+e*e*nmax*gu
  # A signed decomposition is checked coefficientwise. For the negative cross
  # summand, use gu deliberately; the net paid coefficient pu is positive.
  for j,v in enumerate(vals):
   rr=old[i][j]['re'];assert Q(rr['lower'])<=v<=Q(rr['upper'])
  rr=old[i][8]['re'];assert Q(rr['lower'])<=A<=Q(rr['upper'])
  extra=[A,B,F,Cup,Dmax];tables.append(vals+extra)
  ce=boundary(A,B,e)
  rows.append(dict(row=i,mR=r['mR'],lane=r['lane'],g_interval=[gl,gu],norm_interval=[Q(1),Dmax],old_paid_signed_components=dict(zip(columns[:8],vals)),A_complete_connected_upper=A,B_quadratic_relaxation_upper=B,complete_intrinsic_gap_upper='-delta(tau)+A+B*(1-p(tau))',F_full_interval=[Q(0),F],C_cross_interval=[Clo,Cup],F_full_upper_decimal=dec(F),C_cross_interval_decimal=[dec(Clo),dec(Cup)],A_decimal=dec(A),B_decimal=dec(B),intrinsic=ce,positive_gate=dict(status='NONCERTIFYING_ALL_TAU',reason='Upper adds epsilon*p; epsilon*p-delta=tau*(<H>-12)>=0, leaving A+B*(1-p)>0.'),connected_limit_exact_bound_reproduction='PASS'))
 control=[]
 for r in [Q(0),Q(1),Q(16)]:
  d,p,ta=param(r,e)
  control.append(dict(r=r,delta=d,p=p,variance=p*(1-p),variance_payment_intervals=[[p*(1-p)*Q(x['C_cross_interval'][0]),p*(1-p)*Q(x['C_cross_interval'][1])]for x in rows[:4]],interpretation='conditional dimensionless algebra control; no physical tau selected'))
 result=dict(schema='CR2_A_COMPLETE_RETAINED_PAYMENT_RESULT_V1',status='COMPLETE_RIGOROUS_UPPER',independence='Blind single-model A reconstruction from frozen owning definitions; no B, other learner reports or prior A1 payment solution read. Native arithmetic and engine-free replay agree; this is not external verification.',dependencies='Python3 standard library only',case=str(C),epsilon=e,delta_original=delta,n_upper=nmax,b3='1/42',mu0=mu,Trace_G12=T12,Trace_Gsep=T,paid_kernel_upper=pu,source_checks={k:v for k,v in src.items()if not k.startswith('G')},placement_checks=place,bound_definitions=dict(A='K+3 epsilon^2 b K g+epsilon^2 g p_upper+3epsilon^2 M g+6epsilon^4 mu0 Trace(Gsep)b g+4 gamma chi_upper+(45/2)gamma epsilon^2 b g',B='epsilon^2 g_upper*(mu0-p_upper)',F_full='[epsilon^2 g(p_kernel-Delta*n)+epsilon^4 C1_full]/D',C_cross='epsilon^2 mu0*(g+epsilon^2 <T1|G12|T1>)/D',D='1+epsilon^2 n g',relaxed_gap_upper='-delta(tau)+A+B*(1-p(tau))',positive_gate_gap_upper='-delta(tau)+epsilon*p(tau)+A+B*(1-p(tau))',secular='delta=(epsilon/4)sum_{k=0}^3 1/(1+k*r), tau=epsilon*r*sum_{k=0}^3 1/(1+k*r)/16',p='p=(sum a_k)^2/(4 sum a_k^2), a_k=1/(1+k*r)'),rows=rows,scalar_mean_controls=control,remaining_inputs=dict(mathematical_certificate='No missing operand for this conservative complete bound.',exact_values='Exact continuum n and contracted one-boson CT moments would sharpen the field/C_cross enclosures and tau endpoints; they were bounded without changing the trial.',physical_assignment='Tau, physical source/colour/species/action/ruler map and any changed signed ledger remain receiving inputs.'),freeze_custody=custody)
 if a.native:
  N=a.native.resolve();checks=[]
  native_sources=[('000_cross_self_full64.output.json','G12'),('001_internal_self_full64.output.json','G23'),('002_sum_self_full64.output.json','Gsep'),('005_contact_norm4.output.json','G4')]
  for f,k in native_sources:
   p=N/'attempt_001'/f;assert mat(read(p)['matrix'])==src[k];checks.append(dict(path=str(p),sha256=sha(p),check='exact matrix equality'))
  for f,v in [('003_cross_trace_full64.output.json',T12),('004_sum_trace_full64.output.json',T)]:
   p=N/'attempt_001'/f;assert mat(read(p)['matrix'])==sc(eye(64),v);checks.append(dict(path=str(p),sha256=sha(p),check='exact native trace equality'))
  p=N/'attempt_002/000_payment_coefficients12.output.json';assert mat(read(p)['matrix'])==tables;checks.append(dict(path=str(p),sha256=sha(p),check='all156 exact bound coefficients agree'))
  for f,n in [('000_strict_contact_source_Gram.output.json',4),('001_strict_positive_projector_Gram.output.json',64)]:
   p=N/'attempt_003'/f;assert mat(read(p)['matrix'])==sc(eye(n),0);checks.append(dict(path=str(p),sha256=sha(p),check='strict sum of positive source defect Grams is zero'))
  p=N/'attempt_003/002_literal_source_G4.output.json';assert mat(read(p)['matrix'])==src['G4'];checks.append(dict(path=str(p),sha256=sha(p),check='literal source G4 exact semantic native check'))
  for d in ('attempt_001','attempt_002','attempt_003'):
   p=N/d/'CR2_EXECUTION_RECEIPT.json';assert read(p)['status']=='PASSED';checks.append(dict(path=str(p),sha256=sha(p),check='native receipt passed'))
  result['native_comparisons']=checks
 out.mkdir(parents=True);(out/'RESULTS.json').write_text(json.dumps(encode(result),indent=2)+'\n');(out/'SOURCE_REPLAY.json').write_text(json.dumps(encode(src),indent=2)+'\n');(out/'PAYMENT_TABLE.json').write_text(json.dumps(encode(dict(columns=columns,entries=tables)),indent=2)+'\n')
 summary=[]
 for r in rows:
  interval=r['intrinsic'].get('tau_star_bracket_decimal');summary.append(dict(row=r['row'],mR=r['mR'],lane=r['lane'],A=dec(r['A_complete_connected_upper']),B=dec(r['B_quadratic_relaxation_upper']),status=r['intrinsic']['status'],tau_endpoint=interval))
 (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2));print('Exact replay PASS:',out)
if __name__=='__main__':main()
