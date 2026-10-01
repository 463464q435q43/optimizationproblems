#!/usr/bin/python3
"""Separate real-gauge, ordered-factorization and Machin arithmetic.
No import from verify.py or any producer helper. All universal mass results
remain consumed banked hypotheses; frozen replays audit their interfaces.
"""
from fractions import Fraction as R
from pathlib import Path
from mpmath import iv
import ast
import hashlib
import json

iv.dps=85
A,T=R(333,2000),R(3,16)
X,N0,NT,D=6000000185827,690988,1499999,1024
count=0


def gate(s,p):
    global count
    if not p:raise AssertionError(s)
    count+=1;print('SECOND_PASS',s,flush=True)

def v(q):
    q=R(q);return iv.mpf(q.numerator)/q.denominator

def endpoints(z):
    ans=[]
    for sign,m,e,_ in z._mpi_:ans.append(R((-1 if sign else 1)*m)*R(2)**e)
    return tuple(ans)

def floor_trunc(q,d):
    q=R(q);n=q.numerator*10**d//q.denominator
    return ('-' if n<0 else '')+str(abs(n)//10**d)+('.'+str(abs(n)%10**d).zfill(d) if d else '')
def ceil_trunc(q,d):
    q=R(q);n=-((-q.numerator*10**d)//q.denominator)
    return floor_trunc(R(n,10**d),d)

def emit(name,z,d=18):
    l,h=endpoints(z) if hasattr(z,'_mpi_') else (R(z),R(z))
    print('SECOND_'+name,'FLOOR'+str(d),floor_trunc(l,d),'CEIL'+str(d),ceil_trunc(h,d))
    print('SECOND_'+name+'_EXACT',l,h)

gate('negative floor',floor_trunc(R(-13,11),4)=='-1.1819')
gate('negative ceiling',ceil_trunc(R(-13,11),4)=='-1.1818')
gate('tiny signed values',floor_trunc(R(-1,10**9),4)=='-0.0001' and ceil_trunc(R(-1,10**9),4)=='0.0000')
gate('positive rounding',floor_trunc(R(2,3),4)=='0.6666' and ceil_trunc(R(2,3),4)=='0.6667')
mods=[]
for node in ast.walk(ast.parse(Path('second_line.py').read_text())):
    if isinstance(node,ast.Import):mods.extend(x.name for x in node.names)
    if isinstance(node,ast.ImportFrom):mods.append(node.module)
gate('independent module boundary',all(z not in ['verify','flint','primary','second'] for z in mods))
print('SECOND_SOURCE_SHA256',hashlib.sha256(Path('second_line.py').read_bytes()).hexdigest())
model=json.loads(Path('frozen/model_primary.json').read_text())
family={s:json.loads(Path('frozen/l8_'+s+'.json').read_text()) for s in ['primary','independent']}

# A finite Neumann expansion: ordered factors >=2 imply length at most 10.
ld=[v(0)]+[iv.log(d) for d in range(1,D+1)]
xx=v(X)
cx=iv.log(xx/(4*iv.pi))/4+iv.log(1+xx**-2)/8-1/(2*(1+xx*xx))
sx=v(R(1,2))+v(A)*cx
base=[v(0)]+[iv.exp(v(A)*ld[d]**2/4) for d in range(1,D+1)]
coef=[v(0) for _ in range(D+1)];coef[1]=v(1)
prev={1:v(1)}
for length in range(1,11):
    nxt={}
    for a,z in prev.items():
        for d in range(2,D//a+1):nxt[a*d]=nxt.get(a*d,v(0))+z*base[d]
    for m,z in nxt.items():coef[m]+=(-1 if length%2 else 1)*z
    prev=nxt
gate('ordered factorization terminates',all(2*m>D for m in prev))
gate('unit exact',endpoints(coef[1])==(R(1),R(1)))
resmax=R(0)
for m in range(2,D+1):
    residual=sum((coef[d]*base[m//d] for d in range(1,m+1) if m%d==0),v(0))
    l,h=endpoints(residual)
    if not l<=0<=h:raise AssertionError('inverse residual '+str(m))
    resmax=max(resmax,-l,h)
gate('all inverse equations and precision',resmax<R(1,10**65))
emit('ORDERED_INVERSE_RESIDUAL',resmax,65)
mu=[coef[d]*iv.exp(-sx*ld[d]) for d in range(D+1)]
e0=sum((abs(z) for z in mu[1:]),v(0));mass1=sum((abs(mu[d])*ld[d] for d in range(1,D+1)),v(0))
gate('same actual E norm budget',endpoints(e0)[1]<R(41,20) and endpoints(v(R(500000000001,10**12))*mass1)[1]<R(51,50))

# Physical shifted complex controls at independently hash-chosen model centers.
seed=hashlib.sha256(Path('frozen/model_proof.txt').read_bytes()).digest()
times=[A,T,A+(T-A)*R(int.from_bytes(seed[:2],'big'),65536)]
for j,t in enumerate(times):
    x=v(X if j==0 else (28274333882307 if j==1 else X+int.from_bytes(seed[2:4],'big')))
    s=(1+iv.j*x)/2
    alpha=1/(2*s)+1/(s-1)+iv.log(s/(2*iv.pi))/2
    alphap=-1/(2*s*s)-1/(s-1)**2+1/(2*s)
    w=s+v(t)*alpha/2;wp=iv.j*(1+v(t)*alphap/2)/2
    thetap=(alpha+v(t)*alpha*alphap/2).real/2
    E=iv.mpc(0);Ew=iv.mpc(0)
    for d in range(1,D+1):
        z=coef[d]*iv.exp(-w*ld[d]);E+=z;Ew-=ld[d]*z
    q=4*(thetap-(Ew*wp/E).imag);ell=q/(2*wp.imag)
    gate('actual nonzero same E '+str(j),endpoints(abs(E))[0]>R(1,4))
    gate('shifted actual two-scale probe '+str(j),endpoints(q)[0]>17 and endpoints(ell)[0]>17)
    shift=v(t)*(7*x*x-5)/(4*(1+x*x)**2)
    l,h=endpoints(wp.imag-v(R(1,2))-shift)
    gate('imaginary heat-derivative identity '+str(j),l<=0<=h and endpoints(w.imag-x/2)[0]>0)
    emit('PHYSICAL_Q_'+str(j),q);emit('PHYSICAL_ELL_'+str(j),ell)

# Use independently computed producer prefix bounds, not primary partition.
def raw_ball(text):
    m,e,r,f=[int(s,16) for s in text.split()]
    center=R(m)*R(2)**e;radius=R(r)*R(2)**f
    return center-radius,center+radius
bins=[]
for line in Path('frozen/model_second_prefix.log').read_text().splitlines():
    if line.startswith('BIN '):
        _,l,r,raw=line.split(' ',3);lo,hi=raw_ball(raw);bins.append((int(l),int(r),lo,hi))
gate('different complete signed-prefix partition',len(bins)==108 and bins[0][0]==D+1 and bins[-1][1]==N0 and all(a[1]+1==b[0] for a,b in zip(bins,bins[1:])))
B=R(model['consumed_B']);used=sum((z[3] for z in bins),R(0))
gate('prefix subtraction exposed with positive factors',used<B and all(l<N0+1 for l,_,_,_ in bins))
rows=model['rows'];initial_bounds=[]
for row in rows:
    na,nb,xlow=row['l'],row['r'],row['x_lower'];x=v(xlow)
    ca=iv.log(x/(4*iv.pi))/4+iv.log(1+x**-2)/8-1/(2*(1+x*x))
    delta=v(A)*(ca-cx) if xlow!=X else v(0)
    sigma=v(R(1,2))+v(A)*ca
    old=v(B-used)*iv.exp(-delta*iv.log(N0+1))
    for l,r,ll,hh in bins:old+=v(hh)*iv.exp(-delta*iv.log(l))
    step=(iv.log(nb)-iv.log(N0))/67;integ=v(0)
    for k in range(68):
        z=iv.log(N0)+k*step
        integ+=iv.exp(v(A)*z*z/4+(1-sigma)*z)*(1 if k in [0,67] else 2)
    integ*=step/2
    esum=v(0)
    for d in range(1,D+1):
        wl,wh=endpoints(2*(ld[d]+iv.log(nb))/17-1)
        weight=v(max(R(1),wl))+iv.mpf([0,1])*v(max(R(1),wh)-max(R(1),wl))
        esum+=abs(coef[d])*iv.exp(-sigma*ld[d])*weight
    total=old+integ*esum
    gate('entire spatial interval '+str(na),endpoints(total)[1]<R(47,50))
    initial_bounds.append(endpoints(total)[1])
gate('no integer gaps',rows[0]['l']==N0 and rows[-1]['r']==NT and all(r['r']+1==s['l'] for r,s in zip(rows,rows[1:])))
gate('scalar whole-time convex endpoint',endpoints(v(R(47,50))*iv.exp(-34*v(T-A))+21*v(T-A))[1]<R(47,50))
emit('ALL_BLOCK_UPPER',max(initial_bounds))

# Sparse exact polynomials for the real-coordinate derivative identity.
# Coordinates: h, ImZ, sigma', ReW, tau', ImW.
zero=(0,)*6
def var(k):
    a=list(zero);a[k]=1;return {tuple(a):R(1)}
def add(*ps):
    out={}
    for p in ps:
        for m,c in p.items():out[m]=out.get(m,R(0))+c
    return {m:c for m,c in out.items() if c}
def mul(p,q):
    out={}
    for a,c in p.items():
        for b,d in q.items():
            m=tuple(i+j for i,j in zip(a,b));out[m]=out.get(m,R(0))+c*d
    return {m:c for m,c in out.items() if c}
def scale(p,a):return {m:a*c for m,c in p.items() if a*c}
h,iz,sg,rw,tp,iw=[var(k) for k in range(6)]
# h*ImG=h*ImZ-tau'*ImW; differentiate 2ReZ without division.
lhs=add(scale(mul(h,iz),-2),scale(mul(sg,rw),-2),scale(mul(tp,iw),2))
rhs=add(scale(add(mul(h,iz),scale(mul(tp,iw),-1)),-2),scale(mul(sg,rw),-2))
gate('generic real-gauge derivative polynomial',lhs==rhs)
wrong=add(scale(mul(h,iz),-2),scale(mul(tp,iw),2))
gate('mutation dropped real-exponent drift detected',lhs!=wrong)
# Orthogonal phase projection is multiplication by a unit complex scalar.
# For real r,r',Theta', |r'+iTheta'r|^2=r'^2+(Theta'r)^2.
r,rp,th=var(0),var(1),var(2)
projection=add(mul(rp,rp),mul(mul(th,r),mul(th,r)))
gate('orthogonal projection residual nonnegative monomial',add(projection,scale(mul(rp,rp),-1))==mul(mul(th,r),mul(th,r)))
# A finite product showing the beyond-N support is nonempty and indispensable.
lambda_toy={1:R(1),2:R(-3,2),3:R(-5,4)}
b_toy={1:R(1),2:R(3,2),3:R(5,4),4:R(7,4)}
prod={}
for d,c in lambda_toy.items():
    for n,z in b_toy.items():prod[d*n]=prod.get(d*n,R(0))+c*z
gate('all products exact and unit',prod[1]==1 and all(prod.get(m,R(0))==sum((c*b_toy[m//d] for d,c in lambda_toy.items() if m%d==0 and m//d in b_toy),R(0)) for m in range(1,13)))
gate('high-edge deletion mutation nonvacuous',any(c!=0 for m,c in prod.items() if m>4))

# Independent direct gauge charge, exact fractions and a series log bound.
sigcap=T*(R(1,4*X)+R(1,X**3))
term=R(1);exp_lower=R(1)
for k in range(1,100):term*=R(22,k);exp_lower+=term
gate('logarithmic support via exponential series',exp_lower>D*NT)
ev,ed=R(655217372417,10**18),R(37300347933869,10**18)
charge=R(229,200)*ev+R(41,170)*ed+sigcap*R(47,50)*R(88,17)
cap=R(10581704117220,10**18)
gate('direct real-gauge coefficients',R(41,40)+R(102,850)==R(229,200) and R(41,10*17)==R(41,170))
gate('direct charge strictly below banked family cap',charge<cap<R(1,50000))
reserve=R(3,50)-cap
gate('strict new full-exterior reserve',reserve==R(2999470914794139,50000000000000000)>R(2999,50000))
emit('DIRECT_GAUGE_CHARGE',charge);emit('RESERVE',reserve)
# Independent family extraction and old charge calibration.
for name,f in family.items():
    rv,rd=R(f['raw']['Ev'][1]),R(f['raw']['Ed'][1])
    speed=R(500000000001,10**12)
    scalar=(R(21,20)+5*speed/16)*rv+R(21,80)*rd+sigcap*(R(21,10)*1640+R(5,2)*21)/4
    gate('family scalar '+name,scalar<=cap and ceil_trunc(scalar,18)==ceil_trunc(cap,18))
old=(R(41,40)+R(1,2))*R(682857503579,10**18)+R(41,160)*R(114077128828636,10**18)+R(1,8*10**12)
gate('old L7 exact anchor',old==R(605472441605919,20000000000000000000))
tail=(R(9,10)+R(3,65))*ev+R(9,65)*ed+R(1,13*10**13)
gate('true tail exact anchor',tail==R(751998000616933,130000000000000000000))

# Independent Machin rational enclosure, with tangent and branch validation.
def atan(q,terms):
    s=sum((R((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(terms)),R(0))
    other=s+R((-1)**terms,(2*terms+1)*q**(2*terms+1))
    return min(s,other),max(s,other)
a,b=atan(5,70);c,d=atan(239,25)
pi_lo,pi_hi=16*a-4*d,16*b-4*c
z=R(1,5);z2=2*z/(1-z*z);z4=2*z2/(1-z2*z2)
gate('Machin tangent', (z4-R(1,239))/(1+z4/239)==1)
gate('Machin branch and width',0<4*a-d<4*b-c<1 and 3<pi_lo<pi_hi<R(22,7) and pi_hi-pi_lo<R(1,10**80))
def wall(n,t):
    s=4*(n*n-R(t)/16);return s*pi_lo,s*pi_hi
wl,wh=wall(NT+1,T);W=wl.numerator//wl.denominator
gate('unique floor and strict seam',W==wh.numerator//wh.denominator==28274333882307 and W<wl<wh<W+1)
gate('X whole-time first cell',wall(N0,A)[1]<X<wall(N0+1,T)[0])
gate('W whole-time last cell',wall(NT,A)[1]<W<wall(NT+1,T)[0])
gate('ceiling seam cannot borrow missing cell',wall(NT+1,T)[1]<W+1<wall(NT+2,T)[0])
for row in rows:
    gate('all lower walls adverse endpoint '+str(row['l']),row['x_lower']==X if row['l']==N0 else row['x_lower']<wall(row['l'],T)[0])
emit('RIGHT_WALL_MINUS_W',wl-W)
gate('contextual PT2021 height',R(3000175332800)-R(X,2)==R(350479773,2)>0)
print('SECOND_DOMAIN t=['+str(A)+','+str(T)+'] N=['+str(N0)+','+str(NT)+'] y=0 W='+str(W))
Path('second_summary.json').write_text(json.dumps({'snapshot':619,'W':W,'direct_charge':str(charge),'family_charge_cap':str(cap),'reserve':str(reserve),'N':[N0,NT],'all_block_upper':str(max(initial_bounds)),'checks':count},sort_keys=True,indent=2)+'\n')
print('SECOND_CHECKS',count)
print('SECOND: ALL PASS')
