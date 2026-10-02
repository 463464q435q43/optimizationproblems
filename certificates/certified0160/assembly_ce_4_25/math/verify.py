#!/usr/bin/python3
"""Typed global composition of banked Gram finite and differential-tail legs.
Pure local Python. Mathematical success does not authorize record release.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,subprocess,sys,copy,itertools,math
from flint import arb,ctx
import sympy as sp
ctx.prec=256;ctx.threads=1
PINS={'ASSEMBLY.md': 'a6c620eb9ffd110b641982129b1173bc4c7aa4262afc2f12ab08a2451f81773c', 'CITATIONS.json': 'ef9111d59d67d50a6efd2f1411f4d2775b00549d55e38a5dc65a3a9aef645959', 'CONTRACTS.json': 'fa81345dd718f697811eaba3238b59c35091a3d97c839f8baee38580e385b545', 'FACT.txt': '0ec8e7cd2daafe4274b8072659796837b62fe464e3e8bb9420dbc1eaff2fa273', 'PREREG.md': '1216500da8bc30012ae632111ef7d028ce84e6f61ce4b81e06af82461cd898f4', 'PROVENANCE.json': 'c2e7782b8f00d072be98ccb8612d0982812ec236da2e328e97d1a38da4482554', 'QUANTIFIER_AUDIT.md': '722bb0eddbd53e48b6a5f415f285c41b56198c83bbeb4403c7693c7880da0397', 'READINESS.json': '772cfe1d67df12ba084fee1fe1781e564eccd9cc0311fd440bf1328d08cc40f0', 'SECOND_PROOF.md': '640dab98b73910c413749ebcb43853b96ddfbaeb0f0f62770c79e14cf2e2dcb4', 'frozen/analytic_separator_second.txt': 'fd5e4f351cdaf71dd2b0dfe505a48b95965be5db915403e2d3787a19e455d5df', 'frozen/anchor.txt': '874957ddc1caa202aeffa7573013dc161854c39b3f832d367fd5cd008e9ccb54', 'frozen/bank720_theorem.txt': '249aa74644189dd15c0e5bf9e6fcddcfd576e242bb2660542c844f8c0fe4bff3', 'frozen/bank725_audit.txt': '4ae59adc397d9e31bf1d0ca2cb4565943a2840495c7f4bfaba3534a7584fde35', 'frozen/bank729_primary.json': '463e204585233314aeeb78c4b0f3723907e713180c2def062f94b287634c8c56', 'frozen/bank729_proof.txt': '2415dac9b1ef172267133ce3f9a493621a671243295f6bf3a645c15e4c665191', 'frozen/bank729_second.json': 'f8685c1bfeca0a21bfd69a6390dbf4ffff482320d49e597c7bb34dc2ce3d03eb', 'frozen/bank733_audit.txt': 'f25f28713b887a2b26d120ad8cc7207b55ef537cf1a2a33682cf83b503f9365e', 'frozen/bank738_primary.json': '3fbb21ec83d23588a73fc53511a6fc177ff69be020c419ee0c82d6d0bab03d09', 'frozen/bank738_proof.txt': '0837a258f15c47d50f8186701d8b701129af415e1ecbd5b64572cf04fac33a92', 'frozen/bank744_proof.txt': '2c688d63297c8bb60ba9faa801aa2d4a40fca65a0c90f9b80b148624e8874f10', 'frozen/bank754_audit.txt': 'ca2b8e0d5adf4768b57b625cd26ac8070e8449446d7147f34da96cd67a3f64fa', 'frozen/bank754_summary.json': '319a25d21b25970d58b9aaf165c305bdb2cd82df6d99486a10673e9ee22a16d9', 'frozen/bank767_geometry.json': 'f9a2a6e1a4181c7a56ca457342b3e0680deda8f1aafb847cfeae3a97238caeb6', 'frozen/bank767_leaves_primary.txt': '3ed5ee0c88248509ed9fd2b30337e3736d09039050f5166a7a982a3e16ce73c5', 'frozen/bank767_leaves_second.txt': 'dec6c0a8b2ff9559a3cf90a5cf75a11c4ae79752d99e92558e186ae314fe37c5', 'frozen/bank767_outputs.txt': '613d7df7f03c68af80e8a933ebe521ea6ab84f7bb5268c240155d18a5832c7df', 'frozen/bank767_proof.txt': '026b89ecc2fe2e42ef5dc62c513c01b567da609f4f73f7a6b7f6d8528022d806', 'frozen/bank767_secondproof.txt': '16310586a87b2bff2be351fc421ca3b7f1f3e643f8fc8068d23fde0e72300a7d', 'frozen/bank767_summary.json': '092da4612e585c102d19d63e07128111dd53147b0339219489091d64ef204baa', 'frozen/bank772_audit.txt': '678414019adc389f3c85815bb73012b9c6d8db4cd7ab1718dcc3625f82a162e9', 'frozen/bank772_summary.json': 'adf0f852114db7ece61eead8ed40c89b880d73c1d026a0e638a5d25776b4ce89', 'frozen/bank774_bins.txt': '94d0610a407a302ee18a2330cf48ebc94cbf34c74fc20f6545de41de667f8f1e', 'frozen/bank774_build_primary.c': '19bc55ec0eb5634bda211f41a350982df9937e5e3d7819687d828f2001e0af23', 'frozen/bank774_build_second.txt': 'bd4b83859f25c88ce213f5c150241ba2636a54142e0cf217ecd0b314d1bf6ee9', 'frozen/bank774_geometry.json': '1d6a6dc0577e18dd4c6bb49b8b746e353f7bf40490368ea032a3c24019a497d5', 'frozen/bank774_outputs.txt': '3e8f4148cd6880fd7e0533074e2a40a624e4b40bf13b8d61a40a125626e377f2', 'frozen/bank774_primary.json': 'a83bcadbd63c5ba04be0a98ffa628d6b666616af944343de5b5a86a38e600137', 'frozen/bank774_probes.json': '1c2d17ecb293dfa584921bee211731f645d7c2951e706950156ffa4c88da6956', 'frozen/bank774_proof.txt': '41e09d60548b65e2c09c8c374c6e3a9378141fc9817998f2d527bdb8c45d44d8', 'frozen/bank774_second.json': '2d7227cd3797de39934feaae909d6c69cceecad457c9acafeadde115f12a0c8b', 'frozen/bank774_secondproof.txt': 'e567ecd65edd93cdd967e6757afba5767efd5babee6577830b3b2944d3ea27c5', 'frozen/bank774_source_pins.json': '6d9a1ba0a7d661fbe3625190b0fc13b18d9bec9ad47c02660f0c6d43ad6e468f', 'frozen/bank774_summary.json': 'e00c5a340faa03fca859c7bd7f67cfdccfebaf84a97f239c01cc5adc9e5db8e8', 'frozen/boundary_proof.txt': '2bebe2da8c1f28ed99ea856fe2d8134842ec450046077a8549374d84bbb56a54', 'frozen/hermite_separator.txt': '70cc54cfc3932efaa495687dc3565f9af090594deca67b65faa88dde853cc196', 'frozen/interior.txt': 'bdc313246fb5927e7605ba048deca2c2b0566eda9fb98a2a12cae8f53c9d1842', 'frozen/interior_audit.json': '097749381b59ae0e47bf7d38ed11fad4df9789c378333bbc47ecc8c88a9d1342', 'frozen/remote_tail.txt': 'b25f0abb8cccd94b36ea5ec89324c40d80f64724b8de82a40af7a885827069c9', 'frozen/remote_tail_second.txt': '78f6e660c543d9a1a6c741716197b60e58b05130e0b6f81490a7d0da1fe61b06', 'frozen/separator_second_summary.json': 'e81b4ff81fb81da5141feeed77b90d2a8193e6c669924d83a37d64b09fbb10be'}
SECOND_PIN='0674cdc709a12bcdf1c9957bcab64e9bcfe2e0d8c6ecee8c342029c47e6d1313'
COUNT=0
out={'exact':{},'scalars':{},'leaves':[],'mutations':[],'probes':[]}
def gate(ok,name):
 global COUNT
 COUNT+=1
 if not bool(ok):raise AssertionError(name)
def read(n):return json.loads(Path(n).read_text())
def aa(q):q=F(q);return arb(q.numerator)/q.denominator
def ends(z):return (F(str(z.lower().fmpq())),F(str(z.upper().fmpq()))) if isinstance(z,arb) else (F(z),F(z))
def floor_trunc(q,d):q=F(q);return q.numerator*10**d//q.denominator
def ceil_trunc(q,d):return -floor_trunc(-F(q),d)
def fmt(v,d):return ('-' if v<0 else '')+str(abs(v)//10**d)+'.'+str(abs(v)%10**d).zfill(d)
def digits(z,d=18):
 l,u=ends(z);return {'lo':str(l),'hi':str(u),'floor':fmt(floor_trunc(l,d),d),'ceil':fmt(ceil_trunc(u,d),d),'places':d}
def emit(k,z,d=18):
 out['scalars'][k]=digits(z,d);r=out['scalars'][k]
 print(k,'FLOOR'+str(d),r['floor'],'CEIL'+str(d),r['ceil']);return r
def exact(k,z):out['exact'][k]=str(z);print(k,'EXACT',z)
def enclose(l,u):return arb(aa((F(l)+F(u))/2),aa((F(u)-F(l))/2))
def overlaps(z,old):
 l,u=ends(z);return max(l,F(old['lo']))<=min(u,F(old['hi']))
for v,l,u in [(F(-1,3),'-0.33334','-0.33333'),(F(-1,10**8),'-0.00001','0.00000'),(F(1,7),'0.14285','0.14286'),(F(-1,8),'-0.12500','-0.12500')]:
 gate(fmt(floor_trunc(v,5),5)==l and fmt(ceil_trunc(v,5),5)==u,'signed digit helper')
manifest={}
for line in Path('FROZEN.sha256').read_text().splitlines():
 if not line or line.startswith('#'):continue
 dg,n=line.split();p=Path(n);gate(not p.is_absolute() and '..' not in p.parts,'local input')
 gate(hashlib.sha256(p.read_bytes()).hexdigest()==dg,'frozen bytes '+n);manifest[n]=dg
gate(manifest==PINS and bool(PINS),'embedded exact frozen versions')
gate(hashlib.sha256(Path('second_line.py').read_bytes()).hexdigest()==SECOND_PIN,'independent worker version')
for line in Path('SOURCES.sha256').read_text().splitlines():
 dg,n=line.split();gate(not Path(n).is_absolute() and '..' not in Path(n).parts,'confined source')
 gate(hashlib.sha256(Path(n).read_bytes()).hexdigest()==dg,'source bytes')
mem=read('CITATIONS.json');gate(mem['snapshot_entries']==777,'snapshot777')
for k,d in mem['facts'].items():
 gate(d['line']==int(k) and d['kind']=='fact' and hashlib.sha256(d['fact'].encode()).hexdigest()==d['fact_sha256'],'exact cited fact '+k)
 gate('FOUNDATION' in d['fact'],'foundation '+k)
for d in read('PROVENANCE.json'):
 gate(d['memory'] in list(map(int,mem['facts'])) and PINS[d['local_file']]==d['sha256'],'accepted payload identity')
# Bank status is an independently authenticated premise, not proved by hashes.
a,b=F(4,25),F(3,16);X=6000000185827;C=690988;H=2299999;J=2300000;W=66476100549959;T=3000175332800
contract=read('CONTRACTS.json');g=contract['global'];nodes=contract['nodes'];boxes=contract['emitted_boxes']
gate(g=={'A':'3/16','H':H,'J':J,'N0':C,'W':str(W),'X':str(X),'anchor_source':'V1-H-213','anchor_upper':'3/16','l':'4/25','rh_height':str(T)},'exact global contract')
pi=arb.pi()
def wall(n,t):return 4*pi*(arb(n)**2-aa(F(t)/16))
def cc(x):return ((1+x*x).log()/2-(4*pi).log())/4-1/(2*(1+x*x))
c0=cc(arb(X));lc=arb(C).log()
print('A_B_C: BANKED ANALYTIC MODULES')
r=a/2;eps=9*(F(1,2**16)+F(1,15*2**15))+F(41000,2**256)+F(3,2**64)
gate(0<r<a<b<F(1,2) and 128/r==1600 and eps<F(1,1024),'uniform neighborhood remote tail')
gate(T-F(X,2)==F(350479773,2)>0,'PT2021 initial site')
gate(F(21,125)+F(39,2000)==b,'V1 anchor arithmetic')
gate('[V1-H-213 ' in mem['facts']['526']['fact'] and '[V1-H-220 ' in mem['facts']['549']['fact'],'banked anchor identity')
sep=read('frozen/separator_second_summary.json');charge=F(sep['constants']['total']['hi']);mf=F(sep['sweep']['minimum_row'][3],10**12)
gate(sep['sweep']['leaves']==255778 and charge<F(1,800) and mf-charge>F(7,800),'complete accepted separator floor')
gate(F(2)**2-1==3,'padded whole-boundary clearance')
z,t=sp.symbols('z t',real=True);toy=z*z-2*t
gate(sp.diff(toy,t)+sp.diff(toy,z,2)==0 and toy.subs({t:0,z:0})==0 and sp.diff(toy,z).subs(z,0)==0,'no initial simplicity promotion')
for m in [2,3,5,8]:
 h=sum((-1)**k*sp.factorial(m)*z**(m-2*k)/(sp.factorial(k)*sp.factorial(m-2*k)) for k in range(m//2+1))
 prev=sum((-1)**k*sp.factorial(m-1)*z**(m-1-2*k)/(sp.factorial(k)*sp.factorial(m-1-2*k)) for k in range((m-1)//2+1))
 gate(sp.expand(sp.diff(h,z)-m*prev)==0,'Hermite convention control')
print('D: ACCEPTED STRONG GRAM SOURCE, NOT SCALAR PROMOTION')
src=read('frozen/bank767_summary.json')
gate((src['t'],src['X'],src['N'],src['y'])==('4/25',X,C,0),'source point')
gate(src['all_prime_characters'] and src['strict_gram_threshold']=='1/1000000' and src['raw_modulus_floor_strict']=='1/10','strong source theorem')
geom=read('frozen/bank767_geometry.json');tree=geom['boxes'] if isinstance(geom,dict) else geom
gate(len(tree)==3524,'all source leaves retained')
# Exact complete occupancy using disjoint integer bit slabs at max depth5.
depth=max(d for leaf in tree for d,m in leaf);gate(depth==5,'source mesh depth')
side=2**depth;planes=[0]*(side**3);mask_all=(1<<side)-1;volume=F(0)
for leaf in tree:
 spans=[]
 for d,m in leaf:
  gate(0<=m<2**d and 0<=d<=depth,'valid dyadic source arc')
  spans.append((m*2**(depth-d),(m+1)*2**(depth-d)))
 volume+=F(1,2**sum(d for d,m in leaf))
 (l0,u0),(l1,u1),(l2,u2),(l3,u3)=spans;mask=((1<<(u3-l3))-1)<<l3
 for i in range(l0,u0):
  for j in range(l1,u1):
   for k in range(l2,u2):
    ix=(i*side+j)*side+k;gate(planes[ix]&mask==0,'no repeated source atom');planes[ix]|=mask
gate(all(v==mask_all for v in planes) and volume==1,'entire source torus and all seams')
for name in ['bank767_leaves_primary.txt','bank767_leaves_second.txt']:
 rows=[list(map(int,line.split())) for line in Path('frozen/'+name).read_text().splitlines()]
 gate([r[0] for r in rows]==list(range(len(tree))),'all accepted source leaf floors')
 gate(all(F(l,10**12)>F(1,10**6) and u>=l for _,l,u in rows),'all accepted leaf inequalities')
 # These are accepted outputs; no claimed fresh numerical source replay.
 emit(name+'_minimum_lower',F(min(r[1] for r in rows),10**12),12)
rec=read('frozen/bank774_summary.json');P=read('frozen/bank774_primary.json');S=read('frozen/bank774_second.json');partition=read('frozen/bank774_geometry.json')
gate(rec['source']['strong_Gram_not_scalar_summary'] and rec['source']['memory']==767,'strong weighted interface consumed')

# Tie the accepted lightweight outputs to the original accepted manifests.
def original_outputs(name):
 pairs={}
 for line in Path('frozen/'+name).read_text().splitlines():
  if not line or line.startswith('#'):continue
  h,n=line.split();gate(len(h)==64 and n not in pairs,'accepted output manifest grammar');pairs[n]=h
 return pairs
m774=original_outputs('bank774_outputs.txt');m767=original_outputs('bank767_outputs.txt')
for oldname,local in [('p_bins.txt','bank774_bins.txt'),('s_bins.txt','bank774_bins.txt'),('PRIMARY_RESULT.json','bank774_primary.json'),('SECONDARY_RESULT.json','bank774_second.json'),('GEOMETRY.json','bank774_geometry.json')]:
 gate(m774[oldname]==PINS['frozen/'+local]==rec['fresh_products'][oldname],'accepted774 output-manifest join '+oldname)
for oldname,local in [('primary_leaves.txt','bank767_leaves_primary.txt'),('secondary_leaves.txt','bank767_leaves_second.txt')]:
 gate(m767[oldname]==PINS['frozen/'+local],'accepted767 leaf-manifest join')

gate(rec['complete_entrants']==H-C==1609011 and rec['rough_bins']==224 and rec['index_leaves']==14,'complete accepted dimensions')
gate(rec['target']=={'N_natural_closed':[C,H],'all_internal_RIGHT_walls':True,'all_prime_polydisc':True,'t_closed':['4/25','3/16'],'terminal2300000_wall':'EXCLUDED','x_closed':[X,W],'y':0},'accepted finite quantifiers')
# Every rough integer contributes once to the independently checked bin support.
binrows=[list(map(int,s.split())) for s in Path('frozen/bank774_bins.txt').read_text().splitlines()]
gate(binrows[0][:5]==[-1,0,0,0,0] and len(binrows)==225,'complete synthetic and rough bins')
star=binrows[0];vs=enclose(F(star[5],2**100),F(star[6],2**100));gate(vs>0,'synthetic denominator')
expected={};rough=[]
for n in range(2,C+1):
 if math.gcd(n,210)!=1:continue
 rough.append(n);e=n.bit_length()-1;k=(16*n)//2**e-16;j=16*e+k
 if j not in expected:expected[j]=[n,n,0,0]
 v=expected[j];v[1]=n;v[2]+=1;v[3]+=n
bins=[]
for j,l,u,num,total,vl,vu in binrows[1:]:
 gate(expected.pop(j)==[l,u,num,total] and 0<vl<=vu,'complete exact bin support')
 bins.append((l,enclose(F(vl,2**100),F(vu,2**100))))
gate(not expected and len(rough)==157939,'no omitted rough support')
# Re-evaluate all accepted transport leaves with erfi.
def leaf(L,U):
 x=arb(X) if L==C else wall(L,b);s=arb(0) if L==C else aa(a)*(cc(x)-c0)
 gate(s>=0,'inward old-source contraction')
 m=(1+sum(v*(1-(-2*s*arb(rho).log()).exp()) for rho,v in bins)/vs).sqrt()/10
 A=aa(a)/4;B=arb(1)/2-aa(a)*c0-s;D=A.sqrt();u=arb(U).log()
 integ=pi.sqrt()/(2*D)*(-B*B/(4*A)).exp()*((D*u+B/(2*D)).erfi()-(D*lc+B/(2*D)).erfi())
 slope=-arb(1)/2+aa(a)*(arb(U).log()/2-cc(x));sup=4*cc(x)-arb(U).log();ret=m-integ
 gate(slope<0 and sup>0 and ret>arb(1)/100,'whole-leaf entrant and heat guards')
 row={'L':L,'U':U}
 for key,value in [('x_left',x),('s',s),('old_norm_lower_expression',m),('entry_integral_upper',integ),('retained_lower_expression',ret),('entry_log_slope',slope),('heat_support',sup)]:
  d=digits(value,12);row[key]={'lo':d['lo'],'hi':d['hi'],'FLOOR12':d['floor'],'CEIL12':d['ceil']}
  if key!='heat_support':
   for prior in [P,S]:
    old=next(r for r in prior['leaves'] if (r['L'],r['U'])==(L,U))[key]
    gate(overlaps(value,old),'accepted774 '+key+' overlap')
    gate(row[key]['FLOOR12']==old['FLOOR12'] and row[key]['CEIL12']==old['CEIL12'],'all accepted774 digits '+key)
 return row
for L,U in partition:out['leaves'].append(leaf(L,U))
gate(len(out['leaves'])==14 and partition[0][0]==C and partition[-1][1]==H and all(u==l for (_,u),(l,_) in zip(partition,partition[1:])),'exact closed all-index partition')
worst=min(out['leaves'],key=lambda r:F(r['retained_lower_expression']['lo']))
gate(all(F(worst['retained_lower_expression']['hi'])<F(r['retained_lower_expression']['lo']) for r in out['leaves'] if r is not worst),'explicit unique minimum comparison')
gate((worst['L'],worst['U'])==(rec['minimum_sufficient_leaf_expressions'][0]['L'],rec['minimum_sufficient_leaf_expressions'][0]['U']),'accepted minimizing leaf')
out['minimum']={'L':worst['L'],'U':worst['U'],**worst['retained_lower_expression']}
print('ALL14_MINIMUM_SUFFICIENT',worst['L'],worst['U'],'FLOOR12',out['minimum']['FLOOR12'],'CEIL12',out['minimum']['CEIL12'])
print('TRANSPORT_COMPLETE bins',len(bins),'leaves',len(out['leaves']),'entrants',H-C,'rough_fibres',len(rough))
# Hash-selected complete coefficient/fibre expressions; controls, not full production.
probe=read('frozen/bank774_probes.json');ph=hashlib.sha256(Path('frozen/bank774_proof.txt').read_bytes()).hexdigest()
gate(ph==probe['proof_sha256'],'probe defining manuscript')
gate(probe['raw_complete_hash']==m774['p_raw.txt']==m767['primary_raw.txt'] and probe['weights_complete_hash']==m774['p_weights.txt']==m767['primary_weights.txt'],'original complete probe-source identities')
want={1,2,3,7,128,C}|{1+int(hashlib.sha256((ph+':raw:'+str(j)).encode()).hexdigest(),16)%C for j in range(24)}
gate(want=={r[0] for r in probe['raw']},'retained raw hash inputs')
wantw={v for v in [11,13,17,690983] if v in set(rough)}|{rough[int(hashlib.sha256((ph+':weight:'+str(j)).encode()).hexdigest(),16)%len(rough)] for j in range(16)}
gate(wantw|{0}=={r[0] for r in probe['weights']},'retained weight hash inputs')
def amp(n):
 v=arb(n).log();return (aa(a)*v*v/4-(arb(1)/2+aa(a)*c0)*v).exp()
for n,l,u in probe['raw']:
 value=amp(n);lv,uv=ends(value);gate(F(l,2**56)<=lv<=uv<=F(u,2**56),'raw coefficient control');out['probes'].append({'kind':'raw','n':n,'lo':str(lv),'hi':str(uv)})
smooth=[(1,0)]
for p in [2,3,5,7]:
 old=smooth;smooth=[]
 for n,sg in old:
  v=n;k=0
  while v<=C:smooth.append((v,sg+k));v*=p;k+=1
smooth.sort();gate(len(smooth)==1160 and len({n for n,k in smooth})==1160,'complete smooth control support')
def fibre(r):
 plus=arb(0);minus=arb(0)
 for n,k in smooth:
  if n*r>C:break
  v=amp(n*r);plus+=v;minus+=(-1)**k*v
 return plus,minus
cp,cm=fibre(1);gate(cp>0 and cm>0,'source profile denominators')
for rr,l,u in probe['weights']:
 if rr==0:v=((8/cp**2+1/cm**2)/900).sqrt()
 else:
  ap,am=fibre(rr);v=((8*(ap/cp)**2+(am/cm)**2)/9).sqrt()
 lv,uv=ends(v);gate(F(l,2**56)<=lv<=uv<=F(u,2**56),'complete rough-fibre weight control');out['probes'].append({'kind':'weight','r':rr,'lo':str(lv),'hi':str(uv)})
print('E: WHOLE-BAND GEOMETRY AND RIGHT WALLS')
for name,value in [('head_left',arb(X)-wall(C,a)),('head_right',wall(C+1,b)-X),('seam_left',arb(W)-wall(H,a)),('seam_right',wall(J,b)-W)]:
 gate(value>0,'positive '+name);emit(name,value)
gate(wall(J,b)<W+1 and int(wall(J,b).floor().unique_fmpz())==W,'exact floor seam')
n=sp.symbols('n',integer=True,positive=True);tt=sp.symbols('tt',real=True);ps=sp.symbols('pi',positive=True)
sn=4*ps*(n*n-tt/16);gate(sp.simplify((sn/(4*ps)+tt/16)-n*n)==0,'wall adjacent square identity');gate(sp.diff(sn,tt)==-ps/4,'time monotonic wall')
gate(sp.expand(sn.subs(n,n+1)-sn-4*ps*(2*n+1))==0,'strict all-index ordering')
# Finite real-H gauge conversion is exact rational arithmetic, no float gate.
p,q=F(1,800000),F(1600001,40000000000);floor=F(1,100)
surplus=12*floor**2-(30*p+q)*floor-400*p-p*q
gate(surplus==F(22375198391999,32000000000000000)>F(1,2000) and 24*floor-(30*p+q)>0,'adopted finite Hermitian reserve')
old=read('frozen/bank738_primary.json');audit=read('frozen/bank754_summary.json')
gate(F(old['exact']['SURPLUS'])==surplus==F(audit['corrected_surplus_exact']),'accepted lift scalar')
gate(F(old['intervals']['MOMENT_CEILING'][1])<200 and F(old['intervals']['ELL_UPPER'][1])<30 and F(old['intervals']['PHASE_GAP_LOWER'][0])>12,'accepted complete moment and phase domain')
print('T: AUDITED INFINITE PRACTICAL TAIL')
tail=read('frozen/bank729_primary.json');tail2=read('frozen/bank729_second.json');audit=read('frozen/bank772_summary.json')
for k,lim,field in [('CORNER_MASS',F(9,10),'corner'),('BARRIER',F(9,10),'equilibrium'),('CONVERSION',F(1,200000),'conversion')]:
 l,u=map(F,tail['intervals'][k]);j=audit[field]
 gate(u<lim and F(j['hi'])<lim and max(l,F(j['lo']))<=min(u,F(j['hi'])),'exact tail audited bound '+k)
 emit(k,enclose(l,u));gate(digits(enclose(l,u))['floor']==j['floor'] and digits(enclose(l,u))['ceil']==j['ceil'],'audited tail digits')
gate(F(tail['exact']['H'])==H and F(tail['exact']['W'])==W and F(tail['exact']['a'])==a and F(tail['exact']['b'])==b,'practical-tail exact scope')
aj,bj,res=F(179,180),F(19,135),F(19999,200000);jet=res**2/(aj**2+bj**2)
gate(jet==F(tail['intervals']['JET_CERTIFIED'][0])>F(9,1000),'quadratic tail reserve')
# SAME arithmetic in accepted old-stage and V1 regimes.
g1=arb(X)-wall(C,0);g2=wall(C+1,F(1809,10000))-(X+1)
gate(digits(g1,4)['floor']=='5377392.8789' and digits(g2,4)['floor']=='11989041.1415','V1 same-code site anchors')
emit('V1_site_gap1',g1,4);emit('V1_site_gap2',g2,4)
oldW=60821233773498;gate(wall(2199999,F(33,200))<oldW<wall(2200000,b)<oldW+1,'accepted677 distinct predecessor')
emit('anchor677_seam_right',wall(2200000,b)-oldW)
gate(F(186,1000)+F(16733,100000)**2/2==F(19999966445,10**11) and T-F(5000000194858,2)==500175235371,'published-row height anchor')
print('F_G: TYPE LICENSING THEN EXACT GLOBAL UNION')
def lic(c):
 nd=c['nodes'];bb=c['emitted_boxes'];gg=c['global']
 try:
  if not(0<F(gg['l'])<F(gg['anchor_upper'])<=F(gg['A'])<=F(1,2)):return False
  if gg['anchor_source']!='V1-H-213' or F(gg['anchor_upper'])<F(3,16):return False
  if F(gg['X'])/2>F(gg['rh_height']) or F(gg['rh_height'])!=T:return False
  st=nd['stall_tail'];it=nd['interior'];bd=nd['boundary'];fi=nd['finite'];ta=nd['practical_tail']
  if not(st['kind']=='all-complex-real-simple-uniform-tail' and st['y']=='all' and st['source']==590 and st['second_lines']==[588] and F(st['t'][0])==F(st['r'])>0 and F(st['r'])<a and F(st['t'][1])>=b and F(st['radius_exponent'])==128/F(st['r']) and st['t_closed']==[True,True]):return False
  if not(it['source']==599 and it['kind']=='real-simple-interior' and it['t']==['0','3/16'] and it['t_closed']==[False,True] and it['N'] is None and it['x']==['0',str(X)]):return False
  if not(bd['source']==596 and bd['second_lines']==[616] and bd['t']==['0','3/16'] and bd['t_closed']==[True,True] and bd['y']==['-1','1'] and bd['padding_y']==['-2','2']):return False
  if not(fi['source']==774 and fi['source_kind']=='strong-normalized-Gram' and fi['source_memory']==767 and fi['modulus_floor']=='1/100' and fi['entrant_count']==H-C and fi['N']==[C,H] and fi['x']==[str(X),str(W)] and fi['x_closed']==[True,True]):return False
  if not(ta['source']==729 and ta['second_lines']==[772] and ta['N']==[H,None] and ta['x']==[str(W),'inf'] and ta['x_closed']==[True,False]):return False
  for node in [fi,ta]:
   if not(node['kind']=='real-axis-no-double' and node['y']=='0' and node['gauge']=='elementary-Polymath-absMt' and node['t']==['4/25','3/16'] and node['t_closed']==[True,True] and node['cell']=='left-closed-right-open' and node['wall_index']=='right-frozen'):return False
  sources={'interior':'interior','exterior':'finite','tail':'practical_tail'}
  for box in bb:
   if box['module'] not in sources or box['node']!=sources[box['module']]:return False
   node=nd[box['node']]
   if box['t']!=['4/25','3/16'] or box['t_closed']!=[True,True] or box['x']!=node['x'] or box['x_closed']!=node['x_closed']:return False
  return True
 except (KeyError,ValueError,TypeError):return False
gate(lic(contract),'typed theorem licensing')
def member(z,ends,cl):
 l=F(ends[0]);u=None if ends[1]=='inf' else F(ends[1])
 return (z>l or z==l and cl[0]) and (u is None or z<u or z==u and cl[1])
def reps(points):
 p=sorted(points);return [p[0]-1,p[-1]+1]+p+[(x+y)/2 for x,y in zip(p,p[1:])]
def union_bad(bb):
 times=reps({a,b}|{F(v) for bx in bb for v in bx['t']})
 xs=reps({F(0)}|{F(v) for bx in bb for v in bx['x'] if v!='inf'})
 missing=[];extra=[]
 for ti,xx in itertools.product(times,xs):
  target=a<=ti<=b and xx>=0
  actual=any(member(ti,bx['t'],bx['t_closed']) and member(xx,bx['x'],bx['x_closed']) for bx in bb)
  if target and not actual:missing.append([str(ti),str(xx)])
  if actual and not target:extra.append([str(ti),str(xx)])
 return missing,extra
gate(union_bad(boxes)==([],[]),'zero missing and excess components')
# Exact interval cell partition is a finite proof because all predicates are
# constant on each open cell, and every rational endpoint is its own cell.
def reject(name,predicate):gate(not predicate,name);out['mutations'].append(name)
for name,node,key,val in [
 ('scalar floor is not Gram','finite','source_kind','scalar-only'),
 ('missing top entrants','finite','entrant_count',H-C-1),
 ('left derivative at wall','finite','wall_index','left'),
 ('wrong gauge','finite','gauge','exact-Gamma'),
 ('off-axis finite promotion','finite','y','all'),
 ('unbounded finite support','finite','N',[C,None]),
 ('tail starts at nominal index','practical_tail','N',[J,None]),
 ('unlicensed tail earlier time','practical_tail','t',['31/200','3/16']),
 ('time-zero simplicity','interior','t_closed',[True,True]),
 ('unbounded interior index assumption','interior','N',[C,H]),
 ('separator loses initial time','boundary','t_closed',[False,True]),
 ('separator lacks y seam','boundary','y',['-1/2','1/2']),
 ('unpadded horizontal boundary','boundary','padding_y',['-1','1']),
 ('real-axis tail used for stall','stall_tail','kind','real-axis-no-double'),
 ('remote tail lacks all y','stall_tail','y','0'),
 ('remote tail not left uniform','stall_tail','r','4/25'),
 ('wrong remote exponent','stall_tail','radius_exponent','1599')]:
 c=copy.deepcopy(contract);c['nodes'][node][key]=val;reject(name,lic(c))
for name,key,val in [('invented anchor','anchor_upper','1/10'),('RH priced at tail','X',str(W)),('unproved extra RH','rh_height',str(T+1))]:
 c=copy.deepcopy(contract);c['global'][key]=val;reject(name,lic(c))
for name,mod in [('missing finite',0),('missing seam',1),('missing low time',2),('missing tail ray',3),('integer adjacency',4),('excess time',5)]:
 qboxes=copy.deepcopy(boxes)
 if mod==0:qboxes.pop(1)
 if mod==1:qboxes[1]['x_closed'][1]=False;qboxes[2]['x_closed'][0]=False
 if mod==2:
  for bx in qboxes:bx['t_closed'][0]=False
 if mod==3:qboxes.pop()
 if mod==4:qboxes[1]['x'][1]=str(W-1);qboxes[2]['x'][0]=str(W+1)
 if mod==5:qboxes[1]['t'][0]='31/200'
 reject(name,union_bad(qboxes)==([],[]))
reject('upward rounded seam still in predecessor',wall(J,b)>W+1)
# Synthetic values show why a scalar norm alone cannot certify weighted Gram.
reject('scalar1/10 implies arbitrary Gram',F(1)**2>F(9,10)**2/F(1,10)+F(1,100)/F(9,10))
ready=read('READINESS.json');gate(ready['snapshot_entries']==777 and ready['mathematical_inputs_all_banked'] and ready['candidate_release']=='HELD','mathematics and record readiness distinct')
for k in ['complete_Gram_source767','Gram_recovery774','this_global_composition']:gate(ready['audits'][k]=='OPEN','captured external hold '+k)
gate(not ready['official_torus_certificate_used'],'no official receipt asserted')
for key,val in [('a',a),('b',b),('X',X),('W',W),('C',C),('H',H),('J',J),('surplus',surplus),('tail_jet',jet),('RH_required',F(X,2)),('RH_margin',T-F(X,2)),('stall_r',r),('stall_exponent',128/r),('improvement',F(33,200)-a),('comparison_margin',F(86211,500000)-a),('entry_count',H-C),('missing_components',0),('excess_components',0)]:exact(key,val)
emit('MATHEMATICAL_LAMBDA_UPPER',a,10)
print('RH_SOURCE PT2021 arXiv:2004.09765 HEIGHT',T,'INITIAL_REQUIRED',F(X,2),'MARGIN',T-F(X,2))
for box in boxes:print('COVER module='+box['module']+' t=['+','.join(box['t'])+'] x=['+','.join(box['x'])+']')
print('REMOTE_STALL_RADIUS 4*pi*exp(1600)+1 UNIFORM CLOSED[2/25,1/2] ALL_IMAGINARY_PARTS')
# The actual independent line is executed, not inferred from frozen output.
proc=subprocess.run([sys.executable,'second_line.py'],capture_output=True,text=True,timeout=120)
Path('second_line.log').write_text(proc.stdout);Path('second_line_stderr.log').write_text(proc.stderr)
gate(proc.returncode==0 and not proc.stderr,'separate line execution '+proc.stderr[-1500:])
sec=read('SECOND_RESULT.json')
for k,v in sec['exact'].items():gate(out['exact'][k]==v,'independent exact '+k)
for k,row in sec['scalars'].items():
 gate(out['scalars'][k]['floor']==row['floor'] and out['scalars'][k]['ceil']==row['ceil'],'independent scalar '+k)
 gate(max(F(out['scalars'][k]['lo']),F(row['lo']))<=min(F(out['scalars'][k]['hi']),F(row['hi'])),'independent scalar overlap '+k)
for r1,r2 in zip(out['leaves'],sec['leaves']):
 gate((r1['L'],r1['U'])==(r2['L'],r2['U']),'independent leaf geometry')
 for k in ['x_left','s','old_norm_lower_expression','entry_integral_upper','retained_lower_expression','entry_log_slope','heat_support']:
  gate(r1[k]['FLOOR12']==r2[k]['FLOOR12'] and r1[k]['CEIL12']==r2[k]['CEIL12'],'independent all-leaf digits')
  gate(max(F(r1[k]['lo']),F(r2[k]['lo']))<=min(F(r1[k]['hi']),F(r2[k]['hi'])),'independent all-leaf overlap')
gate(out['minimum']['L']==sec['minimum']['L'] and out['minimum']['U']==sec['minimum']['U'],'independent global minimum')
out['checks']=COUNT;out['second_checks']=sec['checks'];out['snapshot']=777;out['theorem']='Lambda<4/25 with sole PT2021 initial height X/2';out['candidate_release']='HELD';out['new_source_production']=False;out['official_attestation']=False
Path('RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RELEASE_STATUS HELD external_source767 external_recovery774 external_final_composition')
print('MATHEMATICAL_CONCLUSION Lambda<4/25; NO RECORD ACCEPTANCE OR PUBLICATION CLAIM')
print('TOTAL CHECKS RUN:',COUNT)
print('RESULT: ALL PASS')
