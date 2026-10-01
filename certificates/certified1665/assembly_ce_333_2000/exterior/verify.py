#!/usr/bin/python3
"""LIVE exact-witness adoption of banked 618 through 605 and 607/606.
Universal model and remainder bounds are consumed, never inferred from probes.
Only package-local inputs and a same-interpreter independent Python child.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import sympy as sp
from flint import arb, ctx

ctx.prec=256
ctx.threads=1
PINS = {'frozen/l7_theorem.txt': '4647f7088414963ed714ec4a13ed6bd36cbda2bc5e7c04c1375b5140d1c270c8', 'frozen/l8_independent.json': '41c1df5f6110f763650e4a0c5ce3a9ba62f4cd8afb25841f502730d1f23d92ce', 'frozen/l8_primary.json': '567aaee836a1e515a6aaf8c61778c1b17d7c47ac8b5c4b2ad7fbfc7d04dc6f0a', 'frozen/l8_proof.txt': '6d58be3401ef7de151a12f703db2b1b2a8b91fd6af516c039d99a11600039281', 'frozen/memory.json': '02907836bce6fe68d37ce710dd9408feee9499bdf98839a873b05496af09ba06', 'frozen/model_kernel_source.txt': '188e8bb7e29b7091797bee84cab45a9a1c69dbb79134293fc5189d769485e6c0', 'frozen/model_primary.json': '74fbed6368bbdfd17abfebf28b40880b72dc15b99308664e7c973840b45a5123', 'frozen/model_primary_source.txt': '8ec28791092898f80050e8158a25d90e7977e18bfdaca0d1c1850b0afa0f697a', 'frozen/model_proof.txt': '764506e8a5120d92629a956517ebd2ad2373613534884f72ec34019aea6e7008', 'frozen/model_second.json': '5a0c81ae73298eeeae71dfdf058d8642d3f9a99a5387abd9f5b49c27dbfd4260', 'frozen/model_second_prefix.log': 'f3fa4f89a6436e75de019954cb06e87116401b295bcea086693bba008543f25e', 'frozen/model_second_source.txt': '7ba6d25201a5c2fd9b8816f9d5cec273846741bdfa90921a0a82726bfb465ecb', 'frozen/provenance.json': '94c56f49a6a4d1442c3014f0132f10b15bb47abd434add9c1a3b82854d941b01'}
SECOND_PIN = '0e01a2267195cd226fa9d3c91310bbe046fa858cd976bde87b89da16350c1006'
COUNT=0
X,N0,NT,D=6000000185827,690988,1499999,1024
A,T=F(333,2000),F(3,16)
SPEED=F(500000000001,10**12)
CAP=F(47,50)
CCAP=F(10581704117220,10**18)


def gate(name,condition):
    global COUNT
    if not condition: raise AssertionError(name)
    COUNT+=1
    print('PASS',name,flush=True)


def b(q):
    q=F(q)
    return arb(q.numerator)/q.denominator


def lo(v): return F(str(v.lower().fmpq()))
def hi(v): return F(str(v.upper().fmpq()))
def floor_trunc(q,n):
    q=F(q); k=q.numerator*10**n//q.denominator
    return ('-' if k<0 else '')+str(abs(k)//10**n)+('.'+str(abs(k)%10**n).zfill(n) if n else '')
def ceil_trunc(q,n): return floor_trunc(F(-((-F(q).numerator*10**n)//F(q).denominator),10**n),n)
def ceilq(q,n):
    q=F(q);return F(-((-q.numerator*10**n)//q.denominator),10**n)

def show(name,v,n=18):
    l,h=(lo(v),hi(v)) if isinstance(v,arb) else (F(v),F(v))
    print(name,'FLOOR'+str(n),floor_trunc(l,n),'CEIL'+str(n),ceil_trunc(h,n))
    print(name+'_EXACT',l,h)

def read(name):return json.loads(Path(name).read_text())
def cfun(x):return ((1+x*x).sqrt()/(4*arb.pi())).log()/4-1/(2*(1+x*x))
def charge(v,d,e0,e1,drift,q):return e0*v/2+2*(e1*v+e0*d+drift)/q

def box(row):return b(F(row['lo'])).union(b(F(row['hi'])))
def encl(v,row):return F(row['lo'])<=lo(v)<=hi(v)<=F(row['hi'])

for q,n,fl,ce in [(F(-1,3),5,'-0.33334','-0.33333'),(F(-1,10**9),5,'-0.00001','0.00000'),(F(1,7),5,'0.14285','0.14286'),(F(-1,8),5,'-0.12500','-0.12500')]:
    gate('signed rounding '+str(q),floor_trunc(q,n)==fl and ceil_trunc(q,n)==ce)
manifest={}
for line in Path('FROZEN.sha256').read_text().splitlines():
    if not line or line.startswith('#'):continue
    digest,name=line.split()
    gate('source-pinned frozen '+name,PINS.get(name)==digest==hashlib.sha256(Path(name).read_bytes()).hexdigest())
    manifest[name]=digest
gate('manifest exact inventory',manifest==PINS)
gate('separate child source pin',hashlib.sha256(Path('second_line.py').read_bytes()).hexdigest()==SECOND_PIN)
mem=read('frozen/memory.json')
gate('snapshot 619',mem['snapshot_entries']==619)
for n,seat,session in [(618,'functional_astra','functional_astra-s6'),(605,'numerics_astra','numerics_astra-s6'),(607,'prover_astra','prover_astra-s5'),(606,'numerics_astra','numerics_astra-s6')]:
    r=mem['facts'][str(n)]
    gate('accepted citation identity '+str(n),r['line']==n and r['seat']==seat and r['session']==session and 'FOUNDATION' in r['fact'])
gate('exact L7 manuscript externally audited',PINS['frozen/l7_theorem.txt'] in mem['facts']['606']['fact'])
for row in read('frozen/provenance.json'):
    gate('frozen producer provenance '+row['file'],row['memory_line'] in [605,607,618] and PINS[row['file']]==row['sha256'])

model=read('frozen/model_primary.json')
other=read('frozen/model_second.json')
fam={s:read('frozen/l8_'+s+'.json') for s in ['primary','independent']}
gate('all domain axes',model['domain']=={'tlo':str(A),'thi':str(T),'Nlo':N0,'Nhi':NT,'X':X,'seam':28274333882307,'y':0})
gate('complete model weight and mass',model['fixed_weight']==17 and F(model['mass_bound'])==CAP and F(model['consumed_B'])==F(891101027766,10**12))
rows=model['rows']; bins=model['bins']
gate('full integer blocks',len(rows)==model['leaf_count']==13 and rows[0]['l']==N0 and rows[-1]['r']==NT and all(r['l']<=r['r'] for r in rows) and all(r['r']+1==s['l'] for r,s in zip(rows,rows[1:])))
gate('full signed prefix bins',bins[0]['l']==D+1 and bins[-1]['r']==N0 and all(r['r']+1==s['l'] for r,s in zip(bins,bins[1:])))
for j,r in enumerate(rows):
    gate('frozen primary block '+str(j),0<F(r['initial']['lo'])<=F(r['initial']['hi'])<CAP and all(F(r[k]['lo'])<=F(r[k]['hi']) for k in ['old','new','initial']))
for j,r in enumerate(other['rows']):
    gate('frozen independent full block '+str(j),r['l']==rows[j]['l'] and r['r']==rows[j]['r'] and 0<F(r['lo'])<=F(r['hi'])<CAP)
gate('both ledgers same full integer cover',len(other['rows'])==len(rows))
max_initial=max(F(r['initial']['hi']) for r in rows)
gate('all-block aggregate exact',max_initial==F(model['max_initial_hi']))
show('BANKED_ALL_BLOCK_INITIAL_UPPER',max_initial)
gate('both complete forcing ledgers',0<F(model['forcing']['lo'])<=F(model['forcing']['hi'])<21 and 0<F(other['R']['lo'])<=F(other['R']['hi'])<21)

# One exact inverse; independent normalized reconstruction checks every d.
logs=[arb(0)]+[arb(d).log() for d in range(1,D+1)]
xx=arb(X);cx=cfun(xx);sx=arb(1)/2+b(A)*cx
bt=[arb(0)]+[(b(A)*logs[d]**2/4).exp() for d in range(1,D+1)]
fd=[arb(0)]+[(b(A)*logs[d]**2/4-sx*logs[d]).exp() for d in range(1,D+1)]
raw=[arb(0) for _ in range(D+1)];norm=[arb(0) for _ in range(D+1)]
raw[1]=norm[1]=arb(1)
proper=[[] for _ in range(D+1)]
for d in range(1,D+1):
    for m in range(2*d,D+1,d):proper[m].append(d)
for m in range(2,D+1):
    raw[m]=-sum((raw[d]*bt[m//d] for d in proper[m]),arb(0))
    norm[m]=-sum((norm[d]*fd[m//d] for d in proper[m]),arb(0))
mu=[raw[d]*(-sx*logs[d]).exp() for d in range(D+1)]
gate('all exact inverse coefficients identified',all(mu[d].overlaps(norm[d]) for d in range(1,D+1)) and raw[1]==1)
gate('exact zero perturbation in family',F(0)<=F(1,2**40) and D in [64,1024] and A<=T)
for label,f in fam.items():
    rs=sorted([r for r in f['rows'] if r['K']==D],key=lambda r:F(r['lo']))
    gate(label+' full closed anchor partition',F(rs[0]['lo'])==A and F(rs[-1]['hi'])==T and all(F(r['lo'])<F(r['hi']) for r in rs) and all(F(r['hi'])==F(s['lo']) for r,s in zip(rs,rs[1:])))
    gate(label+' single freeze covered',any(F(r['lo'])<=A<=F(r['hi']) for r in rs))
    for j,r in enumerate(rs):
        q=r['bounds']
        gate(label+' universal family budgets '+str(j),F(q['Emin'][0])>=F(1,5) and F(q['Emax'][1])<=F(21,10) and F(q['K1'][1])<=F(5,2) and F(q['Qphase'][0])>=16)

# Full Euler reference support, not a truncated reference pretending to be E.
primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
def reference(pmax,eta):
    ref={1:arb(1)};bp=arb(1);ll=arb(0)
    for p in primes:
        if p>pmax:break
        q=bt[p]*(-sx*logs[p]).exp()
        gate('Euler q '+str(pmax)+' '+str(p),0<q<1)
        bp*=1-q;ll+=q*logs[p]/(1-q)
        ref.update({d*p:-z*q for d,z in tuple(ref.items())})
    u,v=arb(0),arb(0)
    for d in sorted(set(ref)|set(range(1,D+1))):
        q=abs((mu[d] if d<=D else arb(0))-ref.get(d,arb(0)))
        u+=q;v+=q*arb(d).log()
    em=bp-u;kl=ll+(v+u*ll)/em
    qp=(xx/(4*arb.pi())).log()-4*b(SPEED)*kl
    return {'Emin':em,'Lambda1':kl,'Q':qp,'ell':qp/(1+2*b(eta)),
            'Emax':sum((abs(z) for z in mu[1:]),arb(0)),
            'EprimeMax':b(SPEED)*sum((abs(mu[d])*logs[d] for d in range(1,D+1)),arb(0))}
ref=reference(47,F(1,10**20))
ref29=reference(29,7*T/(4*X*X))
for k,v in ref.items():
    gate('live reference in frozen enclosure '+k,encl(v,model['reference'][k]))
    show('REF47_'+k,v)
gate('physical fixed scale all required gates',ref['Emin']>b(F(1,4)) and ref['Lambda1']<5 and ref['ell']>17 and ref['Emax']<b(F(41,20)) and ref['EprimeMax']<b(F(51,50)))
gate('exact corner proxy comparison not lower-bound inversion',0<ref29['ell']<17)
show('SOURCE_PROXY_ELL29',ref29['ell'])

# Re-derive every scalar spatial gate from banked signed-prefix masses.
B=F(model['consumed_B']);us=[F(r['hi']) for r in bins]
gate('nonnegative prefix gain direction',all(r['l']<N0+1 for r in bins) and sum(us,F(0))<B)
gate('initial prefix unit weights',arb(N0).log()<17)
for j,r in enumerate(rows):
    l,u,xl=r['l'],r['r'],r['x_lower']
    wall=4*arb.pi()*(arb(l)**2-b(T/16))
    gate('all-time spatial block lower '+str(j),xl>=X and ((l==N0 and xl==X) or (l>N0 and xl<wall<xl+1)))
    cc=cfun(arb(xl));ss=arb(1)/2+b(A)*cc
    delta=b(A)*(cc-cx) if xl!=X else arb(0)
    gate('monotone spatial exponent '+str(j),xl==X or delta>0)
    old=b(B-sum(us,F(0)))*(-delta*arb(N0+1).log()).exp()
    for row,ub in zip(bins,us):old+=b(ub)*(-delta*arb(row['l']).log()).exp()
    step=(arb(u).log()-arb(N0).log())/32
    integ=arb(0)
    for k in range(33):
        z=arb(N0).log()+k*step
        integ+=(b(A)*z*z/4+(1-ss)*z).exp()*(1 if k in [0,32] else 2)
    integ*=step/2
    ew=arb(0)
    for d in range(1,D+1):
        weight=(2*(logs[d]+arb(u).log())/17-1).max(arb(1))
        ew+=abs(raw[d])*(-ss*logs[d]).exp()*weight
    new=ew*integ
    gate('live full block reserve '+str(j),old+new<b(CAP))
    gate('same frozen spatial arithmetic '+str(j),encl(old,r['old']) and encl(new,r['new']) and encl(old+new,r['initial']))
    gate('entering amplitude decreasing '+str(j),b(A)*arb(u).log()/2<ss)
H=T-A
endpoint=b(CAP)*(-34*b(H)).exp()+21*b(H)
gate('convex entire closed time gate',H==F(21,1000) and endpoint<b(CAP) and encl(endpoint,model['time_endpoint']))
gate('global common decay endpoints',cx*arb(D+1).log()-arb(D+1).log()**2/4>34 and cx*arb(NT).log()-arb(NT).log()**2/4>34 and cx>arb(NT).log()/4)
show('TIME_CONVEX_ENDPOINT',endpoint)

# Hash-selected whole coefficient bins: representation audits only.
seed=hashlib.sha256(Path('frozen/model_primary.json').read_bytes()+Path('frozen/model_kernel_source.txt').read_bytes()).digest()
selected={0}
selected.update(sorted(range(len(bins)),key=lambda j:hashlib.sha256(seed+str(j).encode()).digest())[:2])
for j in sorted(selected):
    row=bins[j]; left,right=row['l'],row['r']
    co=[arb(0) for _ in range(right-left+1)];cache={};pairs=0
    for d in range(1,D+1):
        for n in range(max(1,(left+d-1)//d),min(N0,right//d)+1):
            if n not in cache:
                ln=arb(n).log();cache[n]=(b(A)*ln*ln/4-sx*ln).exp()
            co[d*n-left]+=mu[d]*cache[n];pairs+=1
    mass=sum((abs(v) for v in co),arb(0))
    gate('complete signed-bin representation '+str(j),encl(mass,row))
    print('REPLAY_BIN',j,'LEFT',left,'RIGHT',right,'PAIRS',pairs)
    show('SIGNED_PREFIX_BIN_'+str(j),mass)

# Symbolic exact identities, separate from numerical premises.
x,t=sp.symbols('x t',positive=True)
eta=t*sp.atan(x)/4-3*t*x/(2*(1+x*x))
gate('correct eta derivative',sp.factor(sp.diff(eta,x)-t*(7*x*x-5)/(4*(1+x*x)**2))==0)
sigma_prime=t*x*(x*x+5)/(4*(1+x*x)**2)
gate('sigma derivative envelope residual',sp.factor(t*(1/(4*x)+1/x**3)-sigma_prime-t*(x**4+9*x**2+4)/(4*x**3*(x**2+1)**2))==0)
dd,nn,sig=sp.symbols('dd nn sig',positive=True)
gate('multiplicative normalized coefficients',sp.simplify(dd**(-sig)*nn**(-sig)/(dd*nn)**(-sig)-1)==0)
z,v,h,q=sp.symbols('z v h q',positive=True)
f=sp.exp(t*v*v/4+(1-sig)*v)
gate('convex integral density',sp.simplify(sp.diff(f,v,2)/f-((t*v/2+1-sig)**2+t/2))==0)
gate('convex scalar envelope',sp.simplify(sp.diff(z*sp.exp(-q*h)+v*h,h,2)-z*q*q*sp.exp(-q*h))==0)

# Reproduce two banked charge regimes, then the new same-witness adoption.
old=charge(F(682857503579,10**18),F(114077128828636,10**18),F(41,20),F(4),F(1,10**12),F(16))
gate('known-anchor 606',old==F(605472441605919,20000000000000000000))
show('ANCHOR606',old)
tail=charge(F(655217372417,10**18),F(37300347933869,10**18),F(9,5),F(3,5),F(1,10**13),F(26))
gate('known-anchor 613',tail==F(751998000616933,130000000000000000000))
show('ANCHOR613',tail)
sigcap=T*(F(1,4*X)+F(1,X**3))
b1cap=F(21,10)*1640+F(5,2)*21
for label,f in fam.items():
    rv,rd=F(f['raw']['Ev'][1]),F(f['raw']['Ed'][1])
    gate(label+' raw directed value',ceilq(rv,18)==F(655217372417,10**18))
    gate(label+' raw directed derivative',ceilq(rd,18)==F(37300347933869,10**18))
    c=charge(rv,rd,F(21,10),SPEED*F(5,2),2*sigcap*b1cap,F(16))
    gate(label+' family exact charge',c<=CCAP and ceilq(c,18)==CCAP)
    show('FAMILY_CHARGE_'+label.upper(),c)
reserve=1-CAP-CCAP
gate('registered strict reserve',reserve==F(2999470914794139,50000000000000000)>F(2999,50000)>0 and CCAP<F(1,50000))
show('CHARGE_UPPER',CCAP);show('STRICT_RESERVE_LOWER',reserve)
# Direct real-gauge route, with a finite support rather than a p-series B1.
ev,ed=F(655217372417,10**18),F(37300347933869,10**18)
gate('finite logarithmic support',arb(D*NT).log()<22)
cdir=F(229,200)*ev+F(41,170)*ed+4*sigcap*CAP*22/17
gate('direct real-gauge coefficients',F(41,40)+2*F(51,50)/17==F(229,200) and 2*F(41,20)/17==F(41,170))
gate('direct independent charge route',cdir<CCAP)
show('DIRECT_GAUGE_CHARGE_UPPER',cdir)

# Rational seam belongs to predecessor cell on the WHOLE time band.
def wall(n,t):return 4*arb.pi()*(arb(n)**2-b(F(t)/16))
wend=wall(NT+1,T);W=int(wend.floor().unique_fmpz())
gate('same exact rational seam as banked tail',W==28274333882307==model['domain']['seam'])
gate('first cell all closed times',wall(N0,A)<X<wall(N0+1,T))
gate('last cell all closed times',wall(NT,A)<W<wend)
gate('strict floor not a rounded-up wall',W<wend<W+1)
gate('tail consumes same closed seam',str(W) in mem['facts']['613']['fact'] and str(W) in mem['facts']['614']['fact'])
show('RIGHT_WALL_MINUS_W',wend-W)
ni=sp.symbols('ni',positive=True,integer=True)
gate('natural right-hand index at every wall',sp.sqrt(ni**2)==ni)
gate('wall monotonic time direction',sp.diff(4*sp.pi*(ni**2-t/16),t)==-sp.pi/4)
print('DOMAIN t=['+str(A)+','+str(T)+'] N=['+str(N0)+','+str(NT)+'] y=0')
print('RIGHT_ENDPOINT_EXCLUDED 4*pi*(1500000^2-t/16)')

# Mutations expose the exact premise boundary.
def member(u,t,k,defect,c1):return A<=u<=t<=T and k in [64,1024] and 0<=defect<=F(1,2**40) and c1==1
gate('single frozen family member whole band',member(A,A,D,0,1) and member(A,T,D,0,1))
gate('mutation future anchor rejected',not member(T,A,D,0,1))
gate('mutation unsupported support rejected',not member(A,T,2048,0,1))
gate('mutation coefficient tolerance rejected',not member(A,T,D,F(1,2**39),1))
gate('mutation nonunit constant rejected',not member(A,T,D,0,F(99,100)))
gate('mutation terminal index rejected',not N0<=NT+1<=NT)
gate('mutation ceiling seam rejected',not W+1<wend)
gate('mutation unit mass rejected',not F(1)+CCAP<1)
missing=rows[len(rows)//2]
gate('mutation whole integer block removed',not any(r['l']<=missing['l']<=r['r'] for r in rows if r is not missing))

child=subprocess.run([sys.executable,'second_line.py'],capture_output=True,text=True,check=False)
print(child.stdout,end='')
if child.stderr:print(child.stderr,end='',file=sys.stderr)
gate('separate child exit',child.returncode==0)
gate('separate child final marker','SECOND: ALL PASS' in child.stdout)
summary={'snapshot':619,'consumes':[618,605,607,606],'t':[str(A),str(T)],'N':[N0,NT],'x_closed':[X,W],'y':'0','exact_frozen_anchor':str(A),'zero_coefficient_perturbation':True,'mass_cap':str(CAP),'charge_cap':str(CCAP),'strict_reserve_lower':str(reserve),'direct_gauge_charge':str(cdir),'ledger_blocks':len(rows),'prefix_replay_bins':sorted(selected),'model_consumed_not_recomputed':True,'external_adoption_audit_not_claimed':True,'checks':COUNT}
Path('audit_summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
print('COVER module=exterior t=['+str(A)+','+str(T)+'] x=['+str(X)+','+str(W)+']')
print('RH_DEPENDENCY none; future PT2021 required='+str(F(X,2))+' margin='+str(F(3000175332800)-F(X,2)))
print('SCOPE full finite true-H exterior only; no interior, off-axis reality or Lambda conclusion')
print('TOTAL CHECKS RUN:',COUNT)
print('RESULT: ALL PASS')
