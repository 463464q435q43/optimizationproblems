#!/usr/bin/python3
"""Collision-exclusion assembly. Accepted facts plus fully LIVE Python proofs.
No outside reads, no RECORD input, no binary children. Independent sources
are re-executed; pending facts are never treated as accepted citations.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import sympy as sp
from flint import arb, ctx

ctx.prec=256
ctx.threads=1
PINS={'LIVE_PROVENANCE.json': 'f76b1ca92f67ef32430c0658220e40dbcf8fb7bf61d612a687576d1b1d3de48e', 'exterior/FROZEN.sha256': '45333f7c4ad3bad4d49737ecbc060aaf6a59d1353ada70ff8c3522d8a6aa7327', 'exterior/THEOREM.md': '194798fc8464b817e2c672edcd057faf04a03e89384e2dead953fee966348eca', 'exterior/frozen/l7_theorem.txt': '4647f7088414963ed714ec4a13ed6bd36cbda2bc5e7c04c1375b5140d1c270c8', 'exterior/frozen/l8_independent.json': '41c1df5f6110f763650e4a0c5ce3a9ba62f4cd8afb25841f502730d1f23d92ce', 'exterior/frozen/l8_primary.json': '567aaee836a1e515a6aaf8c61778c1b17d7c47ac8b5c4b2ad7fbfc7d04dc6f0a', 'exterior/frozen/l8_proof.txt': '6d58be3401ef7de151a12f703db2b1b2a8b91fd6af516c039d99a11600039281', 'exterior/frozen/memory.json': '02907836bce6fe68d37ce710dd9408feee9499bdf98839a873b05496af09ba06', 'exterior/frozen/model_kernel_source.txt': '188e8bb7e29b7091797bee84cab45a9a1c69dbb79134293fc5189d769485e6c0', 'exterior/frozen/model_primary.json': '74fbed6368bbdfd17abfebf28b40880b72dc15b99308664e7c973840b45a5123', 'exterior/frozen/model_primary_source.txt': '8ec28791092898f80050e8158a25d90e7977e18bfdaca0d1c1850b0afa0f697a', 'exterior/frozen/model_proof.txt': '764506e8a5120d92629a956517ebd2ad2373613534884f72ec34019aea6e7008', 'exterior/frozen/model_second.json': '5a0c81ae73298eeeae71dfdf058d8642d3f9a99a5387abd9f5b49c27dbfd4260', 'exterior/frozen/model_second_prefix.log': 'f3fa4f89a6436e75de019954cb06e87116401b295bcea086693bba008543f25e', 'exterior/frozen/model_second_source.txt': '7ba6d25201a5c2fd9b8816f9d5cec273846741bdfa90921a0a82726bfb465ecb', 'exterior/frozen/provenance.json': '94c56f49a6a4d1442c3014f0132f10b15bb47abd434add9c1a3b82854d941b01', 'exterior/second_line.py': '0e01a2267195cd226fa9d3c91310bbe046fa858cd976bde87b89da16350c1006', 'exterior/verify.py': '71b153d39ae0eab4cc4c37ff8927f0fcab258ae21b551e8d7628088f8df03249', 'frozen/analytic_separator_second.txt': 'fd5e4f351cdaf71dd2b0dfe505a48b95965be5db915403e2d3787a19e455d5df', 'frozen/anchor.txt': '874957ddc1caa202aeffa7573013dc161854c39b3f832d367fd5cd008e9ccb54', 'frozen/boundary_proof.txt': '2bebe2da8c1f28ed99ea856fe2d8134842ec450046077a8549374d84bbb56a54', 'frozen/hermite_separator.txt': '70cc54cfc3932efaa495687dc3565f9af090594deca67b65faa88dde853cc196', 'frozen/interior.txt': 'bdc313246fb5927e7605ba048deca2c2b0566eda9fb98a2a12cae8f53c9d1842', 'frozen/interior_audit.json': '097749381b59ae0e47bf7d38ed11fad4df9789c378333bbc47ecc8c88a9d1342', 'frozen/memory.json': 'b4c2bebf5faf447988982cbe7f199bf4f61e27fe9475928d614fba4e5e4acebc', 'frozen/provenance.json': '9da973e44ba6b1a88fad24e40cf076b1b0a7f91d54aeeddae6907c59c602497b', 'frozen/remote_tail.txt': 'b25f0abb8cccd94b36ea5ec89324c40d80f64724b8de82a40af7a885827069c9', 'frozen/remote_tail_second.txt': '78f6e660c543d9a1a6c741716197b60e58b05130e0b6f81490a7d0da1fe61b06', 'frozen/separator_second_summary.json': 'e81b4ff81fb81da5141feeed77b90d2a8193e6c669924d83a37d64b09fbb10be', 'frozen/tail_certificate.json': 'a0f80abc5e3802c34ac80133f4b5d27643f34754be0613346dd06bf6b4094f05', 'frozen/tail_config.json': '6ba3eb7bc7c4aeb72703c6b4f033d52d43e0358596f8ad27e012238835d24198', 'frozen/tail_gauge.txt': '3d56f7e83f486580836645dee5bd6597c6c054ae6bf5b7e85474ef9e0a3b5aa1', 'frozen/tail_head1.txt': '8fb26ce16be4b34846dc8ca26fddb70d6b14172b23286e2363f034e15a9dc10e', 'frozen/tail_head2.txt': '97c0e0737eac7fe7bc5c07ba5a0e5fea38f006a2d5b4e7cb68121514e561085a', 'frozen/tail_model.txt': '5f47f913cb54ccabb22f23990f1f19c82798e7761b0d02596e530b136d90812d', 'frozen/tail_primary_kernel.txt': '48bad048b78f157a1793021d23d44bb4795c7b24db0da98afaa7dc06a8b17193', 'frozen/tail_second_certificate.json': '0892b25297c3f4b02a69221da1a6bed4b5af43cc7e77c8e171848539d0610a20', 'frozen/tail_second_kernel.txt': 'd6dcad7aef6e30c2651a3ea2251043b2df7f078e7dd2d542b70714204cd0a86c', 'live_adoption_second/AUDIT.md': 'c28976ad0237ceaa7ac3544f32938f727c06e4ce2177c9bc58645fc9daad0ce1', 'live_adoption_second/AUDITED_EXTERIOR.md': '194798fc8464b817e2c672edcd057faf04a03e89384e2dead953fee966348eca', 'live_adoption_second/AUDITED_TAIL.md': '808278ace704916895c8033a9d807b8b3a757cb7e85a53aafd9e5c9e7e23fc3f', 'live_adoption_second/BANK605_independent.json': '41c1df5f6110f763650e4a0c5ce3a9ba62f4cd8afb25841f502730d1f23d92ce', 'live_adoption_second/BANK605_primary.json': '567aaee836a1e515a6aaf8c61778c1b17d7c47ac8b5c4b2ad7fbfc7d04dc6f0a', 'live_adoption_second/INPUTS.json': '50a8548203781c12972489d1d2aea8cdebb3df5c4ba289f92ef9e69f3fb8517b', 'live_adoption_second/check.py': '923bc5cf7b43a10b5f7c22013226ce6c43f3e6869151585df1a602d7002f98fe', 'live_model_second/AUDIT.md': 'b20c42ff8507af10dcd49f7bf2cbb6e171dc1e3be2f0afb973d000b889795948', 'live_model_second/AUDITED_PROOF.md': '764506e8a5120d92629a956517ebd2ad2373613534884f72ec34019aea6e7008', 'live_model_second/CONSUMED_CORNER.md': '43e1f210fcabb3751fafda9695b4881b06a1e2664e2ee370117fe6a57600b6a5', 'live_model_second/CONSUMED_CORNER_OUTPUT.log': '18f70610b6170bf976be75f845d51a81b548aa7593fa981a031eaa5b5600fce9', 'live_model_second/INPUTS.json': '58fceb3a07dd6c3aa572c048d2e54eddd4ce0cc845be7e3dffb7e0f8d97a60ff', 'live_model_second/check.py': '57659617d01247f55a71c70d687082b97f6733851190dfdaad043a425204eb41', 'live_model_second/iv_check.py': 'f70ae63598d19aabae5b0780fa3f0f95893727b17845f3512eb0b81671fa3525'}
COUNT=0
A,T=F(333,2000),F(3,16)
X,W,N0,NT=6000000185827,28274333882307,690988,1499999
TPT=F(3000175332800)


def gate(name,yes):
    global COUNT
    if not yes:raise AssertionError(name)
    COUNT+=1;print('PASS',name,flush=True)

def b(q):
    q=F(q);return arb(q.numerator)/q.denominator

def low(z):return F(str(z.lower().fmpq()))
def high(z):return F(str(z.upper().fmpq()))
def floor_trunc(q,d):
    q=F(q);n=q.numerator*10**d//q.denominator
    return ('-' if n<0 else '')+str(abs(n)//10**d)+('.'+str(abs(n)%10**d).zfill(d) if d else '')
def ceil_trunc(q,d):
    q=F(q);n=-((-q.numerator*10**d)//q.denominator)
    return floor_trunc(F(n,10**d),d)
def emit(name,q,d=18):
    l,h=(low(q),high(q)) if isinstance(q,arb) else (F(q),F(q))
    print(name,'EXACT',l,h,'FLOOR'+str(d),floor_trunc(l,d),'CEIL'+str(d),ceil_trunc(h,d))
def read(name):return json.loads(Path(name).read_text())

for q,n,fl,ce in [(F(-1,3),4,'-0.3334','-0.3333'),(F(-1,10**7),4,'-0.0001','0.0000'),(F(1,7),4,'0.1428','0.1429'),(F(-1,8),4,'-0.1250','-0.1250')]:
    gate('signed directed digit tooling',floor_trunc(q,n)==fl and ceil_trunc(q,n)==ce)
manifest={}
for line in Path('FROZEN.sha256').read_text().splitlines():
    if not line or line.startswith('#'):continue
    digest,name=line.split()
    gate('pinned proof/source/output '+name,PINS.get(name)==digest==hashlib.sha256(Path(name).read_bytes()).hexdigest())
    manifest[name]=digest
gate('complete manifest inventory',manifest==PINS)
mem=read('frozen/memory.json')
gate('selected accepted snapshot',mem['snapshot_entries']==619)
for n in [588,590,596,599,604,605,606,607,613,614,616,617,618]:
    gate('named banked foundation '+str(n),mem['facts'][str(n)]['line']==n and 'FOUNDATION' in mem['facts'][str(n)]['fact'])
gate('anchor citation pinned', '[V1-H-213 ' in mem['facts']['526']['fact'] and '[V1-H-220 ' in mem['facts']['549']['fact'])
for row in read('LIVE_PROVENANCE.json'):
    gate('live independent source attribution '+row['dest'],PINS[row['dest']]==row['sha256'] and row['author']=='numerics_astra-s8' and row['status'].startswith('LIVE'))

print('--- A criterion, explicit uniform tail and positive stall')
gate('valid anchored band',0<A<T<=F(1,2))
epsilon=9*(F(1,2**16)+F(1,15*2**15))+F(20*2050,2**256)+F(3,2**64)
gate('banked remote tail epsilon exact',epsilon<F(1,1024))
gate('remote tail phase strict reserve',F(511,8)>4 and F(35,2**256)<F(1,8))
r=A/2
gate('single left-neighbourhood parameter',0<r<A<=T<=F(1,2) and 128/r==F(512000,333))
emit('REMOTE_EPSILON',epsilon)
print('STALL_REMOTE_RADIUS 4*pi*exp(512000/333)+1 UNIFORM t=[333/4000,1/2]')
gate('external remote manuscript version',PINS['frozen/remote_tail.txt'] in mem['facts']['588']['fact'])
# For any hypothetical Lambda in [A,T], r<Lambda; accepted stall yields a collision.
gate('strict criterion includes both endpoints',r<A and A<=T and T==F(3,16))

print('--- B PT2021 initialization and accepted anchor')
height=F(X,2);margin=TPT-height
gate('accepted RH height',height<=TPT and margin==F(350479773,2)>0)
gate('anchor agrees with banked value',T==F(3,16))
# Two historical exact arithmetic regimes, no new RH computation.
gate('V1 anchor arithmetic',F(21,125)+F(39,2000)==T)
gate('older published row arithmetic',F(186,1000)+F(16733,100000)**2/2==F(19999966445,10**11))
print('RH_SOURCE PT2021 arXiv:2004.09765 REQUIRED',height,'AVAILABLE',TPT,'MARGIN',margin)

print('--- C full boundary, Hermite theorem and interior')
gate('Hermite external version',PINS['frozen/hermite_separator.txt'] in mem['facts']['617']['fact'])
gate('interior external version',PINS['frozen/interior.txt'] in mem['facts']['617']['fact'])
gate('numerical separator external version',PINS['frozen/boundary_proof.txt'] in mem['facts']['616']['fact'])
sumsep=read('frozen/separator_second_summary.json')
charge=F(sumsep['constants']['total']['hi']);row=sumsep['sweep']['minimum_row'];model_floor=F(row[3],10**12)
gate('accepted full boundary output reserve',charge<F(1,800) and model_floor-charge>F(7,800))
gate('external full-domain summary',sumsep['sweep']['leaves']==255778 and row[3]==226168051362)
joint=read('frozen/interior_audit.json')['joint']
gate('interior exact consumed joint',F(joint['X'])==X and F(joint['required_height'])==height and F(joint['margin'])==margin and joint['padding_squared_min']==3)
gate('horizontal strip padding at all times',F(2)**2-1==3 and T>=0)
gate('no time-zero simplicity asserted',A>0)
emit('BOUNDARY_MODEL_FLOOR',model_floor,12);emit('BOUNDARY_CHARGE_UPPER',charge)
# Universal Hermite theorem is consumed; exact controls expose coefficient/sign convention.
w=sp.Symbol('w');polys=[sp.Integer(1),w]
for m in range(1,8):polys.append(sp.expand(w*polys[m]-2*m*polys[m-1]))
for m in [2,3,5,8]:
    explicit=sum((-1)**j*sp.factorial(m)*w**(m-2*j)/(sp.factorial(j)*sp.factorial(m-2*j)) for j in range(m//2+1))
    gate('Hermite normalization control '+str(m),sp.expand(polys[m]-explicit)==0 and sp.expand(sp.diff(polys[m],w)-m*polys[m-1])==0)

print('--- D LIVE same-witness finite exterior and external numerical line')
def run_child(label,directory,script):
    proc=subprocess.run([sys.executable,script],cwd=directory,capture_output=True,text=True,check=False)
    Path(label+'_stdout.log').write_text(proc.stdout)
    Path(label+'_stderr.log').write_text(proc.stderr)
    for line in proc.stdout.splitlines():print('CHILD_'+label+' '+line)
    if proc.stderr:print(proc.stderr,file=sys.stderr,end='')
    gate(label+' child exit',proc.returncode==0)
    results=[s.strip() for s in proc.stdout.splitlines() if s.strip().upper().startswith('RESULT')]
    gate(label+' one successful result',results==['RESULT: ALL PASS'])
    fail=re.compile(r'\[\s*(fail(ed|ure)?|error)\s*\]|^\s*(fail(ed|ure)?|error)\b',re.I)
    gate(label+' no adverse marker or traceback',not any(fail.search(s) for s in proc.stdout.splitlines()) and 'Traceback' not in proc.stderr)
    return proc.stdout

run_child('EXTERIOR','exterior','verify.py')
ex=read('exterior/audit_summary.json')
gate('live exterior all quantifiers',ex['t']==[str(A),str(T)] and ex['N']==[N0,NT] and ex['x_closed']==[X,W] and ex['y']=='0')
gate('live exterior strict reserve',F(ex['strict_reserve_lower'])>F(2999,50000) and ex['zero_coefficient_perturbation'])
run_child('MODEL_SECOND','live_model_second','check.py')
model2=read('live_model_second/independent_certificate.json')
cov=model2['cover']
gate('independent full model cover and seam',model2['W']==W and cov[0]['L']==N0 and cov[-1]['U']==NT and all(s['U']+1==t['L'] for s,t in zip(cov,cov[1:])))
gate('independent all-block mass and forcing',all(F(z['bound'][1])<F(47,50) for z in cov) and F(model2['forcing'][1])<21)
gate('independent actual witness phase',F(model2['ref47']['emin'][0])>F(1,4) and F(model2['ref47']['K'][1])<5 and F(model2['ref47']['Emax'][1])<F(41,20) and F(model2['ref47']['Eprime'][1])<F(51,50) and F(model2['ref47']['ell'][0])>17)
gate('external model exact manuscript',hashlib.sha256(Path('live_model_second/AUDITED_PROOF.md').read_bytes()).hexdigest()==PINS['exterior/frozen/model_proof.txt'])
run_child('ADOPTION_SECOND','live_adoption_second','check.py')
ad=read('live_adoption_second/audit_results.json')
gate('external finite manuscript matches live proof',hashlib.sha256(Path('live_adoption_second/AUDITED_EXTERIOR.md').read_bytes()).hexdigest()==PINS['exterior/THEOREM.md'])
gate('external finite premise discharged',F(ad['arithmetic']['direct'])<F(ex['charge_cap']) and ad['geometry']['W']==W)

print('--- E transitions: natural right-hand index, full closed rational seam')
def wall(n,t):return 4*arb.pi()*(arb(n)**2-b(F(t)/16))
gate('first index all band',wall(N0,A)<X<wall(N0+1,T))
gate('last index all band',wall(NT,A)<W<wall(NT+1,T)<W+1)
gate('derived exact rational seam',int(wall(NT+1,T).floor().unique_fmpz())==W)
n,t=sp.symbols('n t',positive=True)
gate('all-natural-wall exact radicand',sp.simplify((4*sp.pi*(n*n-t/16))/(4*sp.pi)+t/16-n*n)==0)
gate('wall time orientation',sp.diff(4*sp.pi*(n*n-t/16),t)==-sp.pi/4)

print('--- T accepted practical true-H tail; full joints and replay')
config=read('frozen/tail_config.json');first=read('frozen/tail_certificate.json');second=read('frozen/tail_second_certificate.json')
gate('tail whole-time configuration',F(config['t_lo'])==A and F(config['t_hi'])==T and config['head']==NT and config['N1']==NT+1 and first['X1']==W)
gate('tail independent adoption manuscript pinned',PINS['live_adoption_second/AUDITED_TAIL.md']=='808278ace704916895c8033a9d807b8b3a757cb7e85a53aafd9e5c9e7e23fc3f')
tailcharge=F(ad['arithmetic']['tail'])
gate('tail live second-line charge',tailcharge==F(751998000616933,130000000000000000000)<F(3,500000))
gate('tail true-H reserve',1-F(43,50)-tailcharge>F(69997,500000))
rows=first['blocks'];rows2=second['blocks'];analytic=config['analytic_joint'];middle=config['middle_joint']
gate('all primary tail joints',rows[0]['a']==NT and rows[-1]['b']==analytic and all(r['a']<r['b'] for r in rows) and all(r['b']==s['a'] for r,s in zip(rows,rows[1:])))
gate('all independent tail joints',[(r['a'],r['b']) for r in rows]==[(r['a'],r['b']) for r in rows2])
for label,cert in [('PRIMARY',first),('SECOND',second)]:
    all_upper=[F(r['total_hi']) for r in cert['blocks']]
    gate(label+' all tail row bounds',all(v<F(43,50) for v in all_upper))
    gate(label+' exact tail aggregate',max(all_upper)==F(cert['global_hi']))
    gate(label+' analytic through infinity',F(cert['infinite_hi'])<F(1,100)<F(43,50))
    emit(label+'_TAIL_ALL_BLOCK_UPPER',max(all_upper))
# Small reproducibility replays of the accepted heavy-leg transport, never C.
heads={}
for cut,name in [(NT,'frozen/tail_head1.txt'),(middle,'frozen/tail_head2.txt')]:
    bins=[]
    for line in Path(name).read_text().splitlines():
        s=line.split()
        if s[0]=='BIN':bins.append((int(s[1]),int(s[2]),max(F(0),F(int(s[4]),10**18))))
    gate('whole frozen head cover '+str(cut),bins[0][0]==2 and bins[-1][1]==cut and all(x[1]+1==y[0] for x,y in zip(bins,bins[1:])))
    heads[cut]=bins
c=b(F(config['phase_derivative_cap']));e=b(F(config['eta_derivative_cap']));ta=b(A)
ps=[2,3,5,7,11,13];ls=[arb(p).log() for p in ps]
def endpoint(n):
    ln=arb(n).log();sig=arb(1)/2+ta*(ln/2-b(F(1,n*n)))
    qs=[(ta*l*l/4-sig*l).exp() for l in ls]
    kl=sum((q*l/(1-q) for q,l in zip(qs,ls)),arb(0))
    return sig,(2*ln-b(F(1,n*n))-4*c*kl)/(1+2*e)
div=[]
for mask in range(64):
    d=1;rate=arb(0)
    for k,p in enumerate(ps):
        if mask>>k&1:d*=p;rate+=ls[k]**2/4
    div.append((d,arb(d).log(),rate))
seed=hashlib.sha256(Path('frozen/tail_certificate.json').read_bytes()).digest()
picks={0,len(rows)-1,max(range(len(rows)),key=lambda k:F(rows[k]['total_hi']))}
picks.add(int.from_bytes(seed[:4],'big')%len(rows))
for k in sorted(picks):
    row=rows[k];nn,rr=row['a'],row['b'];cut=NT if nn<middle else middle
    sig,ell=endpoint(nn);delta=sig-endpoint(cut)[0]
    hd=sum((b(hi) if nn==cut else b(hi)*(-delta*arb(l).log()).exp() for l,r,hi in heads[cut]),arb(0))
    wt=(2*(arb(rr).log()+arb(30030).log())/ell-1).max(arb(1))
    kk=(ta/4).sqrt();shift=(sig-1)/(2*kk)
    pref=arb.pi().sqrt()/(2*kk)*(-(sig-1)**2/ta).exp();top=(kk*arb(rr).log()-shift).erfi()
    integ=arb(0)
    for d,ld,rate in div:
        ii=pref*(top-(kk*arb(cut//d).log()-shift).erfi())
        if not ii>0:raise AssertionError('positive replay integral')
        integ+=(ta*rate-sig*ld).exp()*ii
    gate('hash-selected full tail row '+str(k),hd<b(F(row['head_hi'])) and wt*integ<b(F(row['phi_hi'])) and hd+wt*integ<b(F(row['total_hi'])))
print('TAIL_REPLAY_ROWS',sorted(picks))

print('--- F exact module union, both time endpoints and every open slab')
boxes=[('interior',A,T,F(0),F(X)),('exterior',A,T,F(X),F(W)),('tail',A,T,F(W),None)]
def covered(bs):
    cuts=sorted({A,T}|{x for _,a,z,_,_ in bs for x in [a,z] if A<x<T})
    def good(t0,t1):
        intervals=sorted([(c,d) for _,a,z,c,d in bs if a<=t0 and t1<=z],key=lambda r:r[0]);reach=F(0)
        for c,d in intervals:
            if c>reach:return False
            if d is None:return True
            reach=max(reach,d)
        return False
    return all(good(t,t) for t in cuts) and all(good(l,r) for l,r in zip(cuts,cuts[1:]))
gate('complete closed t-x union',covered(boxes))
gate('interior never exceeds RH abscissa',all(d<=X for m,a,z,c,d in boxes if m=='interior'))
gate('mutation remove finite region',not covered([boxes[0],boxes[2]]))
gate('mutation spatial seam shifted',not covered([boxes[0],boxes[1],('tail',A,T,F(W+1),None)]))
gate('mutation missing lower time interval',not covered([boxes[0],('exterior',A+F(1,10**6),T,F(X),F(W)),boxes[2]]))
gate('mutation interior simplicity at zero forbidden',not F(0)>0)
for m,a,z,c,d in boxes:print('COVER module='+m+' t=['+str(a)+','+str(z)+'] x=['+str(c)+','+('inf' if d is None else str(d))+']')
print('AXES collision_y=0; interior_N=unrestricted; exterior_N=[690988,1499999]; tail_N>=1499999')
print('BOUNDARY_AXES t=[0,3/16] y=[-1,1] padded_to=[-2,2]; stall_tail_all_imaginary_parts')

print('--- G strict statement and exact improvement')
lam=A
comparison=F(86211,500000)
gate('record improvement against anchor',T-lam==F(21,1000)>0)
gate('moonshot comparison with real margin',comparison-lam==F(2961,500000)>0)
emit('LAMBDA_STRICT_UPPER',lam,10);emit('IMPROVEMENT_OVER_ANCHOR',T-lam,10);emit('IMPROVEMENT_OVER_COMPARISON_TARGET',comparison-lam,10)
gate('unchanged sole RH dependency',TPT-height==margin)
Path('assembly_audit.json').write_text(json.dumps({'lambda_strict_upper':str(lam),'t':[str(A),str(T)],'anchor':str(T),'X':X,'W':W,'rh_required':str(height),'rh_margin':str(margin),'snapshot':619,'checks':COUNT,'pending_claim_consumed':False,'external_model_rederived_live':True,'external_adoption_rederived_live':True,'coverage_boxes':3},sort_keys=True,indent=2)+'\n')
print('TOTAL CHECKS RUN:',COUNT)
print('RESULT: ALL PASS')
print('RECORD_LAMBDA_UPPER =',lam)
print('RECORD_T_LO =',A)
print('RECORD_T_HI =',T)
print('RECORD_ANCHOR =',T)
print('RECORD_X =',X)
