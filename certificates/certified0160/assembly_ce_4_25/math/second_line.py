#!/usr/bin/python3
"""Separate real-interval/Machin and interval-subtraction composition line."""
from fractions import Fraction as Q
from pathlib import Path
import json, math, copy
from mpmath import iv
iv.dps=90
COUNT=0
out={'exact':{},'scalars':{},'leaves':[],'mutations':[]}
def check(b,name):
 global COUNT
 COUNT+=1
 if not bool(b): raise AssertionError(name)
def qi(x):
 x=Q(x);return iv.mpf(x.numerator)/x.denominator
def bounds(x):
 def q(t):
  sign,mant,exp,bc=t
  return Q((-1 if sign else 1)*int(mant))*Q(2)**int(exp)
 return q(x._mpi_[0]),q(x._mpi_[1])
def lo(x):return bounds(x)[0]
def hi(x):return bounds(x)[1]
def lower(x):return lo(x)>0
def text(q,d,upper=False):
 q=Q(q);v=-((-q.numerator*10**d)//q.denominator) if upper else q.numerator*10**d//q.denominator
 return ('-' if v<0 else '')+str(abs(v)//10**d)+'.'+str(abs(v)%10**d).zfill(d)
def save(k,x,d=18):
 l,u=bounds(x);out['scalars'][k]={'lo':str(l),'hi':str(u),'floor':text(l,d),'ceil':text(u,d,True),'places':d}
 return out['scalars'][k]
def hull(a,b):return iv.mpf([qi(a).a,qi(b).b])
for q,l,u in [(Q(-1,3),'-0.33334','-0.33333'),(Q(-1,10**8),'-0.00001','0.00000'),(Q(1,7),'0.14285','0.14286')]:
 check(text(q,5)==l and text(q,5,True)==u,'signed digit law')
def atan_enclosure(n):
 x=Q(1,n);s=Q(0)
 for k in range(160):s+=(-1)**k*x**(2*k+1)/(2*k+1)
 e=x**321/321
 return hull(s,s+e)  # even number of terms: next term positive
pi=16*atan_enclosure(5)-4*atan_enclosure(239)
check(lower(pi-3) and lower(4-pi),'pi enclosure')
a,b=Q(4,25),Q(3,16);X=6000000185827;C=690988;H=2299999;J=2300000;W=66476100549959
A=qi(a);B=qi(b)
def cc(x):return (iv.log(1+x*x)/2-iv.log(4*pi))/4-1/(2*(1+x*x))
c0=cc(qi(X));lc=iv.log(qi(C))
raw=[]
for s in Path('frozen/bank774_bins.txt').read_text().splitlines():raw.append(list(map(int,s.split())))
star=raw[0];check(star[:5]==[-1,0,0,0,0],'synthetic header')
vs=hull(Q(star[5],2**100),Q(star[6],2**100));check(lower(vs),'positive denominator')
bins=[(r[1],hull(Q(r[5],2**100),Q(r[6],2**100))) for r in raw[1:]]
check(len(bins)==224,'complete bins')
partition=json.loads(Path('frozen/bank774_geometry.json').read_text())
accepted=[json.loads(Path('frozen/'+f).read_text()) for f in ['bank774_primary.json','bank774_second.json']]
for L,U in partition:
 x=qi(X) if L==C else 4*pi*(qi(L)**2-B/16)
 s=qi(0) if L==C else A*(cc(x)-c0)
 check(lo(s)>=0,'inward')
 m=iv.sqrt(1+sum(v*(1-iv.exp(-2*s*iv.log(qi(r)))) for r,v in bins)/vs)/10
 h=iv.log(qi(U))-lc;aa=A/4;bb=qi(Q(1,2))-A*c0-s;D=2*aa*lc+bb
 check(lower(h) and lower(D),'positive complete series')
 z=D*h+aa*h*h;check(hi(z)<1,'complete series tail guard')
 coeff=[qi(1),D]
 for k in range(2,101):coeff.append((D*coeff[-1]+2*aa*coeff[-2])/k)
 part=sum(coeff[k]*h**(k+1)/(k+1) for k in range(101))
 rem=h*qi(Q(3,math.factorial(51)))
 integral=iv.exp(aa*lc*lc+bb*lc)*(part+hull(0,hi(rem)))
 retained=m-integral;slope=-qi(Q(1,2))+A*(iv.log(qi(U))/2-cc(x));support=4*cc(x)-iv.log(qi(U))
 check(hi(slope)<0 and lower(support),'whole-leaf monotonicity and heat support')
 check(lo(retained)>Q(1,100),'entire leaf admitted')
 row={'L':L,'U':U}
 for key,val in [('x_left',x),('s',s),('old_norm_lower_expression',m),('entry_integral_upper',integral),('retained_lower_expression',retained),('entry_log_slope',slope),('heat_support',support)]:
  l,u=bounds(val);row[key]={'lo':str(l),'hi':str(u),'FLOOR12':text(l,12),'CEIL12':text(u,12,True)}
  if key!='heat_support':
   for prod in accepted:
    old=next(q for q in prod['leaves'] if (q['L'],q['U'])==(L,U))[key]
    check(max(l,Q(old['lo']))<=min(u,Q(old['hi'])),'accepted leaf enclosure')
    check(row[key]['FLOOR12']==old['FLOOR12'] and row[key]['CEIL12']==old['CEIL12'],'all directed cells agree')
 out['leaves'].append(row)
worst=min(out['leaves'],key=lambda r:Q(r['retained_lower_expression']['lo']))
check(all(Q(worst['retained_lower_expression']['hi'])<Q(r['retained_lower_expression']['lo']) for r in out['leaves'] if r is not worst),'unique sufficient minimum')
out['minimum']={'L':worst['L'],'U':worst['U'],**worst['retained_lower_expression']}
# Adjacent-square geometry, not wall-minus-abscissa formula.
for name,x,n in [('head',X,C),('seam',W,H)]:
 q=qi(x)/(4*pi)
 check(lo(q+A/16)>n*n and hi(q+B/16)<(n+1)**2,'whole-band natural cell '+name)
 save(name+'_left',4*pi*(q+A/16-n*n))
 save(name+'_right',4*pi*((n+1)**2-q-B/16))
check(hi(4*pi*(qi(J)**2-B/16)-W)<1,'floor seam')
# Same functions in two previously accepted regimes.
save('anchor677_seam_right',4*pi*(qi(2200000)**2-B/16)-60821233773498)
check(lo(qi(60821233773498)/(4*pi)+qi(Q(33,200))/16)>2199999**2,'anchor677 predecessor')
check(hi(qi(60821233773498)/(4*pi)+B/16)<2200000**2,'anchor677 terminal')
g1=qi(X)-4*pi*C*C;g2=4*pi*(qi(C+1)**2-qi(Q(1809,10000))/16)-(X+1)
check(text(lo(g1),4)=='5377392.8789' and text(lo(g2),4)=='11989041.1415','V1 source geometry')
save('V1_site_gap1',g1,4);save('V1_site_gap2',g2,4)
# Exact independent expansion of the real Hermitian perturbations.
p=Q(1,800000);q=Q(1600001,40000000000);r=Q(1,100)
surplus=12*r*r-30*p*r-q*r-2*200*p-p*q
check(surplus==Q(22375198391999,32000000000000000)>Q(1,2000),'real lift')
check(24*r-30*p-q>0,'increasing lift')
aj,bj,res=Q(179,180),Q(19,135),Q(19999,200000)
jet=res*res/(aj*aj+bj*bj);check(jet>Q(9,1000),'tail quadratic')
# Exact interval operations: None is +infinity only here.
def nonempty(i):
 l,u,cl,cu=i;return u is None or l<u or (l==u and cl and cu)
def meet(i,j):
 l=max(i[0],j[0]);cl=(i[2] if l==i[0] else True) and (j[2] if l==j[0] else True)
 if i[1] is None:u=j[1]
 elif j[1] is None:u=i[1]
 else:u=min(i[1],j[1])
 cu=False if u is None else ((i[3] if u==i[1] else True) and (j[3] if u==j[1] else True))
 k=(l,u,cl,cu);return k if nonempty(k) else None
def subtract(i,j):
 k=meet(i,j)
 if k is None:return [i]
 pieces=[(i[0],k[0],i[2],not k[2])]
 if k[1] is not None:pieces.append((k[1],i[1],not k[3],i[3]))
 return [x for x in pieces if nonempty(x)]
def complement(target,ints):
 left=[target]
 for j in ints:left=[z for i in left for z in subtract(i,j)]
 return left
def decode(v,axis):
 return (Q(v[axis][0]),None if v[axis][1]=='inf' else Q(v[axis][1]),*v[axis+'_closed'])
def contains(i,x):
 return (x>i[0] or x==i[0] and i[2]) and (i[1] is None or x<i[1] or x==i[1] and i[3])
def full_union(boxes):
 ends=sorted({a,b}|{Q(s) for box in boxes for s in box['t']})
 times=[ends[0]-1,ends[-1]+1]+ends+[(v+w)/2 for v,w in zip(ends,ends[1:])]
 bad=[]
 for t in times:
  active=[decode(box,'x') for box in boxes if contains(decode(box,'t'),t)]
  if a<=t<=b:
   if complement((Q(0),None,True,False),active):bad.append(('missing',str(t)))
   if any(complement(i,[(Q(0),None,True,False)]) for i in active):bad.append(('excess',str(t)))
  elif active:bad.append(('excess_time',str(t)))
 return not bad,bad
contract=json.loads(Path('CONTRACTS.json').read_text());boxes=contract['emitted_boxes']
check(full_union(boxes)[0],'exact two-dimensional complement')
check(complement((Q(C),Q(H),True,True),[(Q(l),Q(u),True,True) for l,u in partition])==[],'complete index complement')
check(subtract((Q(0),Q(1),True,True),(Q(0),Q(1),False,False))==[(Q(0),Q(0),True,True),(Q(1),Q(1),True,True)],'singleton subtraction selftest')
mut=[]
z=copy.deepcopy(boxes);z[1]['x_closed'][1]=False;z[2]['x_closed'][0]=False;mut.append(('isolated_seam',z))
z=copy.deepcopy(boxes);[box['t_closed'].__setitem__(0,False) for box in z];mut.append(('initial_time',z))
z=copy.deepcopy(boxes);z.pop();mut.append(('infinite_ray',z))
z=copy.deepcopy(boxes);z[1]['t'][0]='33/200';mut.append(('early_finite_band',z))
z=copy.deepcopy(boxes);z[1]['x'][1]=str(W-1);z[2]['x'][0]=str(W+1);mut.append(('integer_adjacency',z))
for name,z in mut:check(not full_union(z)[0],name);out['mutations'].append(name)
for name,value in [('surplus',surplus),('tail_jet',jet),('a',a),('b',b),('X',X),('W',W),('C',C),('H',H),('J',J),('RH_required',Q(X,2)),('RH_margin',Q(3000175332800)-Q(X,2)),('stall_r',a/2),('stall_exponent',128/(a/2)),('improvement',Q(33,200)-a),('missing_components',0),('excess_components',0)]:out['exact'][name]=str(value)
check(Q(out['exact']['RH_margin'])==Q(350479773,2)>0,'PT2021')
check(Q(21,125)+Q(39,2000)==b and 0<a<b<=Q(1,2),'anchor and time')
check(Q(186,1000)+Q(16733,100000)**2/2==Q(19999966445,10**11),'distinct published row arithmetic')
check(3000175332800-Q(5000000194858,2)==500175235371,'distinct RH anchor')
out['checks']=COUNT;out['full_proof_not_sampled']=True;out['external_record_audit']=False
Path('SECOND_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('SECOND_LINE_CHECKS',COUNT)
print('SECOND_MINIMUM',worst['L'],worst['U'],worst['retained_lower_expression']['FLOOR12'],worst['retained_lower_expression']['CEIL12'])
print('SECOND_LINE: ALL PASS')
