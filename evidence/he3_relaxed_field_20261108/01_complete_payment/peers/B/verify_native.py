#!/usr/bin/env python3
"""Host readback of native receipts against separately authored replay outputs."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
K=Path('/home/lilhelper/SAM_Research_Overflow/ironclad/campaigns/he3_relaxed_field_cr2_20261108');O=K/'peers/B';N=K/'native/B/attempt_03';R=O/'replay_attempt_02'
def rd(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
report=rd(N/'EXECUTION.json');assert report['status']=='PASSED'
proofs=[]
for step in report['trace']:
 for kind in ['input','output']:assert sha(N/step[kind])==step[kind+'_sha256']
 assert all(c['passed'] for c in step['checks']);proofs.append({'id':step['id'],'operation':step['operation'],'input':str(N/step['input']),'input_sha256':step['input_sha256'],'output':str(N/step['output']),'output_sha256':step['output_sha256'],'checks':step['checks']})
source=rd(R/'SOURCE_OPERATORS.json');matches={}
for file,key in [('000_full_cross_gram.output.json','Gcross'),('001_full_total_gram.output.json','Gtotal'),('002_vacuum_cross_metric.output.json','vacuum_G4')]:
 actual=rd(N/file)['matrix'];matches[key]=actual==source[key];assert matches[key]
for file in ['003_positive_swap_contract.output.json','004_trial_source_contract.output.json']:
 x=rd(N/file);assert x['rank']==0 and all(F(v)==0 for row in x['matrix'] for v in row);matches[file]=True
m=rd(N/'005_refined_complete_bound_table.output.json')['result']['output']['matrix'];res=rd(R/'RESULTS.json');comparisons=[]
keys=['original_formula_paid_upper','refined_complete_paid_upper','full_field_bounds','cross_self_CT_bounds','norm_bounds']
for i,row in enumerate(res['rows']):
 vals=[F(row['original_formula_paid_upper']),F(row['refined_complete_paid_upper']),F(row['full_field_bounds'][1]),F(row['cross_self_CT_bounds'][1]),F(row['norm_bounds'][1]),F(row['terms']['packet_kinetic']),F(res['epsilon'])**2*F(res['mu0'])*F(row['g_interval'][1])]
 for j,q in enumerate(vals):
  entry=m['entries'][i][j];assert entry['im']=={'lower':'0','upper':'0'};lo=F(entry['re']['lower']);hi=F(entry['re']['upper']);assert lo<=q<=hi,(i,j)
 comparisons.append({'row':i,'all7_exact_replay_values_in_native_enclosures':True})
audit=dict(schema='CR2_B_NATIVE_REPLAY_READBACK_V1',status='PASSED',scope='Source matrix equality and exact rational upper-endpoint arithmetic checked against retained native enclosures; same-model separate-code work, not external verification.',native_execution=str(N/'EXECUTION.json'),native_execution_sha256=sha(N/'EXECUTION.json'),native_CR2_receipt=rd(N/'CR2_EXECUTION_RECEIPT.json'),source_matches=matches,all12_rows=comparisons,steps=proofs,engine_modified=False)
wr(O/'NATIVE_REPLAY_COMPARISON.json',audit)
res['native_provenance']={'execution_receipt':str(N/'CR2_EXECUTION_RECEIPT.json'),'execution_sha256':sha(N/'EXECUTION.json'),'comparison':str(O/'NATIVE_REPLAY_COMPARISON.json'),'comparison_sha256':sha(O/'NATIVE_REPLAY_COMPARISON.json'),'all12_exact_replay_values_in_native_enclosures':True,'core':'0.11.3','SLC':'SLC-GEN5-R1','scope':'CR2_SOURCE_BOUND_CALCULATION_NO_DUCK_WINDOW'}
wr(O/'RESULTS.json',res)
print(json.dumps({'status':'PASSED','source_matches':matches,'rows':len(comparisons)},indent=2))
