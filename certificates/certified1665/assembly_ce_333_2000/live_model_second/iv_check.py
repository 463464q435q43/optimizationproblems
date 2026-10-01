#!/usr/bin/python3
"""Standalone mpmath.iv line: no primary or producer helpers imported.
Reversed arithmetic choices: raw inverse sieve, d-outer forcing from global
integer moment blocks, trapezoid integrals, full Euler polynomial expansion.
"""
import json, hashlib
from fractions import Fraction
from pathlib import Path
from mpmath import iv
iv.dps=76
Q=Fraction


def v(q):
    q=Q(q)
    return iv.mpf(q.numerator)/q.denominator

def endpoint_tuple(t):
    sg,m,e,b=t
    return Q((-1 if sg else 1)*m)*Q(2)**e

def bounds(x):
    return [endpoint_tuple(x._mpi_[0]),endpoint_tuple(x._mpi_[1])]

def save(x):return [str(t) for t in bounds(x)]
def join(x,y):return iv.mpf([x.a,y.b])
def need(name,test):
    if not test:raise AssertionError(name)
    print('IV_PASS',name,flush=True)

def ceiling(q,d):
    q=Q(q);s=10**d;n=-((-q.numerator*s)//q.denominator)
    return ('-' if n<0 else '')+str(abs(n)//s)+'.'+str(abs(n)%s).zfill(d)

def floor(q,d):
    q=Q(q);s=10**d;n=(q.numerator*s)//q.denominator
    return ('-' if n<0 else '')+str(abs(n)//s)+'.'+str(abs(n)%s).zfill(d)

def display(name,x,d=18):
    l,u=bounds(x)
    print('IV_'+name,'FLOOR'+str(d),floor(l,d),'CEIL'+str(d),ceiling(u,d),flush=True)

X=6000000185827;a=Q(333,2000);top=Q(3,16);K=1024;N=690988;T=1499999
cap=Q(500000000001,10**12)

def saddle(x):
    z=v(x)
    return (iv.log(z)-iv.log(4*iv.pi)+iv.log(1+1/(z*z))/2)/4-1/(2*(1+z*z))

cc=saddle(X);sigma=v(Q(1,2))+v(a)*cc

def raw_inverse(t,dmax):
    # Proper-factor propagation, not Neumann powers or normalized recursion.
    log=[iv.mpf(0)]+[iv.log(j) for j in range(1,dmax+1)]
    heat=[iv.mpf(0)]+[iv.exp(v(t)*log[j]**2/4) for j in range(1,dmax+1)]
    acc=[iv.mpf(0) for _ in range(dmax+1)];acc[1]=iv.mpf(1)
    lam=[iv.mpf(0) for _ in range(dmax+1)]
    lam[1]=iv.mpf(1)
    for n in range(1,dmax+1):
        if n>1:lam[n]=-acc[n]
        for m in range(2,dmax//n+1):acc[n*m]+=lam[n]*heat[m]
    return lam,log


def reference(lam,log,t,D,primecap):
    sig=v(Q(1,2))+v(t)*cc
    primes=[p for p in range(2,primecap+1) if all(p%d for d in range(2,p))]
    terms={1:iv.mpf(1)}; lower=iv.mpf(1); derivative=iv.mpf(0)
    for p in primes:
        l=iv.log(p);b=iv.exp(v(t)*l*l/4)
        q=b*iv.exp(-sig*l)
        need('factor 0<q<1 '+str(p),bounds(q)[0]>0 and bounds(q)[1]<1)
        lower*=1-q;derivative+=q*l/(1-q)
        # Raw reference then normalization after the whole product is expanded.
        for d,c in list(terms.items()):terms[p*d]=-c*b
    U=iv.mpf(0);V=iv.mpf(0)
    for d in sorted(set(terms)|set(range(1,D+1))):
        l=iv.log(d)
        z=abs((lam[d] if d<=D else 0)-terms.get(d,0))*iv.exp(-sig*l)
        U+=z;V+=z*l
    emin=lower-U;kl=derivative+(V+U*derivative)/emin
    emax=sum((abs(lam[d])*iv.exp(-sig*log[d]) for d in range(1,D+1)),iv.mpf(0))
    eprime=v(cap)*sum((abs(lam[d])*iv.exp(-sig*log[d])*log[d] for d in range(1,D+1)),iv.mpf(0))
    e=v(Q(7,1)*top/(4*X*X)) if primecap==29 else v(Q(1,10**20))
    ell=(iv.log(v(X)/(4*iv.pi))-4*v(cap)*kl)/(1+2*e)
    return {'emin':save(emin),'K':save(kl),'Emax':save(emax),'Eprime':save(eprime),'ell':save(ell)}


def coefficient_probes(case,D):
    t=Q(case['t']);lam,log=raw_inverse(t,D)
    sig=v(Q(1,2))+v(t)*cc
    for row in case['probes']:
        m=row['m'];total=iv.mpf(0)
        for d in range(1,min(m,D)+1):
            if m%d==0:
                n=m//d;ln=iv.log(n)
                total+=lam[d]*iv.exp(v(t)*ln*ln/4)
        total*=iv.exp(-sig*iv.log(m))
        l,u=bounds(total)
        need('signed coefficient integer enclosure t='+str(t)+' m='+str(m),Q(row['lo'])<=l<=u<=Q(row['hi']))
    return lam,log


def full_forcing(lam,log,cut):
    mu=[abs(lam[d])*iv.exp(-sigma*log[d]) for d in range(K+1)]
    # One global integer block partition includes every d-specific cutoff.
    cuts={1,T+1}
    for d in range(1,K+1):
        cuts.add(T//d+1)
        cuts.add(min(T,cut//d)+1)
    c=1
    while c<=T:
        c=min(T+1,max(c+1,(4097*c)//4096))
        cuts.add(c)
    grid=sorted(cuts)
    moments={0:[iv.mpf(0)]*4};running=[iv.mpf(0)]*4
    for l,end in zip(grid,grid[1:]):
        r=end-1
        z=join(iv.log(l),iv.log(r))
        # f(n) is decreasing; enclose on the full integer block, no point sample.
        fl=iv.exp(v(a)*iv.log(l)**2/4-sigma*iv.log(l))
        fr=iv.exp(v(a)*iv.log(r)**2/4-sigma*iv.log(r))
        f=join(fr,fl);pw=iv.mpf(1)
        running=list(running)
        for j in range(4):
            running[j]+=(r-l+1)*f*pw
            pw*=z
        moments[r]=running
    need('moments full integer coverage',grid[0]==1 and grid[-1]==T+1 and sum(y-x for x,y in zip(grid,grid[1:]))==T)
    ln=iv.log(T);R=iv.mpf(0)
    def part(l,r):
        if l>r:return [iv.mpf(0)]*4
        return [moments[r][j]-moments[l-1][j] for j in range(4)]
    for d in range(1,K+1):
        z=log[d];q=T//d;g=min(T,cut//d)
        need_order=q<=g
        if not need_order:raise AssertionError('cutoff order')
        p=part(1,q)
        out=(z*z*p[0]+2*z*p[1])/4
        p=part(q+1,g)
        out+=(ln*ln*p[0]-p[2])/4
        p=part(g+1,T)
        out+=((2*z/17-1)*(ln*ln*p[0]-p[2])+2*(ln*ln*p[1]-p[3])/17)/4
        R+=mu[d]*out
    need('independent d-first forcing upper <21',bounds(R)[1]<21)
    display('FULL_FORCING',R)
    print('IV_MOMENT_BLOCKS',len(grid)-1,flush=True)
    return R


def blocks(lam,log,data):
    result=[];bs=data['prefix_bins'];budget=v(Q(data['B']))
    totalU=sum((v(Q(r['hi'])) for r in bs),iv.mpf(0))
    need('independent prefix budget positive',bounds(budget-totalU)[0]>0)
    for row in data['cover']:
        L,U,x=row['L'],row['U'],row['xbase']
        if L==N:need('first spatial base exact',x==X)
        else:
            wall=4*iv.pi*(v(L)**2-v(top)/16)
            need('base is unique floor '+str(L),bounds(wall)[0]>x and bounds(wall)[1]<x+1 and x>=X)
        sig=v(Q(1,2))+v(a)*saddle(x)
        delta=sig-sigma if x!=X else iv.mpf(0)
        # Algebraically reorganized form; coefficients B-sumU positive certified.
        old=(budget-totalU)*iv.exp(-delta*iv.log(N+1))
        for r in bs:old+=v(Q(r['hi']))*iv.exp(-delta*iv.log(r['l']))
        entering=iv.mpf(0)
        for d in range(1,K+1):
            z=2*iv.log(d*U)/17-1
            l,u=bounds(z)
            w=iv.mpf([str(max(Q(1),l)),str(max(Q(1),u))])
            entering+=abs(lam[d])*iv.exp(-sig*log[d])*w
        ll=iv.log(N);rr=iv.log(U);step=(rr-ll)/257
        integ=iv.mpf(0)
        for i in range(258):
            z=ll+i*step
            h=iv.exp(v(a)*z*z/4+(1-sig)*z)
            integ+=h*(v(Q(1,2)) if i in (0,257) else 1)
        integ*=step
        bound=old+entering*integ
        # Our erfi-greedy endpoints can be arbitrarily close to 47/50.  The
        # independent quadrature must certify the same strict target, not a looser one.
        need('independent full block '+str(L),bounds(bound)[1]<Q(47,50))
        result.append({'L':L,'U':U,'bound':save(bound),'integral':save(integ)})
        display('BLOCK_'+str(L),bound)
    return result


def main():
    need('signed truncation floor',floor(Q(-10009,10000),3)=='-1.001')
    need('signed truncation ceiling',ceiling(Q(-10009,10000),3)=='-1.000')
    data=json.loads(Path('independent_certificate.json').read_text())
    for case in data['anchors']:
        la,lg=coefficient_probes(case,64)
        rr=reference(la,lg,Q(case['t']),64,29)
        for key in rr:
            p,q=rr[key],case['reference'][key]
            need('anchor reference intersection '+case['t']+' '+key,max(Q(p[0]),Q(q[0]))<=min(Q(p[1]),Q(q[1])))
    la,lg=coefficient_probes({'t':str(a),'probes':data['probes']},K)
    rr=reference(la,lg,a,K,47)
    need('reference modulus',Q(rr['emin'][0])>Q(1,4))
    need('reference log derivative',Q(rr['K'][1])<5)
    need('reference corrected phase',Q(rr['ell'][0])>17)
    need('reference modulus maximum',Q(rr['Emax'][1])<Q(41,20))
    need('reference derivative maximum',Q(rr['Eprime'][1])<Q(51,50))
    for key,val in rr.items():
        print('IV_REFERENCE47',key,'FLOOR12',floor(Q(val[0]),12),'CEIL12',ceiling(Q(val[1]),12),flush=True)
    exp17=iv.exp(17);cut=data['weight_kink']
    need('independent integer weight kink',bounds(exp17)[0]>cut and bounds(exp17)[1]<cut+1)
    R=full_forcing(la,lg,cut)
    cov=blocks(la,lg,data)
    # Full-cover gate with endpoint orientation, including last predecessor cell.
    need('independent all-block joints',cov[0]['L']==N and cov[-1]['U']==T and all(x['U']+1==y['L'] for x,y in zip(cov,cov[1:])))
    w=4*iv.pi*(v(T+1)**2-v(top)/16)
    need('independent shared rational tail seam',bounds(w)[0]>data['W'] and bounds(w)[1]<data['W']+1)
    kleft=cc*iv.log(K+1)-iv.log(K+1)**2/4
    kright=cc*iv.log(T)-iv.log(T)**2/4
    need('independent common decay minimum',bounds(kleft)[0]>34 and bounds(kright)[0]>34)
    endpoint=v(Q(47,50))*iv.exp(-34*v(top-a))+21*v(top-a)
    need('independent convex-envelope terminal',bounds(endpoint)[1]<Q(47,50))
    Path('iv_results.json').write_text(json.dumps({'ref47':rr,'forcing':save(R),'blocks':cov},indent=2)+'\n')
    print('INDEPENDENT REAL INTERVAL AUDIT COMPLETE',flush=True)

if __name__=='__main__':main()
