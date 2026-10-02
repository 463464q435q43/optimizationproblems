#!/usr/bin/python3
"""Constructive release boundary. Accepted audits and COMPLETE LIVE proofs are distinct.

Facts are consumed from the captured accepted bank snapshot. A package digest
checks integrity only. The independent verifier authenticates both bank status
and the manually encoded audit-to-target semantic bindings.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json


def load(name):
    p=Path(name)
    if p.is_absolute() or '..' in p.parts: raise ValueError('nonlocal input')
    return json.loads(p.read_text())


def sha(path):
    p=Path(path)
    if p.is_absolute() or '..' in p.parts: raise ValueError('nonlocal hash input')
    return hashlib.sha256(p.read_bytes()).hexdigest()


def snapshot_well_formed(snapshot):
    facts=snapshot['facts']
    return all(int(k)==v['line'] and int(k)<=snapshot['entries']
               and v['kind']=='fact'
               and hashlib.sha256(v['fact'].encode()).hexdigest()==v['fact_sha256']
               and ((v['verifier']['mode']=='v1_import' and int(k)<581)
                    or (v['verifier']['mode']=='check+llm'
                        and v['verifier']['check']['exit']==0))
               for k,v in facts.items())


def matching_edge(requirement,edge,facts):
    """Check a compiled audit implication, not merely its status label."""
    try:
        target=facts[str(requirement['target'])]
        audited=facts[str(edge['audit'])]
        admitted=load('QUALIFICATION_BINDINGS.json').get(str(edge['audit']))
        if admitted is None or any(edge.get(k)!=v for k,v in admitted.items()):return False
        return (edge['target']==requirement['target']
            and edge['target_fact_sha256']==requirement['target_fact_sha256']==target['fact_sha256']
            and edge['target_proof_sha256']==requirement['target_proof_sha256']
            and edge['audit_fact_sha256']==audited['fact_sha256']
            and audited['line']>=target['line']
            and audited['seat']!=target['seat']
            and audited['kind']=='fact'
            and audited['verifier']['mode']=='check+llm'
            and audited['verifier']['check']['exit']==0
            and set(requirement['obligations']).issubset(edge['obligations']))
    except (KeyError,TypeError,ValueError):
        return False


def cut_primary(contract,edge_list,snapshot):
    """Direct existential matching per required target, then universal AND."""
    if not snapshot_well_formed(snapshot): return {'invalid_snapshot':True,'missing':sorted(contract['required']),'ready':False}
    facts=snapshot['facts'];covered={};missing=[]
    for name,req in sorted(contract['required'].items()):
        witnesses=[e['audit'] for e in edge_list if matching_edge(req,e,facts)]
        covered[name]=sorted(set(witnesses))
        if not witnesses:missing.append(name)
    return {'covered':covered,'missing':missing,'ready':not missing,'invalid_snapshot':False}


def cut_secondary(contract,edges,snapshot):
    """Independent atom set-subtraction implementation; no matching_edge call."""
    obligations=set()
    for role,req in contract['required'].items():
        for item in req['obligations']:
            obligations.add((role,req['target'],req['target_fact_sha256'],req['target_proof_sha256'],item))
    # Keep all atoms of each role tied to ONE accepted audit, never combine
    # two partial audits without a separately justified compiled implication.
    valid=[];facts=snapshot['facts']
    for edge in edges:
        if str(edge.get('audit')) not in facts or str(edge.get('target')) not in facts:continue
        au=facts[str(edge['audit'])];ta=facts[str(edge['target'])]
        if au.get('kind')!='fact' or au['seat']==ta['seat'] or au['line']<ta['line']:continue
        if au['verifier']['mode']!='check+llm' or au['verifier']['check']['exit']!=0:continue
        admitted=load('QUALIFICATION_BINDINGS.json').get(str(edge['audit']))
        if admitted is None:continue
        if any(edge.get(k)!=admitted[k] for k in admitted):continue
        if edge.get('audit_fact_sha256')!=au['fact_sha256'] or edge.get('target_fact_sha256')!=ta['fact_sha256']:continue
        atoms={(name,edge['target'],edge['target_fact_sha256'],edge.get('target_proof_sha256'),item)
               for name in contract['required'] for item in edge.get('obligations',[])}
        valid.append((edge['audit'],atoms))
    remaining=set(obligations);witnesses={}
    for role in sorted(contract['required']):
        needed={a for a in obligations if a[0]==role};witnesses[role]=[]
        for audit,atoms in valid:
            if needed and not (needed-atoms):
                remaining-=needed;witnesses[role].append(audit)
    return {'missing':sorted({a[0] for a in remaining}),'covered':{k:sorted(set(v)) for k,v in witnesses.items()},'ready':not remaining,'atom_count':len(obligations)}


def verify_source789(snapshot,edge_list):
    """Boundary replays for the only new accepted release qualification.
    The full source proof remains memory789, not the sampled checks here.
    """
    au=load('frozen/external789_SUMMARY.json');co=load('frozen/external789_COMPLETE_RESULTS.json');le=load('frozen/external789_LEAF_RESULTS.json')
    assert au['target']==767 and au['name']=='EXTERNAL_COMPLETE_GRAM_SOURCE_AUDIT'
    assert au['snapshot']==779 and au['closed_leaves']==3524 and au['gram_threshold']=='1/1000000'
    assert au['source_floor']=='1/10' and not au['found_load_bearing_discrepancy']
    assert not au['memory774_transport_audited'] and not au['memory777_transport_audited']
    assert not au['official_attestation'] and not au['physical_cover_export']
    assert au['local_physical_scope']['source_t']=='4/25' and au['local_physical_scope']['source_x']==6000000185827
    assert au['local_physical_scope']['source_N']==690988 and au['local_physical_scope']['source_y']==0
    assert co['both_original_lines_compared'] and co['raw']==690988 and co['rough']==157939 and co['inverse']==53 and co['fourier_support']==132901
    accepted={}
    for line in Path('math/frozen/bank767_outputs.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        dg,name=line.split();accepted[name]=dg
    for role,original in [('raw','raw'),('weights','weights'),('inverse','inverse'),('fourier','fourier')]:
        key='primary_'+original+'.txt';alt='secondary_'+original+'.txt'
        assert co['products'][role]['both_original_lines_equal']
        assert co['products'][role]['sha256']==accepted[key]==accepted[alt]
        assert co['products'][role]['count']==au['original_coefficients'][role]
    assert le['coverage']['closed_boxes']==3524 and le['coverage']['all_faces_closed'] and F(le['coverage']['sum_exact_volume'])==1
    assert le['jet_tables']['primary']['count']==le['jet_tables']['secondary']['count']==123340
    own=le['minimum_expressions']['own'];assert F(own['lo'])>F(1,1000000) and F(own['hi'])>=F(own['lo'])
    assert not any(e['target']!=767 for e in edge_list if e['audit']==789)
    assert snapshot['facts']['789']['seat']=='numerics_astra'
    return {'source_qualified_by':789,'target':767,'raw_terms':co['raw'],'weights_including_synthetic':co['products']['weights']['count'],'closed_source_leaves':3524,'transport774_audited':False,'composition786_audited':False,'full_source_rerun_here':False}


def required_roles_intact(contract):
    """Concrete selected-release obligation set; cannot drop a held role."""
    return (contract.get('policy')=='EXACT_ACCEPTED_AUDIT_OR_COMPLETE_LIVE_INDEPENDENT_PROOF'
            and contract.get('live_role')=='recovery774'
            and contract.get('selected_mathematical_target')==786
            and sorted(contract.get('required',{}))==['complete_source767','composition786','recovery774'])


def verify_composition795():
    au=load('frozen/external795_SUMMARY.json');nu=load('frozen/external795_NUMERICAL.json');lo=load('frozen/external795_LOGICAL.json')
    math=load('math/RESULT.json')
    assert au['name']=='EXTERNAL_GRAM_GLOBAL_COMPOSITION_AUDIT' and au['target_memory']==786
    assert au['target_assembly_sha256']==sha('math/ASSEMBLY.md') and au['target_snapshot']==777
    assert au['source_external_audit']==789 and not au['separate_complete_recovery774_external_audit_supplied']
    assert not au['found_load_bearing_discrepancy'] and not au['record_package_audited'] and not au['official_attestation']
    assert au['closed_positive_boxes']==3 and au['missing_components']==au['excess_components']==0
    assert au['complete_counts']==nu['complete_input_counts']=={'entrants':1609011,'leaves':14,'rough_bins':224,'rough_fibres':157939}
    assert F(au['finite_surplus'])==F(math['exact']['surplus'])>F(1,2000)
    assert F(au['tail_squared_reserve'])==F(math['exact']['tail_jet'])>F(9,1000)
    assert all(nu['exact'][k]==v for k,v in math['exact'].items())
    assert lo['complete_real_axis_reflection'] and lo['missing_components']==lo['excess_components']==0
    assert lo['positive_boxes']==3 and lo['target_direct_citations']==21
    assert lo['recovery_external_audit']=='not supplied by this artifact' and not lo['record_acceptance']
    assert au['initial_RH']==lo['initial_RH']
    for key in ['height','margin','required']:
        expect={'height':'3000175332800','margin':'350479773/2','required':'6000000185827/2'}[key]
        assert F(au['initial_RH'][key])==F(expect)
    # Compare every accepted external leaf interval to the freshly recomputed
    # original composition expression, not only its displayed minimum.
    assert len(nu['leaves'])==len(math['leaves'])==14
    for n,m in zip(nu['leaves'],math['leaves']):
        assert (n['L'],n['U'])==(m['L'],m['U'])
        assert F(n['retained_lower_expression']['lo'])>F(1,100)
        assert F(m['retained_lower_expression']['lo'])>F(1,100)
        assert F(n['retained_lower_expression']['lo'])<=F(m['retained_lower_expression']['hi'])
        assert F(m['retained_lower_expression']['lo'])<=F(n['retained_lower_expression']['hi'])
    return {'audit':795,'target':786,'complete_recovery774_audit':False,'record_acceptance':False,'original_citations':21,'leaf_comparisons':14}


def current_cut():
    snapshot=load('BANK_SNAPSHOT.json');contract=load('RELEASE_CONTRACT.json');edge_doc=load('AUDIT_EDGES.json')
    assert snapshot['entries']==796 and edge_doc['snapshot']==796
    assert required_roles_intact(contract)
    for req in contract['required'].values():
        assert sha(req['target_proof'])==req['target_proof_sha256']
        assert snapshot['facts'][str(req['target'])]['fact_sha256']==req['target_fact_sha256']
    assert sha('RECOVERY_LIVE.json')==contract['live_source_manifest_sha256']
    source=verify_source789(snapshot,edge_doc['edges']);composition=verify_composition795()
    one=cut_primary(contract,edge_doc['edges'],snapshot);two=cut_secondary(contract,edge_doc['edges'],snapshot)
    assert not one['invalid_snapshot'] and one['missing']==two['missing'] and one['ready']==two['ready'] and one['covered']==two['covered']
    assert one['missing']==['recovery774'] and not one['ready']
    return {'snapshot':796,'cut':one,'secondary_atoms':two['atom_count'],'source_boundary':source,'composition_boundary':composition,'scope':'accepted-only exact supplied inventory; recovery proof must actually execute LIVE'}


def live_witness_matches(witness,contract):
    # Called only with the in-memory result returned by execute(), never with
    # a configurable JSON flag or an unexecuted stored summary. Program flow
    # and complete replay, not this finite predicate, supply freshness.
    try:
        req=contract['required']['recovery774']; spec=load('RECOVERY_LIVE.json')
        return (witness['witness_type']=='COMPLETE_LIVE_INDEPENDENT_PROOF'
            and witness['author']==contract['live_author']==spec['author']
            and witness['target']==774==req['target']
            and witness['target_fact_sha256']==req['target_fact_sha256']==spec['target_fact_sha256']
            and witness['target_proof_sha256']==req['target_proof_sha256']==spec['target_proof_sha256']
            and witness['capsule_sha256']==contract['live_source_manifest_sha256']==sha('RECOVERY_LIVE.json')
            and witness['source_transformations']==[] and witness['execution_exit']==0
            and witness['fresh_complete_execution'] and not witness['bank_acceptance_asserted']
            and set(witness['products'])==set(spec['generated_products'])
            and witness['input_sha256']=={n:e['sha256'] for n,e in spec['files'].items()}
            and witness['summary']['complete_raw_cells']==690988
            and witness['summary']['complete_weight_cells']==157940
            and witness['summary']['positive_bins']==224
            and witness['summary']['original_leaves']==14
            and witness['summary']['original_scalar_slots']==277
            and witness['summary']['coverage']['entry_count']==1609011
            and witness['summary']['coverage']['t_closed']==['4/25','3/16']
            and witness['summary']['coverage']['x_closed']==[6000000185827,66476100549959]
            and witness['summary']['coverage']['terminal2300000']=='OPEN')
    except (KeyError,TypeError,ValueError):return False


def constructive_cut(accepted,witness,contract):
    missing=list(accepted['cut']['missing']); witnesses=dict(accepted['cut']['covered'])
    if live_witness_matches(witness,contract):
        missing.remove('recovery774');witnesses['recovery774']=['COMPLETE_LIVE:functional_astra-s27']
    # Independent set subtraction for the two disjoint witness types.
    requirements=set(contract['required']); covered={r for r,v in accepted['cut']['covered'].items() if v}
    if live_witness_matches(witness,contract):covered.add('recovery774')
    assert set(missing)==requirements-covered
    return {'missing':sorted(missing),'ready':not missing,'witnesses':witnesses,
            'live_bank_acceptance_asserted':False,'historical_accepted_only_policy_unchanged':False,
            'policy':'EXACT_ACCEPTED_AUDIT_OR_COMPLETE_LIVE_INDEPENDENT_PROOF'}


def floor_trunc(q,d):
    q=F(q);return q.numerator*10**d//q.denominator


def ceil_trunc(q,d):return -floor_trunc(-F(q),d)


def fixed(n,d):return ('-' if n<0 else '')+str(abs(n)//10**d)+'.'+str(abs(n)%10**d).zfill(d)


def record_arithmetic():
    assert (floor_trunc(F(-1,3),5),ceil_trunc(F(-1,3),5))==(-33334,-33333)
    assert (floor_trunc(F(-1,10**8),5),ceil_trunc(F(-1,10**8),5))==(-1,0)
    a,b,X,T=F(4,25),F(3,16),F(6000000185827),F(3000175332800)
    assert 0<a<b<=F(1,2) and F(21,125)+F(39,2000)==b
    assert T-X/2==F(350479773,2)>0 and F(33,200)-a==F(1,200)
    return {'lambda_upper':str(a),'t_lo':str(a),'t_hi':str(b),'anchor_upper':str(b),'X':str(X),'RH_height':str(T),'RH_margin':str(T-X/2),'gain':str(F(33,200)-a),'FLOOR10':fixed(floor_trunc(a,10),10),'CEIL10':fixed(ceil_trunc(a,10),10)}
