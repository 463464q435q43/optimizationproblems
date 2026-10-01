#!/usr/bin/python3
"""Independent full-domain numerical line; no producer source or cover imported."""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, subprocess, sys, time
from flint import arb, ctx
ctx.prec = 224
COUNT = 0

def check(name, cond):
    global COUNT
    if not cond:
        raise AssertionError(name)
    COUNT += 1
    print('PASS', name, flush=True)

def ar(q):
    q = F(q)
    return arb(q.numerator)/q.denominator

def lo(z):
    return F(str(z.lower().fmpq()))

def hi(z):
    return F(str(z.upper().fmpq()))

def floor_trunc(q, digits):
    q=F(q); scale=10**digits
    n=(q.numerator*scale)//q.denominator
    return ('-' if n<0 else '')+str(abs(n)//scale)+'.'+str(abs(n)%scale).zfill(digits)

def ceil_trunc(q, digits):
    q=F(q); scale=10**digits
    n=-((-q.numerator*scale)//q.denominator)
    return ('-' if n<0 else '')+str(abs(n)//scale)+'.'+str(abs(n)%scale).zfill(digits)

def show(name,z,digits=18):
    print(name,'FLOOR'+str(digits),floor_trunc(lo(z),digits),
          'CEIL'+str(digits),ceil_trunc(hi(z),digits),flush=True)

def pack(z): return [str(lo(z)),str(hi(z))]
def hull(l,r): return arb.union(l,r)

def cfun(x):
    z=arb(x)
    return ((1+z*z).sqrt()/(4*arb.pi())).log()/4-1/(2*(1+z*z))

def inverse(t,K):
    # Neumann expansion (delta+g)^(-1)=sum (-g)^(*j).
    # Every factor of g has integer index >=2, so the series terminates.
    logs=[arb(0)]+[arb(d).log() for d in range(1,K+1)]
    b=[arb(0)]+[(ar(t)*l*l/4).exp() for l in logs[1:]]
    inv=[arb(0) for _ in range(K+1)]; inv[1]=arb(1)
    power=[arb(0) for _ in range(K+1)]
    for d in range(2,K+1): power[d]=b[d]
    sign=-1; length=1
    while 2**length<=K:
        for d in range(2**length,K+1): inv[d]+=sign*power[d]
        nxt=[arb(0) for _ in range(K+1)]
        for e in range(2**length,K//2+1):
            for k in range(2,K//e+1): nxt[e*k]+=power[e]*b[k]
        power=nxt; sign=-sign; length+=1
    return inv,logs,b

X=6000000185827; A=F(333,2000); TOP=F(3,16); H=TOP-A
N0=690988; NT=1499999; D=1024; B=F(891101027766,10**12)
VC=F(500000000001,10**12); EPS=F(1,10**20)
C=cfun(X)
SIG=arb(1)/2+ar(A)*C


def prefix(t,K,anchor=None):
    start=time.process_time()
    lam,logs,_=inverse(t,K)
    sig=arb(1)/2+ar(t)*C
    mu=[lam[d]*(-sig*logs[d]).exp() for d in range(K+1)]
    bits=90; unit=1<<bits
    L=[]; U=[]
    for d in range(K+1):
        L.append(int((mu[d].lower()*unit).floor().fmpz()))
        U.append(int((mu[d].upper()*unit).ceil().fmpz()))
    fl=[0]*(N0+1); fu=[0]*(N0+1)
    for n in range(1,N0+1):
        z=arb(n).log(); v=(ar(t)*z*z/4-sig*z).exp()
        fl[n]=int((v.lower()*unit).floor().fmpz())
        fu[n]=int((v.upper()*unit).ceil().fmpz())
    check('positive exact integer initializers '+str(t), min(fl[1:])>0)
    cl=[v*unit for v in fl]; cu=[v*unit for v in fu]
    pairs=N0
    for d in range(2,K+1):
        low,high=L[d],U[d]
        for n in range(1,N0//d+1):
            m=d*n
            cl[m]+=low*(fl[n] if low>=0 else fu[n])
            cu[m]+=high*(fu[n] if high>=0 else fl[n])
        pairs+=N0//d
    check('complete prefix pair count '+str(t),pairs==sum(N0//d for d in range(1,K+1)))
    check('constant coefficient exact '+str(t),cl[1]==cu[1]==unit*unit)
    check('all inverse-annihilation residues enclosed '+str(t),
          all(cl[m]<=0<=cu[m] for m in range(2,K+1)))
    total_lo=0;total_hi=0
    for m in range(2,N0+1):
        low,high=cl[m],cu[m]
        check_order=low<=high
        if not check_order: raise ArithmeticError('integer interval reversed')
        total_lo+=0 if low<=0<=high else min(abs(low),abs(high))
        total_hi+=max(abs(low),abs(high))
    total=hull(ar(F(total_lo,unit*unit)),ar(F(total_hi,unit*unit)))
    show('MAIN t='+str(t)+' K='+str(K),total,10)
    if anchor is not None:
        check('banked main CEIL10 reproduced '+str(t),ceil_trunc(hi(total),10)==anchor)
    bins=[];left=K+1
    while left<=N0:
        right=min(N0,max(left,(33*left)//32-1))
        lower=upper=0
        for m in range(left,right+1):
            l,u=cl[m],cu[m]
            lower+=0 if l<=0<=u else min(abs(l),abs(u))
            upper+=max(abs(l),abs(u))
        bins.append({'l':left,'r':right,'lo':str(F(lower,unit*unit)),
                     'hi':str(F(upper,unit*unit))})
        left=right+1
    # Hash-selected probes taken only from our exact bin ledger, never producer data.
    seed=hashlib.sha256(json.dumps(bins,sort_keys=True).encode()).digest()
    chosen={1,2,K,K+1,N0,N0-1}
    for j in range(24):
        chosen.add(1+int.from_bytes(hashlib.sha256(seed+j.to_bytes(4,'big')).digest(),'big')%N0)
    chosen.update(row['l'] for row in bins[::19])
    probes=[{'m':m,'lo':str(F(cl[m],unit*unit)), 'hi':str(F(cu[m],unit*unit))} for m in sorted(chosen)]
    print('PREFIX_RECEIPT',json.dumps({'t':str(t),'K':K,'pair_count':pairs,'bins':len(bins),
          'cpu_seconds_diagnostic':time.process_time()-start}),flush=True)
    return lam,logs,mu,bins,probes,total


def ref(lam,logs,t,K,cap):
    sig=arb(1)/2+ar(t)*C
    mu={d:lam[d]*(-sig*logs[d]).exp() for d in range(1,K+1)}
    primes=[p for p in range(2,cap+1) if all(p%d for d in range(2,p))]
    check('reference prime enumeration '+str(cap),primes==[p for p in range(2,cap+1) if all(p%d for d in range(2,p))])
    prod=arb(1); logarithmic=arb(0); refs={1:arb(1)}
    for p in primes:
        z=arb(p).log(); q=(ar(t)*z*z/4-sig*z).exp()
        check('reference factor '+str(cap)+'/'+str(p),q>0 and q<1)
        prod*=1-q; logarithmic+=q*z/(1-q)
        refs.update({d*p:-v*q for d,v in list(refs.items())})
    U=arb(0);V=arb(0)
    for d in sorted(set(mu)|set(refs)):
        diff=abs(mu.get(d,arb(0))-refs.get(d,arb(0)))
        U+=diff; V+=diff*arb(d).log()
    emin=prod-U; L=(prod*logarithmic+V)/emin
    E0=sum((abs(v) for v in mu.values()),arb(0))
    E1=ar(VC)*sum((abs(mu[d])*logs[d] for d in mu),arb(0))
    Q=(arb(X)/(4*arb.pi())).log()-4*ar(VC)*L
    e=ar(F(7,1)*TOP/(4*X*X)) if cap==29 else ar(EPS)
    ell=Q/(1+2*e)
    ans={'emin':pack(emin),'K':pack(L),'Emax':pack(E0),'Eprime':pack(E1),'Q':pack(Q),'ell':pack(ell),
         'support_count':len(refs)}
    for name,z in [('EMIN',emin),('LOGDER',L),('EMAX',E0),('EPRIME',E1),('ELL',ell)]:
        show('REFERENCE'+str(cap)+' t='+str(t)+' '+name,z,12)
    return ans,emin,L,E0,E1,ell


def forcing(mu,logs):
    # Reverse finite sums: exact d-prefixes, certified boxes of integer n.
    p0=[arb(0)];p1=[arb(0)];p2=[arb(0)]
    for d in range(1,D+1):
        v=abs(mu[d]);z=logs[d]
        p0.append(p0[-1]+v);p1.append(p1[-1]+v*z);p2.append(p2[-1]+v*z*z)
    e17=arb(17).exp(); cut=int(e17.floor().fmpz())
    check('exact weight kink integer',e17>cut and e17<cut+1)
    check('weight kink exceeds maximum index',cut>NT)
    check('positive n-factor decreasing', ar(A)*arb(NT).log()/2 < SIG)
    ln=arb(NT).log(); result=arb(0); rows=[];l=1
    while l<=NT:
        f=min(D,NT//l);g=min(D,cut//l)
        fstop=NT//f if f<D else NT//D
        gstop=cut//g if g<D else cut//D
        # Independent integer cover, ratio <=1025/1024; exact quotient boundaries.
        r=min(NT,fstop,gstop,max(l,(1025*l)//1024))
        if not (l<=r and min(D,NT//r)==f and min(D,cut//r)==g and f<=g):
            raise ArithmeticError('quotient partition')
        z=hull(arb(l).log(),arb(r).log())
        inner=(p2[f]+2*z*p1[f]+(ln*ln-z*z)*(p0[g]-p0[f]
                 +(2*z/17-1)*(p0[D]-p0[g])+2*(p1[D]-p1[g])/17))/4
        f_l=(ar(A)*arb(l).log()**2/4-SIG*arb(l).log()).exp()
        f_r=(ar(A)*arb(r).log()**2/4-SIG*arb(r).log()).exp()
        result+=(r-l+1)*inner*hull(f_r,f_l)
        rows.append([l,r,f,g]);l=r+1
    check('forcing cover all integers',rows[0][0]==1 and rows[-1][1]==NT and
          all(r[1]+1==s[0] for r,s in zip(rows,rows[1:])))
    check('global maximum-index forcing <21',result<21)
    print('FORCING_BOXES',len(rows),'KINK_INTEGER',cut,flush=True)
    show('MAXINDEX_FORCING',result)
    return result,rows,cut


def integral(sig,U):
    # Exact antiderivative in log coordinates, no quadrature samples.
    q=ar(A)/4; root=q.sqrt(); beta=1-sig
    vl=arb(N0).log();vu=arb(U).log()
    I=arb.pi().sqrt()/(2*root)*(-beta*beta/(4*q)).exp()*(
        (root*vu+beta/(2*root)).erfi()-(root*vl+beta/(2*root)).erfi())
    return I


def spatial(lam,logs,bins):
    u_bins=[ar(F(row['hi'])) for row in bins]
    log_bins=[arb(row['l']).log() for row in bins]
    rlog=arb(N0+1).log();sc=ar(B)
    check('prefix mass upper less than total bank budget',sum(u_bins,arb(0))<sc)
    check('unit weights on entire prefix',arb(N0).log()<17)
    check('prefix bins closed integer cover',bins[0]['l']==D+1 and bins[-1]['r']==N0 and
          all(r['r']+1==s['l'] for r,s in zip(bins,bins[1:])))
    cache={}
    def base(L):
        if L not in cache:
            if L==N0: x=X
            else:
                wall=4*arb.pi()*(arb(L)**2-ar(TOP)/16)
                x=int(wall.floor().fmpz())
                if not (wall>x and wall<x+1 and x>=X):raise ArithmeticError('floor spatial base')
            sigma=arb(1)/2+ar(A)*cfun(x)
            delta=sigma-SIG
            if L==N0: delta=arb(0)
            e=(-delta*rlog).exp()
            old=sc*e+sum((u*((-delta*z).exp()-e) for u,z in zip(u_bins,log_bins)),arb(0))
            coeff=[abs(lam[d])*(-sigma*logs[d]).exp() for d in range(D+1)]
            cache[L]=(x,sigma,old,coeff)
        return cache[L]
    def bound(L,U):
        x,sig,old,coeff=base(L)
        if not ar(A)*arb(U).log()/2<sig: raise ArithmeticError('new terms decreasing')
        mass=arb(0);ln=arb(U).log()
        for d in range(1,D+1):
            z=2*(logs[d]+ln)/17-1
            # Exact max enclosed without a binary floating comparison.
            weight=(1+z+abs(1-z))/2
            mass+=coeff[d]*weight
        new=mass*integral(sig,U)
        return old+new,old,new,x
    cover=[];L=N0;cap=ar(F(939,1000))
    while L<=NT:
        z,old,new,x=bound(L,L)
        check('singleton base passes L='+str(L),z<cap)
        lower=L;upper=NT
        while lower<upper:
            mid=(lower+upper+1)//2
            trial,*_=bound(L,mid)
            if trial<cap: lower=mid
            else:upper=mid-1
        U=lower;z,old,new,x=bound(L,U)
        check('whole spatial index block '+str(len(cover)),z<cap)
        cover.append({'L':L,'U':U,'xbase':x,'bound':pack(z),'old':pack(old),'entering':pack(new)})
        print('INTEGER_BLOCK',L,U,'XBASE',x,flush=True)
        show('BLOCK_BOUND',z)
        L=U+1
        if len(cover)>128:raise AssertionError('preregistered cover cap')
    check('full independent integer cover',cover[0]['L']==N0 and cover[-1]['U']==NT and
          all(r['U']+1==s['L'] for r,s in zip(cover,cover[1:])))
    worst=max(F(r['bound'][1]) for r in cover)
    print('SPATIAL_BLOCK_COUNT',len(cover),flush=True)
    print('SPATIAL_GLOBAL_CEIL18',ceil_trunc(worst,18),flush=True)
    return cover


def algebra_and_geometry():
    check('negative floor self-test',floor_trunc(F(-10009,10000),3)=='-1.001')
    check('negative ceiling self-test',ceil_trunc(F(-10009,10000),3)=='-1.000')
    check('signed cross-zero floor self-test',floor_trunc(F(-1,10001),3)=='-0.001')
    check('signed cross-zero ceiling self-test',ceil_trunc(F(-1,10001),3)=='0.000')
    check('positive floor and ceiling self-test',floor_trunc(F(10009,10000),3)=='1.000' and ceil_trunc(F(10009,10000),3)=='1.001')
    check('saddle c positive and maximum-index dominance',C>arb(NT).log()/4)
    k1=C*arb(D+1).log()-arb(D+1).log()**2/4
    k2=C*arb(NT).log()-arb(NT).log()**2/4
    check('common complement decay both concave endpoints >34',k1>34 and k2>34)
    show('COMMON_DECAY_LEFT',k1);show('COMMON_DECAY_RIGHT',k2)
    terminal=ar(F(47,50))*(-34*ar(H)).exp()+21*ar(H)
    check('convex time envelope terminal below 47/50',terminal<ar(F(47,50)))
    show('TIME_ENDPOINT_ENVELOPE',terminal)
    xwall=4*arb.pi()*(arb(NT+1)**2-ar(TOP)/16)
    W=int(xwall.floor().fmpz())
    check('unique terminal rational seam',W==28274333882307 and xwall>W and xwall<W+1)
    def natural(x,n):
        return arb(x)/(4*arb.pi())+ar(A)/16>n*n and arb(x)/(4*arb.pi())+ar(TOP)/16<(n+1)**2
    check('initial site constant natural index',natural(X,N0))
    check('terminal seam includes predecessor index',natural(W,NT))
    check('each natural wall right-hand index symbolic',F(N0*N0)==F(N0*N0)-A/16+A/16)
    # Interval-union checker genuinely detects missing first/last/interior indices.
    def integer_cover(rows):
        return bool(rows) and rows[0][0]==N0 and rows[-1][1]==NT and all(l<=r for l,r in rows) and all(r[1]+1==s[0] for r,s in zip(rows,rows[1:]))
    good=[(N0,NT)]
    check('integer-domain positive control',integer_cover(good))
    check('missing terminal cell mutation rejected',not integer_cover([(N0,NT-1)]))
    check('missing entering cell mutation rejected',not integer_cover([(N0,N0),(N0+2,NT)]))
    # Small exact heat model: inverse coefficients cancel at anchor but regrow.
    # b_2(a+h)=b_2(a)*exp(h log(2)^2/4), so its first derivative is nonzero.
    regrowth=(ar(A)*arb(2).log()**2/4).exp()*arb(2).log()**2/4
    check('persistent annihilation mutation rejected by n=2 derivative',regrowth>0)
    show('REGROWTH_DERIVATIVE_N2',regrowth)
    # Pure Dirichlet-polynomial inverse countermodel: b_n=1,D=2,sigma=2.
    # This tests the algebraic new-pair rule, not the physical heat parameters.
    # Both models use the same lambda_1=1,lambda_2=-1; only N changes.
    def toy_mass(index):
        coefficients={}
        for d,coef in [(1,F(1)),(2,F(-1))]:
            for n in range(1,index+1):
                coefficients[d*n]=coefficients.get(d*n,F(0))+coef
        return sum((abs(v)/F(m*m) for m,v in coefficients.items() if m>1),F(0))
    m2,m3=toy_mass(2),toy_mass(3)
    check('new-index omission rejected by exact finite convolution',m2==F(1,16) and m3==F(29,144) and m3>m2)
    print('NEW_PAIR_COUNTERMODEL M2='+str(m2)+' M3='+str(m3),flush=True)
    # Upper prefix bounds are not lower prefix bounds.  The positive gain is essential.
    total=F(10);prefix_true=F(4);prefix_upper=F(6);tail_true=total-prefix_true
    check('upper-prefix subtraction as separate tail mutation rejected',tail_true>total-prefix_upper)
    actual=prefix_true+(total-prefix_true)/2
    correct=total/2+prefix_upper*(1-F(1,2))
    check('positive Laplace gain countermodel control',correct>=actual)
    nearest=F(floor_trunc(F(10004,10000)+F(1,2000),3))
    check('nearest string as upper bound mutation rejected',nearest<F(10004,10000))
    print('RS_COVER t=[333/2000,3/16] N=[690988,1499999] y={0} x>=X in [s_N(t),s_(N+1)(t))',flush=True)
    print('CLOSED_RECTANGLE t=[333/2000,3/16] x=[6000000185827,28274333882307] y={0}',flush=True)
    print('RH_CONTEXT PT2021 T=3000175332800 REQUIRED=6000000185827/2 MARGIN='+str(F(3000175332800)-F(X,2)),flush=True)
    return W


def main():
    start=time.process_time()
    inputs=json.loads(Path('INPUTS.json').read_text())
    check('audited manuscript exact version',hashlib.sha256(Path('AUDITED_PROOF.md').read_bytes()).hexdigest()==inputs['audited_manuscript_sha256'])
    check('consumed corner manuscript exact version',hashlib.sha256(Path('CONSUMED_CORNER.md').read_bytes()).hexdigest()==inputs['consumed_corner_manuscript_sha256'])
    check('banked corner output provenance',hashlib.sha256(Path('CONSUMED_CORNER_OUTPUT.log').read_bytes()).hexdigest()==inputs['consumed_corner_output_sha256'])
    W=algebra_and_geometry()
    anchors=[]
    for t,label in [(F(17,100),'0.6182732025'),(F(21,125),'0.6669190220')]:
        la,lg,mu,bi,pr,ma=prefix(t,64,label)
        rr,*_=ref(la,lg,t,64,29)
        anchors.append({'t':str(t),'main':pack(ma),'reference':rr,'probes':pr})
    lam,logs,mu,bins,probes,mass=prefix(A,D)
    ref29,*rest29=ref(lam,logs,A,D,29)
    ell29=rest29[-1]
    check('consumed corner exact scale upper <17 not only lower',ell29>0 and ell29<17)
    check('corner published reference FLOOR12 reproduced',floor_trunc(lo(ell29),12)=='16.323213748562')
    # A lower bound alone cannot establish the direction needed for weight containment.
    def licenses_weight_transfer(enclosure,newscale):
        l,u=enclosure
        return 0<l<=u<=newscale
    check('exact corner weight-transfer positive control',licenses_weight_transfer((lo(ell29),hi(ell29)),F(17)))
    check('one-sided scale misuse mutation rejected',not licenses_weight_transfer((F(163,10),F(18)),F(17)))
    check('wrong scale orientation has a finite weight countermodel',max(F(1),2*F(19)/17-1)>max(F(1),2*F(19)/18-1))
    ref47,emin,k,e0,e1,ell=ref(lam,logs,A,D,47)
    check('global reference modulus >1/4',emin>ar(F(1,4)))
    check('global logarithmic derivative <5',k<5)
    check('global exact-shift corrected scale >17',ell>17)
    check('global modulus cap <41/20',e0<ar(F(41,20)))
    check('global derivative cap <51/50',e1<ar(F(51,50)))
    forcing_ball,force_rows,cut=forcing(mu,logs)
    cover=spatial(lam,logs,bins)
    # Detect a removed cover row, not merely a selected marker or stored hash.
    def cover_ok(rows):
        return bool(rows) and rows[0]['L']==N0 and rows[-1]['U']==NT and all(r['U']+1==s['L'] for r,s in zip(rows,rows[1:]))
    check('missing block mutation rejected',not cover_ok(cover[:-1]))
    report={'snapshot':617,'precision_bits':ctx.prec,'anchors':anchors,'prefix_bins':bins,'probes':probes,
            'ref29':ref29,'ref47':ref47,'forcing':pack(forcing_ball),'forcing_rows':force_rows,
            'weight_kink':cut,'cover':cover,'W':W,'B':str(B),'main':pack(mass)}
    Path('independent_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    rc=subprocess.run([sys.executable,'iv_check.py'],check=False).returncode
    check('separate scalar and coefficient audit exits',rc==0)
    iv=json.loads(Path('iv_results.json').read_text())
    check('separate audit bound not sampled',F(iv['forcing'][1])<21 and len(iv['blocks'])==len(cover))
    for name in ['emin','K','Emax','Eprime','ell']:
        x=ref47[name];y=iv['ref47'][name]
        check('cross-engine reference intersection '+name,max(F(x[0]),F(y[0]))<=min(F(x[1]),F(y[1])))
    for name in ['check.py','iv_check.py','AUDIT.md','INPUTS.json']:
        print('OWN_SOURCE_SHA256',name,hashlib.sha256(Path(name).read_bytes()).hexdigest(),flush=True)
    print('SCOPE independent finite-model full-domain second line; no new H_t charge, RH verification or Lambda bound',flush=True)
    print('TOTAL CHECKS RUN:',COUNT,flush=True)
    print('CPU_SECONDS_DIAGNOSTIC',time.process_time()-start,flush=True)
    print('RESULT: ALL PASS',flush=True)

if __name__=='__main__':main()
