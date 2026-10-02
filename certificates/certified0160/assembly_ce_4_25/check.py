#!/usr/bin/python3
"""Delivery checks including complete LIVE proof execution. Not a new theorem.
All mathematical lines actually run. No accepted-only hold is silently waived;
the new constructive witness is checked separately and subjected to mutations.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,subprocess,sys,copy,ast
import release_gate as rg
import verify as delivery
import recovery_live as live_adapter
COUNT=0;mutations=[]


def ck(ok,label):
    global COUNT
    COUNT+=1
    if not bool(ok):raise AssertionError(label)

def dump(n,o):Path(n).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')

def agree(c,e,s):
    one=rg.cut_primary(c,e,s);two=rg.cut_secondary(c,e,s)
    ck(not one['invalid_snapshot'],'test inventory well formed')
    ck(one['missing']==two['missing'] and one['ready']==two['ready'] and one['covered']==two['covered'],'two accepted-audit relation algorithms')
    return one

def rejected(c,e,s,label):
    ck(not agree(c,e,s)['ready'],label);mutations.append(label)

frozen=delivery.pinned_inputs()
snap=rg.load('BANK_SNAPSHOT.json');contract=rg.load('RELEASE_CONTRACT.json');edges=rg.load('AUDIT_EDGES.json')['edges']
ck(rg.snapshot_well_formed(snap),'captured accepted bank grammar not authority from hashes')
for z in rg.load('ORIGINS.json'):ck(z['sha256']==rg.sha(z['local']),'local accepted input identity')
ck(len([z for z in rg.load('ORIGINS.json') if z['local'].startswith('math/')])==54,'all original math files unchanged')
for z in rg.load('frozen/ACCEPTED_SOURCE_TEXTS.json')['sources']:
    ck(hashlib.sha256(z['text'].encode()).hexdigest()==z['sha256'],'inert accepted source identity')
# All target roles and obligation clauses remain, even though the witness type
# for recovery is strengthened from historical absence to constructive replay.
ck(rg.required_roles_intact(contract),'literal selected roles')
for omitted in contract['required']:
    a=copy.deepcopy(contract);a['required'].pop(omitted)
    ck(not rg.required_roles_intact(a),'cannot drop required role '+omitted);mutations.append('drop_role_'+omitted)

cal=rg.load('CALIBRATIONS.json');c=cal['contract'];es=cal['edges']
ck(agree(c,es,snap)['ready'],'known675_676_684 regime')
for role in c['required']:
    ck(agree({'required':{role:c['required'][role]}},es,snap)['ready'],'known distinct '+role)
subsets=[]
for mask in range(1<<len(es)):
    used=[e for j,e in enumerate(es) if mask&(1<<j)];ans=agree(c,used,snap)
    expect=sorted(role for role,req in c['required'].items() if not any(e['target']==req['target'] for e in used))
    ck(ans['missing']==expect and ans['ready']==(mask==7),'complete legacy subset table')
    subsets.append({'mask':mask,'missing':ans['missing'],'ready':ans['ready']})
for j,e in enumerate(es):
    for item in e['obligations']:
        a=copy.deepcopy(es);a[j]['obligations'].remove(item)
        rejected(c,a,snap,'missing legacy scope '+str(e['audit'])+' '+item)
    for key,value in [('target',767),('target_fact_sha256',snap['facts']['767']['fact_sha256']),('target_proof_sha256','0'*64),('audit_fact_sha256','0'*64),('audit',789)]:
        a=copy.deepcopy(es);a[j][key]=value;rejected(c,a,snap,'wrong legacy '+str(e['audit'])+' '+key)
    a=copy.deepcopy(es);a[j]['audit']=e['target'];a[j]['audit_fact_sha256']=snap['facts'][str(e['target'])]['fact_sha256']
    rejected(c,a,snap,'self audit '+str(e['target']))
    a=copy.deepcopy(es);a[j]['audit']=10**6;a[j]['status']='accepted';a[j]['exit']=0
    rejected(c,a,snap,'uncaptured accepted flag '+str(e['target']))
    a=copy.deepcopy(es);a[j]['obligations']=e['obligations'][:1]
    other=copy.deepcopy(es[j]);other['obligations']=e['obligations'][1:];a.append(other)
    rejected(c,a,snap,'partial scopes not one complete audit '+str(e['target']))
# Accepted795 does not qualify recovery774, nor789 composition/recovery.
current_accepted=agree(contract,edges,snap)
ck(current_accepted['missing']==['recovery774'],'accepted-only cut is honest')
for edge in edges:
    req=contract['required']['recovery774'];fake=copy.deepcopy(edge)
    fake.update({'target':774,'target_fact_sha256':req['target_fact_sha256'],'target_proof_sha256':req['target_proof_sha256'],'obligations':req['obligations']})
    ck(agree(contract,edges+[fake],snap)['missing']==['recovery774'],'no accepted audit promotion')
    mutations.append('no_promotion_'+str(edge['audit']))
for flag,value in [('candidate_release','READY'),('all_accepted',True),('pending_result','ALL PASS')]:
    a=copy.deepcopy(contract);a[flag]=value
    ck(agree(a,edges,snap)['missing']==['recovery774'],'decorations are not witnesses');mutations.append('ignored_'+flag)

# New LIVE binding: every banked input statement exactly agrees with own
# captured bank_ref. This does not grant acceptance to the external source.
spec=rg.load('RECOVERY_LIVE.json');files=spec['files']
def member(n):
    e=files[n];return e['text'].encode() if 'text' in e else Path(e['local_file']).read_bytes()
for n,e in files.items():
    ck(hashlib.sha256(member(n)).hexdigest()==e['sha256'],'full LIVE source identity '+n)
    ck(len(member(n))==e['bytes'],'full LIVE member length '+n)
cits=json.loads(member('CITATIONS.json'))
for k,z in cits.items():
    ck(z['fact']==snap['facts'][k]['fact'] and z['fact_sha256']==snap['facts'][k]['fact_sha256'],'LIVE bank input '+k)
ck(set(n for n in files if n.endswith('.py'))=={'check.py','audit_primary.py','audit_secondary.py','controls.py'},'complete original executable inventory')
ck(spec['source_transformations']==[] and not spec['uses_bank_acceptance_of_this_source'],'no rewrite/no acceptance promotion')
for n in ['check.py','audit_primary.py','audit_secondary.py','controls.py']:
    tree=ast.parse(member(n).decode())
    ck(bool(tree.body),'complete source parses '+n)
    ck(not any(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id in ('exec','eval','__import__') for x in ast.walk(tree)),'no dynamic source import '+n)

# Execute the REAL record entry point. It must run all mathematics and every
# independent recovery worker before reaching any RECORD emission.
p=subprocess.run([sys.executable,'verify.py'],capture_output=True,text=True,timeout=750)
Path('record_gate.log').write_text(p.stdout);Path('record_gate_stderr.log').write_text(p.stderr)
ck(p.returncode==0 and not p.stderr,'complete record success')
rl=[z for z in p.stdout.splitlines() if z.startswith('RECORD_')]
ck(rl==['RECORD_LAMBDA_UPPER = 4/25','RECORD_T_LO = 4/25','RECORD_T_HI = 3/16','RECORD_ANCHOR = 3/16','RECORD_X = 6000000185827'],'all5 independent header lines')
ck(p.stdout.splitlines().count('RESULT: ALL PASS')==1 and p.stdout.count('COVER module=')==3,'result/coverage cardinality')
r=rg.load('RELEASE_RESULT.json');w=rg.load('LIVE_EXECUTION.json');math=rg.load('math/RESULT.json')
ck(r['candidate_release']=='CONSTRUCTIVE_COMPLETE' and not r['candidate_accepted'],'proposal not acceptance')
ck(r['accepted_only_qualification']['cut']['missing']==['recovery774'],'retain distinction between witness types')
ck(r['constructive_qualification']['ready'] and not r['constructive_qualification']['missing'],'complete constructive cut')
ck(math['checks']==156550 and math['second_checks']==435,'unchanged arithmetic checks')
ck(w['checks']==1701309 and r['live_recovery_checks']==w['checks'],'all independent original workers')
ck(rg.live_witness_matches(w,contract),'actual returned LIVE witness matches')
# Replay quantitative-interface checker on every newly created product.
root=Path('live_recovery_runtime')
primary=json.loads((root/'PRIMARY_AUDIT.json').read_text());secondary=json.loads((root/'SECONDARY_AUDIT.json').read_text());control=json.loads((root/'CONTROL_AUDIT.json').read_text())
ck(live_adapter.check_summary(w['summary'],primary,secondary,control,spec,root),'complete quantitative LIVE interface')
# Active witness mutations; these are representation controls, not claimed
# proofs of arbitrary runtime freshness. Freshness is actual execution above.
for key,value in [('witness_type','ACCEPTED_AUDIT'),('author','prover_astra-s31'),('target',786),('target_fact_sha256','0'*64),('target_proof_sha256','0'*64),('capsule_sha256','0'*64),('source_transformations',['delete_worker']),('execution_exit',1),('fresh_complete_execution',False),('bank_acceptance_asserted',True),('products',{}),('input_sha256',{})]:
    a=copy.deepcopy(w);a[key]=value
    ck(not rg.live_witness_matches(a,contract),'LIVE rejects '+key);mutations.append('live_'+key)
for key,val in [('complete_raw_cells',690987),('complete_weight_cells',157939),('positive_bins',223),('original_leaves',13),('original_scalar_slots',276)]:
    a=copy.deepcopy(w);a['summary'][key]=val
    ck(not rg.live_witness_matches(a,contract),'incomplete LIVE '+key);mutations.append('incomplete_'+key)
for key,val in [('entry_count',1609010),('t_closed',['159/1000','3/16']),('x_closed',[6000000185827,66476100549960]),('terminal2300000','CLOSED')]:
    a=copy.deepcopy(w);a['summary']['coverage'][key]=val
    ck(not rg.live_witness_matches(a,contract),'LIVE scope '+key);mutations.append('live_scope_'+key)
# All subsets of the THREE current proofs. Only the full constructive set
# succeeds; the accepted-only pair explicitly remains incomplete.
current_subsets=[]
for mask in range(8):
    used=[edges[j] for j in range(2) if mask&(1<<j)]
    ans=agree(contract,used,snap)
    base={'cut':ans};live_w=w if mask&4 else {}
    out=rg.constructive_cut(base,live_w,contract)
    ck(out['ready']==(mask==7),'complete current constructive truth table')
    current_subsets.append({'mask':mask,'ready':out['ready'],'missing':out['missing']})
# Deleting a scope clause from an accepted input cannot be repaired by LIVE774.
for j,e in enumerate(edges):
    for item in e['obligations']:
        a=copy.deepcopy(edges);a[j]['obligations'].remove(item)
        ans=agree(contract,a,snap);out=rg.constructive_cut({'cut':ans},w,contract)
        ck(not out['ready'],'current accepted missing scope '+item);mutations.append('current_scope_'+str(e['audit'])+'_'+item)

out={'name':'CE_GRAM_CONSTRUCTIVE_RECORD_DELIVERY','snapshot':796,'target_memory':786,
 'record_exit':p.returncode,'record_lines':len(rl),'record_arithmetic':r['arithmetic'],
 'accepted_witnesses':{'complete_source767':789,'composition786':795},'live_witness':'functional_astra-s27 COMPLETE execution; not a bank citation',
 'accepted_only_missing':['recovery774'],'constructive_missing':[],
 'math_primary_checks':math['checks'],'math_second_checks':math['second_checks'],'live_checks':w['checks'],
 'legacy_subsets':subsets,'current_proof_subsets':current_subsets,'adverse_rejections':mutations,
 'adverse_count':len(mutations),'checks':COUNT,'candidate_acceptance_asserted':False,'publication_approved':False}
dump('CHECK_RESULT.json',out)
print('COMPLETE_RECORD_EXIT',p.returncode,'RECORD_LINES',len(rl),'COVER_BOXES',3)
print('TARGET_SCORE EXACT',r['arithmetic']['lambda_upper'],'FLOOR10',r['arithmetic']['FLOOR10'],'CEIL10',r['arithmetic']['CEIL10'])
print('ACCEPTED_789_SOURCE767 ACCEPTED_795_COMPOSITION786 LIVE_COMPLETE_RECOVERY774')
print('LIVE_RAW',690988,'WEIGHTS',157940,'POSITIVE_BINS',224,'LEAVES',14,'SCALAR_SLOTS',277,'ENTRANTS',1609011)
print('MATH_CHECKS',math['checks'],math['second_checks'],'LIVE_CHECKS',w['checks'])
print('LEGACY_SUBSETS',len(subsets),'CONSTRUCTIVE_SUBSETS',len(current_subsets),'ADVERSE_REJECTIONS',len(mutations))
print('CHECKS',COUNT)
print('RESULT: ALL PASS')
