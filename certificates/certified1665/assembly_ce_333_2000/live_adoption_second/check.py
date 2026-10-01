#!/usr/bin/python3
"""External adoption line, standalone. No producer module imports."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
import sympy as S
from mpmath import iv
iv.dps=80
checks=0

def gate(name,ok):
    global checks
    if not ok:raise AssertionError(name)
    checks+=1;print('PASS',name,flush=True)

def floor_trunc(q,n):
    q=Q(q);d=10**n;p=q.numerator*d//q.denominator
    return ('-' if p<0 else '')+str(abs(p)//d)+'.'+str(abs(p)%d).zfill(n)

def ceil_trunc(q,n):
    q=Q(q);d=10**n;p=-((-q.numerator*d)//q.denominator)
    return ('-' if p<0 else '')+str(abs(p)//d)+'.'+str(abs(p)%d).zfill(n)

def val(q):
    q=Q(q);return iv.mpf(q.numerator)/q.denominator

def fraction(t):
    s,m,e,b=t;return Q((-1 if s else 1)*m)*Q(2)**e

def ends(z):return fraction(z._mpi_[0]),fraction(z._mpi_[1])
def store(z):return [str(q) for q in ends(z)]
def display(name,z,n=18):
    l,u=ends(z);print(name,'FLOOR'+str(n),floor_trunc(l,n),'CEIL'+str(n),ceil_trunc(u,n),flush=True)

def exponential(q,count):
    q=Q(q);t=Q(1);s=t
    for k in range(1,count+1):t*=q/k;s+=t
    nxt=t*q/(count+1);ratio=q/(count+2)
    if not 0<=ratio<1:raise ValueError('series tail ratio')
    return s,s+nxt/(1-ratio)

def arctan_inverse(k,count):
    s=Q(0)
    for j in range(count):s+=Q((-1)**j,(2*j+1)*k**(2*j+1))
    nxt=Q((-1)**count,(2*count+1)*k**(2*count+1))
    return min(s,s+nxt),max(s,s+nxt)

def symbolic():
    # All real variables, so conjugation and real projection have no hidden hypothesis.
    zr,zi,wr,wi,h,sp,tp=S.symbols('zr zi wr wi h sp tp', real=True)
    ell=2*h/tp
    z=zr+S.I*zi;w=wr+S.I*wi
    dz=S.I*h*z-(sp+S.I*tp)*w
    G=z-w/ell+S.conjugate(w)/ell
    gate('resultant real projection exact',S.simplify(S.re(G)-zr)==0)
    identity=S.expand(2*S.re(dz)+2*h*S.im(G)+2*sp*wr)
    gate('real-gauge derivative exact including sigma drift',identity==0)
    gate('sigma drift deletion mutation rejected',S.expand(2*S.re(dz)+2*h*S.im(G))!=0)
    flat=z-w/(4*h)+S.conjugate(w)/(4*h)
    wrong=S.factor(2*S.re(dz)+2*h*S.im(flat)+2*sp*wr)
    gate('flat-scale mutation witness',wrong==wi*(2*tp-1))
    r,p,q=S.symbols('r p q',real=True)
    Tr=(1-r)*(p+S.I*q)+r*(p-S.I*q)
    nrm=S.expand(Tr*S.conjugate(Tr))
    gate('weighted coefficient norm low regime',S.expand(p*p+q*q-nrm-4*r*(1-r)*q*q)==0)
    gate('weighted coefficient norm high regime',S.expand((2*r-1)**2*(p*p+q*q)-nrm-4*r*(r-1)*p*p)==0)
    # R=exp(iTheta)*(u-V): its co-rotating real derivative is u'-V'.
    u,V,up,Vp,theta,dtheta=S.symbols('u V up Vp theta dtheta',real=True)
    inside=(up-Vp)+S.I*dtheta*(u-V)
    gate('real normalized error derivative has no phase penalty',S.simplify(S.re(inside)-(up-Vp))==0)
    # Entire-support polynomial identity and raw-normalized inverse uniqueness.
    q2,q3,q4,q5,q6,zeta=S.symbols('b2 b3 b4 b5 b6 z',real=True)
    b={1:S.Integer(1),2:q2,3:q3,4:q4,5:q5,6:q6}
    lam={1:S.Integer(1)}
    for d in range(2,7):lam[d]=S.expand(-sum(lam[e]*b[d//e] for e in range(1,d) if d%e==0))
    for d in range(2,7):gate('triangular inverse identity '+str(d),S.expand(sum(lam[e]*b[d//e] for e in lam if d%e==0))==0)
    # Normalization is encoded by prime exponents rather than independent n variables.
    ps=[2,3,5];variables=S.symbols('v2 v3 v5',nonzero=True)
    def norm(n):
        out=S.Integer(1)
        for p,v in zip(ps,variables):
            while n%p==0:out*=v;n//=p
        if n!=1:raise ValueError('basis')
        return out
    for n in range(2,7):
        rec=lam[n]*norm(n)+sum(lam[e]*norm(e)*b[n//e]*norm(n//e) for e in range(1,n) if n%e==0)
        gate('raw to normalized inverse identity '+str(n),S.expand(rec)==0)
    # Log moment envelope derivative checked exactly in its independent L variable.
    x,L=S.symbols('x L',positive=True)
    form=2*S.Rational(3,16)*(S.Rational(1,4)/x+1/x**3)*L
    derivative=S.diff(form,x)+S.diff(form,L)/(2*x)
    desired=2*S.Rational(3,16)*((S.Rational(1,2)-L)/(4*x*x)+(S.Rational(1,2)-3*L)/x**4)
    gate('tail drift derivative universal identity',S.simplify(derivative-desired)==0)
    return {'flat_scale_residual':str(wrong),'tail_drift_derivative':str(desired)}


def arithmetic():
    X=6000000185827;Y=26000000000000;a=Q(333,2000);b=Q(3,16)
    n0=690988;nT=1499999;D=1024
    v=Q(655217372417,10**18);d=Q(37300347933869,10**18)
    sig=b*(Q(1,4*X)+Q(1,X**3));family_cap=Q(529085205861,50000000000000000)
    VC=Q(500000000001,10**12)
    A_sigma=2*sig*(Q(21,10)*1640+Q(5,2)*21)
    def charge(E0,E1,P,ve,de,drift):return E0*ve/2+2*(E1*ve+E0*de+drift)/P
    family=charge(Q(21,10),VC*Q(5,2),16,v,d,A_sigma)
    exact_raw_charges={}
    for nm in ['BANK605_primary.json','BANK605_independent.json']:
        raw=json.loads(Path(nm).read_text())['raw']
        vl,vu=map(Q,raw['Ev']);dl,du=map(Q,raw['Ed'])
        exact_charge=charge(Q(21,10),VC*Q(5,1)/2,16,vu,du,A_sigma)
        gate('bank605 raw enclosures fit printed upper inputs '+nm,0<vl<=vu<=v and 0<dl<=du<=d)
        gate('full-rational raw replay reaches original family ceiling '+nm,exact_charge<=family_cap)
        gate('family directed CEIL18 anchor '+nm,ceil_trunc(exact_charge,18)=='0.000010581704117220')
        exact_raw_charges[nm]=str(exact_charge)
        print('BANK605_FULL_RAW_CHARGE',nm,'CEIL18',ceil_trunc(exact_charge,18),flush=True)
    # The printed CEIL endpoints of v,d can widen past the previously banked
    # family ceiling.  The universal family cap is consumed as a theorem;
    # do not demand that rounded raw endpoints reproduce its last digit.
    gate('family theorem cap below global budget',family_cap<Q(1,50000))
    gate('family raw-ceiling recomputation nearby conservative',family<Q(1,50000))
    tail=charge(Q(9,5),Q(3,5),26,v,d,Q(1,10**13))
    gate('bank613 tail charge exact',tail==Q(751998000616933,130000000000000000000))
    gate('tail charge cap',tail<Q(3,500000))
    gate('tail reserve strict lower comparison',1-Q(43,50)-tail>Q(69997,500000))
    older=charge(Q(41,20),Q(4),16,Q(682857503579,10**18),Q(114077128828636,10**18),Q(1,10**12))
    gate('bank606 different charge regime exact',older==Q(605472441605919,20000000000000000000))
    # A direct real-gauge route for finite exterior, conditional only on its mass/reference premises.
    coeff_u=Q(41,20)/2+2*Q(51,50)/17;coeff_du=2*Q(41,20)/17
    gate('finite real-gauge value coefficient',coeff_u==Q(229,200))
    gate('finite real-gauge derivative coefficient',coeff_du==Q(41,170))
    exp22lo,_=exponential(Q(22),160)
    gate('finite product log-degree below22 by positive series',exp22lo>D*nT)
    drift_finite=2*sig*Q(47,50)*22
    direct=coeff_u*v+coeff_du*d+2*drift_finite/17
    gate('direct real-gauge charge below family theorem cap',direct<family_cap)
    reserve=1-Q(47,50)-family_cap
    gate('published finite reserve exact',reserve==Q(2999470914794139,50000000000000000))
    gate('finite reserve target',reserve>Q(2999,50000))
    gate('both E multipliers omission is detectable',charge(2,0,16,1,1,0)>charge(1,0,16,1,1,0))
    # Tail half-line drift: monotone L(x)=log D+log x/2, derivative signs depend on L>1/2.
    L=iv.log(30030)+iv.log(Y)/2
    F=2*val(b)*(val(Q(1,4*Y))+val(Q(1,Y**3)))*L
    gate('tail endpoint log-moment positive',ends(L)[0]>Q(1,2))
    gate('tail entire-half-line drift cap',ends(F)[1]<Q(1,10**13))
    gate('tail lower geometric wall using pi>3',12*(Q(nT*nT)-b/16)>Y)
    gate('H5 strict positivity for all tail points',a*(3*Y-2)>6)
    h5tail=(val(a)*iv.pi*Y/4-val(a)/2-val(Q(3,2)))/(1+val(Y)**2)
    gate('independent H5 tail lower endpoint positive',ends(h5tail)[0]>0)
    Ktail=val(Q(87,100))
    proxy=(iv.log(val(Y)/(4*iv.pi))-4*val(VC)*Ktail)/(1+2*val(Q(1,10**24)))
    gate('tail proxy exceeds26 from coarse Y and K',ends(proxy)[0]>26)
    # eta and |w'| at Y: pointwise estimates are monotone half-line envelopes.
    sx=val(b)*(val(Q(1,4*Y))+val(Q(1,Y**3)))
    etacap=val(7*b/(4*Y*Y))
    gate('tail eta cap satisfies cited envelope',ends(etacap)[1]<Q(1,10**24))
    speed=iv.sqrt(sx*sx+(val(Q(1,2))+etacap)**2)
    gate('tail x-derivative speed satisfies cited envelope',ends(speed)[1]<VC)
    for nm,z in [('TAIL_H5_ENDPOINT',h5tail),('TAIL_PHASE_PROXY',proxy)]:display(nm,z)
    display('TAIL_DRIFT_ENDPOINT',F)
    # Do not claim family raw rounded-endpoint equality if last digit differs.
    for nm,q in [('FAMILY_CHARGE_THEOREM',family_cap),('FAMILY_RAW_CEILING_RECOMPUTATION',family),('TAIL_CHARGE',tail),('OLDER_CHARGE_ANCHOR',older),('DIRECT_FINITE_CHARGE',direct),('FINITE_RESERVE',reserve)]:
        print(nm,'EXACT',q,'FLOOR18',floor_trunc(q,18),'CEIL18',ceil_trunc(q,18),flush=True)
    print('FINITE_REAL_GAUGE_COEFFICIENTS',coeff_u,coeff_du,flush=True)
    return {'full_raw_charges':exact_raw_charges,'family_cap':str(family_cap),'family_raw_ceiling_recomputation':str(family),'tail':str(tail),'older':str(older),'direct':str(direct),'reserve':str(reserve),'tail_drift':store(F)}


def geometry():
    lo5,hi5=arctan_inverse(5,96);lo239,hi239=arctan_inverse(239,32)
    pl=16*lo5-4*hi239;pu=16*hi5-4*lo239
    gate('Machin pi enclosure crosses independent interval',pl<ends(iv.pi)[1] and pu>ends(iv.pi)[0])
    gate('exact pi coarse bounds',3<pl<pu<Q(22,7))
    a=Q(333,2000);b=Q(3,16);n0=690988;nt=1499999;X=6000000185827;W=28274333882307
    def wall(n,t):return 4*pl*(n*n-t/16),4*pu*(n*n-t/16)
    low,high=wall(nt+1,b)
    gate('terminal seam exact floor',W<low<high<W+1)
    gate('closed X below first right wall',wall(n0,a)[1]<X<wall(n0+1,b)[0])
    gate('closed W in last predecessor cell',wall(nt,a)[1]<W<wall(nt+1,b)[0])
    # Complete radicand endpoints, not nearest-rounded natural-index evaluation.
    for x,n in [(X,n0),(W,nt)]:
        radlo=Q(x)/(4*pu)+a/16;radhi=Q(x)/(4*pl)+b/16
        gate('whole-time natural index x='+str(x),n*n<radlo and radhi<(n+1)**2)
    gate('round-up seam mutation requires next index at top time',Q(W+1)/(4*pu)+b/16>(nt+1)**2)
    # Exact symbolic wall assignment at every n>=1, not a finite samples assertion.
    n,t=S.symbols('n t',real=True)
    rad=(4*S.pi*(n*n-t/16))/(4*S.pi)+t/16
    gate('all-n right-hand wall identity',S.simplify(rad-n*n)==0)
    # Non-vacuous interval-union topology, with closed bits as part of the data.
    def covered(rows,start,stop):
        rows=sorted(rows,key=lambda r:r[0])
        if not rows or rows[0][0]!=start or not rows[0][2]:return False
        end=rows[0][1];closed=rows[0][3]
        for left,right,lc,rc in rows[1:]:
            if end is None:return True
            if left>end or (left==end and not (closed or lc)):return False
            if right is None or right>end:end=right;closed=rc
            elif right==end:closed=closed or rc
        return end is None if stop is None else end==stop and closed
    good=[(X,W,True,True),(W,None,True,False)]
    gate('exterior-tail closed union positive control',covered(good,X,None))
    gate('both-open seam mutation rejected',not covered([(X,W,True,False),(W,None,False,False)],X,None))
    gate('one-open other-closed seam legal',covered([(X,W,True,False),(W,None,True,False)],X,None))
    gate('interior spatial gap mutation rejected',not covered([(X,W-1,True,True),(W,None,True,False)],X,None))
    gate('time endpoint omission mutation rejected',not covered([(a,b,True,False)],a,b))
    gate('time closed band positive control',covered([(a,b,True,True)],a,b))
    margin=Q(3000175332800)-Q(X,2)
    gate('unchanged PT height margin',margin==Q(350479773,2))
    print('AUDITED_TAIL_COVER t=[333/2000,3/16] x=[28274333882307,inf) y={0} N>=1499999',flush=True)
    print('CONDITIONAL_EXTERIOR_COVER t=[333/2000,3/16] x=[6000000185827,28274333882307] y={0} N=[690988,1499999]',flush=True)
    print('RH_CONTEXT PT2021 T=3000175332800 REQUIRED=6000000185827/2 MARGIN='+str(margin),flush=True)
    return {'pi':[str(pl),str(pu)],'wall':[str(low),str(high)],'W':W,'margin':str(margin)}


def probes(seed):
    # New complex computations using iv explicitly, not the producer's array helpers.
    # Frozen inverse constructed by formal ordered factorizations in a small support.
    def mul(u,v):return (u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0])
    def add(u,v):return (u[0]+v[0],u[1]+v[1])
    def exponential(z):
        e=iv.exp(z[0]);return e*iv.cos(z[1]),e*iv.sin(z[1])
    def norm(z):return iv.sqrt(z[0]**2+z[1]**2)
    results=[]
    for k in range(4):
        raw=hashlib.sha256(seed+k.to_bytes(4,'big')).digest()
        t=Q(333,2000)+Q(int.from_bytes(raw[:2],'big'),65536)*Q(21,1000)
        x=6000000185827+int.from_bytes(raw[2:4],'big');N=7+raw[4]%7;D=12
        X=val(x);sig=val(Q(1,2))+val(t)*(iv.log(iv.sqrt(1+X*X)/(4*iv.pi))/4-1/(2*(1+X*X)))
        eta=val(t)*iv.atan2(X,iv.mpf(1))/4-3*val(t)*X/(2*(1+X*X));tau=X/2+eta
        b=[iv.mpf(0)]+[iv.exp(val(t)*iv.log(n)**2/4) for n in range(1,max(N,D)+1)]
        lam=[iv.mpf(0) for _ in range(D+1)];lam[1]=iv.mpf(1)
        for j in range(2,D+1):lam[j]=-sum((lam[e]*b[j//e] for e in range(1,j) if j%e==0),iv.mpf(0))
        def power(n,flat=False):return exponential((-sig*iv.log(n),-(X/2 if flat else tau)*iv.log(n)))
        E=(iv.mpf(0),iv.mpf(0));Eflat=E;A=E
        for d in range(1,D+1):
            pd=power(d);pf=power(d,True)
            E=add(E,(lam[d]*pd[0],lam[d]*pd[1]));Eflat=add(Eflat,(lam[d]*pf[0],lam[d]*pf[1]))
        for n in range(1,N+1):
            pn=power(n);A=add(A,(b[n]*pn[0],b[n]*pn[1]))
        C={}
        for d in range(1,D+1):
            for n in range(1,N+1):C[d*n]=C.get(d*n,iv.mpf(0))+lam[d]*b[n]
        combined=(iv.mpf(0),iv.mpf(0));truncated=combined
        for m,c in sorted(C.items()):
            pm=power(m);term=(c*pm[0],c*pm[1]);combined=add(combined,term)
            if m<=N:truncated=add(truncated,term)
        product=mul(E,A);wrong=mul(Eflat,A)
        for j in [0,1]:
            residual=product[j]-combined[j];l,u=ends(residual)
            gate('same-shift full-product probe '+str(k)+' component '+str(j),l<=0<=u and u-l<Q(1,10**40))
        flatdiff=norm((wrong[0]-combined[0],wrong[1]-combined[1]))
        edgediff=norm((product[0]-truncated[0],product[1]-truncated[1]))
        gate('flat-mollifier mutation excluded '+str(k),ends(flatdiff)[0]>Q(1,10**9))
        gate('dropped-edge mutation excluded '+str(k),ends(edgediff)[0]>Q(1,10**9))
        results.append({'t':str(t),'x':x,'N':N,'flat_difference':store(flatdiff),'edge_difference':store(edgediff)})
    return results


def main():
    inputs=json.loads(Path('INPUTS.json').read_text())
    for file,key in [('AUDITED_EXTERIOR.md','exterior_sha256'),('AUDITED_TAIL.md','tail_sha256')]:
        gate('pinned '+file,hashlib.sha256(Path(file).read_bytes()).hexdigest()==inputs[key])
    for name,digest in inputs['bank605_output_sha256'].items():
        gate('bank605 frozen output provenance '+name,hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest)
    gate('negative floor tool',floor_trunc(Q(-10001,10000),3)=='-1.001')
    gate('negative ceiling tool',ceil_trunc(Q(-10001,10000),3)=='-1.000')
    gate('negative near-zero ceiling tool',ceil_trunc(Q(-1,10001),3)=='0.000')
    report={'algebra':symbolic(),'arithmetic':arithmetic(),'geometry':geometry(),
            'probes':probes(bytes.fromhex(inputs['exterior_sha256']))}
    Path('audit_results.json').write_text(json.dumps(report,indent=2)+'\n')
    for p in ['check.py','AUDIT.md','INPUTS.json','AUDITED_EXTERIOR.md','AUDITED_TAIL.md']:
        print('SOURCE_SHA256',p,hashlib.sha256(Path(p).read_bytes()).hexdigest(),flush=True)
    print('SCOPE bank613 external tail-adoption second line; finite adoption conditional on explicitly stated mass/reference premise; no new Lambda bound',flush=True)
    print('TOTAL CHECKS RUN:',checks,flush=True)
    print('RESULT: ALL PASS',flush=True)

if __name__=='__main__':main()
