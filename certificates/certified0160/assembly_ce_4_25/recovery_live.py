#!/usr/bin/python3
"""Storage-only adapter for the COMPLETE independently authored recovery proof.
It never treats a stored result, audit-status flag or uncaptured bank fact as a
proof. Exact external source bytes are materialized locally and all original
workers execute in every record invocation with inherited confinement.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,subprocess,sys,re,ast


def digest(data):return hashlib.sha256(data).hexdigest()
def safe(name):
    p=Path(name)
    if p.is_absolute() or '..' in p.parts or not p.parts:raise AssertionError('nonlocal LIVE path')
    return p

def read(name):return json.loads(safe(name).read_text())

def materialize(spec):
    assert spec['mode']=='COMPLETE_LIVE_INDEPENDENT_PROOF'
    assert spec['author']=='functional_astra-s27' and spec['target_memory']==774
    assert spec['source_transformations']==[] and not spec['uses_bank_acceptance_of_this_source']
    assert spec['workers']==['audit_primary.py','audit_secondary.py','controls.py'] and spec['entry_point']=='check.py'
    assert len(spec['files'])==46
    root=Path('live_recovery_runtime');root.mkdir(exist_ok=True)
    # Never retain a previous generated mathematical product as an input.
    for name in spec['generated_products']:
        p=root/safe(name)
        if p.exists():p.unlink()
    got={}
    for name,entry in sorted(spec['files'].items()):
        assert ('text' in entry)!=('local_file' in entry)
        data=entry['text'].encode() if 'text' in entry else safe(entry['local_file']).read_bytes()
        assert len(data)==entry['bytes'] and digest(data)==entry['sha256']
        p=root/safe(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        assert digest(p.read_bytes())==entry['sha256'];got[name]=entry['sha256']
    # The original sealed manifest is retained unchanged and checked in full.
    original=json.loads((root/'RELEASE_PINS.json').read_text())
    assert set(got)==set(original)|{'RELEASE_PINS.json'}
    assert all(got[n]==h for n,h in original.items())
    assert digest((root/'AUDIT.md').read_bytes())==digest(Path('LIVE_RECOVERY_PROOF.md').read_bytes())
    assert digest((root/'ARITHMETIC.md').read_bytes())==digest(Path('LIVE_RECOVERY_ARITHMETIC.md').read_bytes())
    # Source inspection is an integrity regression, not a replacement for the
    # official confinement run. The original script uses same-interpreter -B.
    for name in ['check.py']+spec['workers']:
        tree=ast.parse((root/name).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='subprocess':
                assert name=='check.py' and node.func.attr=='run'
                argv=node.args[0];assert isinstance(argv,ast.List)
                a=argv.elts[0]
                assert isinstance(a,ast.Attribute) and isinstance(a.value,ast.Name) and a.value.id=='sys' and a.attr=='executable'
                assert not any(k.arg in ('shell','env','executable') for k in node.keywords)
    return root,got


def check_summary(summary,primary,secondary,control,spec,root):
    """Concrete quantitative joins; a PASS field alone is never sufficient."""
    assert summary['status']=='EXTERNAL_GRAM_SPATIAL_RECOVERY_AUDIT_PASS'
    assert summary['audited_memory']==774 and summary['auditor']=='functional_astra' and summary['producer']=='ladder_astra'
    assert summary['snapshot']==791
    for key,val in [('complete_raw_cells',690988),('complete_weight_cells',157940),('positive_bins',224),('synthetic_bins',1),('original_leaves',14),('original_failed_parents',13),('original_point_controls',8),('original_scalar_slots',277),('active_rejections',25)]:
        assert summary[key]==val
    for key in ['official_attestation','physical_COVER_export','allindex782_audit','final_composition_audit','new_tail','new_Lambda','new_source_phase_search','candidate']:
        assert summary[key] is False
    assert summary['coverage']==secondary['coverage']
    cv=summary['coverage']
    assert cv['t_closed']==['4/25','3/16'] and cv['x_closed']==[6000000185827,66476100549959] and cv['y']==0
    assert cv['entry_count']==1609011 and cv['target_count']==1609012
    assert cv['all_RIGHT_walls_by_identity'] and cv['terminal2300000']=='OPEN'
    assert cv['closed_index']==read('math/frozen/bank774_geometry.json')
    assert F(summary['lift_surplus'])==F(22375198391999,32000000000000000)>F(1,2000)
    assert F(summary['eventual_RH_margin'])==F(350479773,2)
    assert primary['status']=='PRIMARY_EXTERNAL_COMPLETE_PASS' and secondary['status']=='SECONDARY_EXTERNAL_PASS'
    assert primary['scalar_comparisons']==secondary['scalar_comparisons']==277
    assert len(primary['rows'])==len(secondary['rows'])==35
    for a,b in zip(primary['rows'],secondary['rows']):
        assert (a['category'],a['L'],a['U'])==(b['category'],b['L'],b['U'])
        if a['category']=='leaves':
            assert F(a['retained_lower_expression']['lo'])>F(1,100)
            assert F(b['retained_lower_expression']['lo'])>F(1,100)
    original_digests={}
    for ln in Path('math/frozen/bank774_outputs.txt').read_text().splitlines():
        if ln and not ln.startswith('#'):
            h,n=ln.split();original_digests[n]=h
    cp=primary['complete']
    assert cp['raw_sha256']==original_digests['p_raw.txt']==original_digests['s_raw.txt']
    assert cp['weight_sha256']==original_digests['p_weights.txt']==original_digests['s_weights.txt']
    assert cp['bin_sha256']==digest((root/'OWN_BINS.txt').read_bytes())==digest(Path('math/frozen/bank774_bins.txt').read_bytes())
    assert control['status']=='EXTERNAL_ADVERSE_AND_BINDING_PASS' and len(control['rejected_mutations'])==25
    assert control['domain']['source']=='COMPLETE_WEIGHTED_GRAM_767' and control['domain']['base_cutoff_stable_before_heat']
    # All mathematical products were absent before this invocation. They are
    # all now required, and their hashes must equal the newly emitted manifest.
    manifest={}
    for ln in (root/'OUTPUTS.sha256').read_text().splitlines():
        h,n=ln.split();assert n not in manifest
        assert digest((root/safe(n)).read_bytes())==h;manifest[n]=h
    assert set(manifest)==set(spec['generated_products'])-{'OUTPUTS.sha256'}
    assert summary['outputs']=={k:manifest[k] for k in summary['outputs']}
    assert summary['checks']>primary['checks']+secondary['checks']+control['checks']
    return True


def execute():
    spec=read('RECOVERY_LIVE.json');root,got=materialize(spec)
    # Same Python interpreter and inherited confinement; no env override,
    # foreign executable or modified mathematical source.
    p=subprocess.run([sys.executable,'check.py'],cwd=root,capture_output=True,text=True,timeout=600)
    Path('live_recovery.log').write_text(p.stdout);Path('live_recovery_stderr.log').write_text(p.stderr)
    if p.returncode:raise AssertionError('complete LIVE recovery execution did not pass: '+p.stderr)
    assert not p.stderr
    assert not re.search(r'\[\s*(fail(?:ed|ure)?|error)\s*\]|^\s*(fail(?:ed|ure)?|error)\b',p.stdout,re.I|re.M)
    # The independently authored driver appends its assertion count to RESULT.
    results=[z for z in p.stdout.splitlines() if z.startswith('RESULT:')]
    summary=json.loads((root/'SUMMARY.json').read_text())
    assert results==['RESULT: ALL PASS '+str(summary['checks'])]
    primary=json.loads((root/'PRIMARY_AUDIT.json').read_text())
    secondary=json.loads((root/'SECONDARY_AUDIT.json').read_text())
    control=json.loads((root/'CONTROL_AUDIT.json').read_text())
    check_summary(summary,primary,secondary,control,spec,root)
    for line in p.stdout.splitlines():
        # Show complete quantitative transcript, but do not make the external
        # author's historical claim text an additional candidate claim.
        if line.startswith('FACT_TEXT'):continue
        print('LIVE_RECOVERY '+line)
    out={'witness_type':'COMPLETE_LIVE_INDEPENDENT_PROOF','author':spec['author'],'target':774,
         'target_fact_sha256':spec['target_fact_sha256'],'target_proof_sha256':spec['target_proof_sha256'],
         'capsule_sha256':digest(Path('RECOVERY_LIVE.json').read_bytes()),'source_transformations':[],
         'input_sha256':got,'execution_exit':p.returncode,'stdout_sha256':digest(p.stdout.encode()),
         'stderr_sha256':digest(p.stderr.encode()),'products':{n:digest((root/n).read_bytes()) for n in spec['generated_products']},
         'summary':summary,'fresh_complete_execution':True,'bank_acceptance_asserted':False,
         'checks':summary['checks']}
    Path('LIVE_EXECUTION.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    return out


if __name__=='__main__':
    execute()
    print('LIVE_ADAPTER: ALL PASS')
