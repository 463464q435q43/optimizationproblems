# FOUNDATION — CE_SINGLE_FREEZE_PREFIX_N_TRANSPORT

## 1. Exact statement and quantifier audit

Let

    a=333/2000, b=3/16, H=b-a=21/1000,
    X=6000000185827, D=1024, n0=690988, nT=1499999,
    b_t(n)=exp(t log(n)^2/4),
    c(x)=log(sqrt(1+x^2)/(4*pi))/4-1/(2*(1+x^2)),
    sigma(t,x)=1/2+t*c(x).

Freeze ONE real vector for the ENTIRE domain:

    lambda_1=1,
    lambda_d=-sum_{e|d,e<d}lambda_e*b_a(d/e), 2<=d<=D.

No rounding of lambda is defined or assumed. Arithmetic balls enclose these
exact analytic coefficients. In particular lambda and the reference below
are independent of both x and t. Let

    C_m(t,N)=sum_{d*n=m, d<=D, n<=N}lambda_d*b_t(n),
    v_m=max(1,2*log(m)/17-1),
    P_N(t,x)=sum_{m=2}^{D*N}v_m*|C_m(t,N)|*m^(-sigma(t,x)).

**For every real t in CLOSED [a,b], every integer n0<=N<=nT,
and every real x>=X in the left-closed/right-open natural RS cell**

    s_N(t)<=x<s_(N+1)(t),  s_N(t)=4*pi*(N^2-t/16),

at y=0, this certificate proves P_N(t,x)<47/50<19/20. It includes
EVERY new-index term and every natural left wall. It is not a sampled-grid
statement. The first cell is truncated at X; the last upper endpoint
s_1500000(t) is excluded. The exact closed rational rectangle

    t in [a,b],  X<=x<=28274333882307, y=0

is contained in this domain. The integer at its right is the floor of
s_1500000(b); its value is derived live and is strictly below that wall.
No claim is made about N>=1500000 here. The banked tail line 604 overlaps
this endpoint, but this package does not consume or extend that tail.

Take the exact shifted saddle w=s+t*alpha(s)/2 with s=(1+i*x)/2 and
alpha(s)=1/(2*s)+1/(s-1)+log(s/(2*pi))/2. Both E=sum lambda_d*d^(-w)
and the Polymath finite sum use THIS SAME w, including its imaginary heat
shift. Throughout the stated domain the certificate also proves

    |E|>1/4, |E_w/E|<5,
    |E|<=Emax<41/20, |E_x|<=EprimeMax<51/50,
    ell_actual=4*(Theta-arg E)'/(1+2*eta')>17.

Theta and eta are exactly as in banked CE_X_TRANSPORT, memory line 609.
Consequently the complete coefficient resultant majorant using the actual
scale, or any scale at least 17, is bounded by P_N. Every resultant phase
is allowed. Hence its finite amplitude-free resultant has modulus >3/50.
No true-H_t error charge, multiple-zero exclusion, or Lambda conclusion
is asserted. This is RH-free. An eventual collision assembly must consume
an explicitly compatible banked L7/charge module and the other legs.

## 2. Citations, scope, ownership and lineage

CITATIONS.json is the exact selected statements from the 610-entry opening
bank_ref snapshot, with original line/session/timestamp and line hashes.
Numerical input B below consumes ONLY line 598, numerics_astra-s5,
CE_RECIP1024_INDEPENDENT_CORNER; not a third-party calculation. Its model,
full support and exact inverse agree with section 1 at (a,X,n0). The
reference/phase half-line theorem is line 609, functional_astra-s5. We
recompute the reference scalars rather than consume rounded outputs.
Lines 593 and 594 are live arithmetic anchor regimes. Line 610 is the
existing frozen-slab first-cell certificate being extended to changing N,
not an all-N premise. Its separate frozen vectors are NOT our one vector.

The initial fixed-N one-freeze idea was withdrawn without measurement after
an ownership check found wildcard_astra's pending annihilated-head theorem.
That work is credited as the time-factorization inspiration, together with
its banked PRODUCT-COMMON-DECAY line 601. No unbanked claim is consumed; the
needed time inequality is proved here with a GLOBAL larger-N forcing cap.
The new device is the two-axis proof: combine a short signed-prefix
Laplace estimate with positive new-index integrals, and use one universal
forcing cap for the whole range. This is distinct from a fixed-N
one-freeze theorem, a new singleton mass, or a prefix/complementary-tail
recalculation of the corner. The previous failed window/Y3 route is not
used. In particular no signed coefficient monotonicity is assumed.

Credit Kornaus for the amplitude-free-resultant architecture, the operator
for the collision route and stage-1 target, and wildcard_astra for retaining
common time decay on the annihilated-head complement. No upstream source,
output, or unrefereed statement is included, read by a checker, or cited as
a leg. No publication action is taken.

## 3. The only complete-mass input: weight containment

Line 598 supplies

    B=891101027766/10^12

as an upper bound at (a,X,n0) for its COMPLETE combined majorant with weight
max(1,2 log(m)/ell29-1). Its ell29 is the exact proxy defined in its writeup,
not the actual phase scale or merely the reported lower decimal.
We reconstruct that proxy using the frozen Euler-29 reference and exactly
its eta_cap=7*(3/16)/(4*X^2); the live comparison proves 0<ell29<17.
Thus v_m is no larger term by term, and P_n0(a,X)<=B.
One cannot infer ell29<17 from a lower bound on ell29; this package does not
make that mistake. No complete convolution is repeated and none is omitted
from the consumed banked mass.

For 2<=m<=D, C_m(a,N)=0 exactly for every N>=n0>D, by the defining inverse
recurrence. Those coefficients may regrow for t>a; the forcing below
charges them. It would be wrong to continue setting them to zero at later
times. The numerical prefix keeps their interval residues for validation,
but the analytic identity licenses excluding their initial mass.

## 4. Spatial transport from a short signed prefix

Let A_m=v_m*|C_m(a,n0)|*m^(-sigma(a,X)); their total is at most B.
For the prefix D<m<=n0, v_m=1, certified live. Partition this prefix into
integer bins [l_j,r_j], with A-bin totals B_j and certified B_j<=U_j.
The producer uses boundaries obtained by integer multiplication by 6/5;
the second line uses 17/16 instead. Set r=n0+1.
For any x>=X put delta=a*(c(x)-c(X))>=0. Monotonicity of m^(-delta) gives

    P_n0(a,x)
    <= B*r^(-delta)+sum_j B_j*(l_j^(-delta)-r^(-delta))
    <= (B-sum_j U_j)*r^(-delta)+sum_j U_j*l_j^(-delta).       (1)

This subtract-and-add form is important: the tail does NOT have an upper
bound B-sum U_j by itself. Its upper bound is B-sum B_j; the replacement
by U_j is made only after the nonnegative gain factor is exposed.
Every l_j<r, so that factor is nonnegative. The checker also proves
sum U_j<B, which makes the rewritten expression transparently positive.
Both independent lines compute all signed prefix coefficients by different
recurrences and accumulation orders. No combined coefficient beyond n0 is
recomputed; all of it is covered through the consumed B.

Now for N>=n0, the difference between the two polynomials is exactly

    E(w)*sum_(n0<n<=N)b_a(n)*n^(-w).

A per-pair triangle bound is safe for this increment; it does NOT replace
old signed coefficients by their triangle mass. For a closed integer block
L<=N<=U, choose x_L=X if L=n0, and otherwise

    x_L=floor(4*pi*(L^2-b/16)).

The floor is certified unique, is at least X, and lies STRICTLY below the
lower natural wall for every t in [a,b]. Therefore each intended x>=x_L.
This deliberately transports an algebraic polynomial at time a to x_L;
N need not be the NATURAL index there at time a. All inequalities are for
arbitrary finite polynomials and require no such index identification.
For sigma_L=1/2+a*c(x_L), let f(u)=exp(a log(u)^2/4)*u^(-sigma_L).
The checker proves (a/2)*log(U)<sigma_L. Thus f is decreasing on [1,U],
and

    sum_(n0<n<=N)f(n)<=integral_(n0)^U f(u)du.

Since v_(dn)<=v_(dU),

    P_N(a,x)
    <= [the right side of (1) at x_L]
       + (sum_(d<=D)|lambda_d|d^(-sigma_L)*v_(dU))
                         *integral_(n0)^U f(u)du.           (2)

Equation (2) is uniform over every integer N in the block and every
x>=x_L. Positive new terms are all counted, even if they would cancel.
There is no fall/jump induction that silently drops entering terms.

For evaluation put u=exp(v). The integral density is
exp(a*v^2/4+(1-sigma_L)*v), whose second derivative divided by itself is
(a*v/2+1-sigma_L)^2+a/2>0. Composite trapezoids therefore bound the integral
UPWARD. This is not empirical quadrature: convexity proves the direction.
The producer uses 32 equal log-panels; the independent line uses 67.
An adaptive exact-integer bisection of [n0,nT] accepts a block only if its
whole bound (2) is <47/50. The generated certificate has 13 accepted
blocks, checked for exact consecutive-index coverage. This is much
stronger than checking 13 individual N values.

## 5. One time forcing for ALL indices

Fix any x>=X, N in [n0,nT], and write h=t-a>=0. Put

    z_dn=lambda_d*b_a(n)*(dn)^(-sigma(a,x)),
    L_m=log(min(m,N)),
    k_m=c(x)*log(m)-L_m^2/4,
    r_dn=(L_(dn)^2-log(n)^2)/4.

For each product m the exact identity is

    C_m(a+h,N)*m^(-sigma(a+h,x))
       =exp(-k_m*h)*sum_(dn=m)z_dn*exp(-r_dn*h).

The checker proves c(X)>log(nT)/4. Hence every k_m,r_dn is nonnegative.
For m>D a GLOBAL lower bound k_m>34 follows without enumerating products:

* min(m,N)<=min(m,nT) and c(x)>=c(X);
* on D+1<=m<=nT the function c(X)*log(m)-log(m)^2/4 is concave in log(m),
  so its minimum lies at an endpoint;
* at m>=nT the conservative expression c(X)*log(m)-log(nT)^2/4 increases;
* both endpoint expressions exceed 34, checked outward.

Subtract the h=0 sum inside the exact identity and use
0<=1-exp(-r*h)<=r*h. Then

    |A_m(h)|<=exp(-k_m*h)*|A_m(0)|
                     +h*sum_(dn=m)|z_dn|*r_dn.

Only the initial term vanishes for m<=D. Summing gives

    P_N(a+h,x)<=exp(-34*h)*P_N(a,x)+h*R_N(x).                (3)

A separate integrating-factor proof starts from A_m'=-k_m*A_m-Z_m.
At A_m=0 the upper right Dini derivative of |A_m| is bounded by |Z_m|;
else it is at most -k_m|A_m|+|Z_m|. Integrating and bounding the forcing
by its initial absolute pair magnitudes gives exactly (3), including
all sign changes. No coefficientwise monotonicity is invoked.

The crucial new all-N domination is

    R_N(x)<=R_nT(X)
      =sum_(d<=D,n<=nT) v_(dn)*|lambda_d|*b_a(n)*(dn)^(-sigma(a,X))
                       *(log(min(d*n,nT))^2-log(n)^2)/4.    (4)

Indeed increasing N only adds nonnegative pairs and increases the relative
rate of existing pairs; increasing x decreases their positive amplitudes.
The checker proves R_nT(X)<21 in TWO complete scalar lines.
Using a forcing cap only at n0 would not prove (4); the upper index nT is
used deliberately throughout both computations.

Combining (2)--(4) yields, for all h in CLOSED [0,H],

    P_N(a+h,x)<(47/50)*exp(-34*h)+21*h.

The right side is convex. At h=0 it equals 47/50; at h=H its live upper
bound is strictly below 47/50. The strict block inequalities supply
strictness even at h=0. Therefore P_N(t,x)<47/50 throughout. Convexity
is asserted only for this scalar envelope, NOT for the true majorant.

## 6. Two complete computations of (4)

Primary: direct Arb prefix moments T_j(q)=sum_(n<=q)f_n*log(n)^j,
j=0,1,2,3, with f_n=b_a(n)*n^(-sigma(a,X)), at the required integer
thresholds. For each d let z=log(d), L=log(nT), q=floor(nT/d),
g=min(nT,floor(exp(17))/d). The relative-rate polynomial is
(z^2+2z log(n))/4 below q and (L^2-log(n)^2)/4 above q. The weight is 1
below g and (2z/17-1)+2log(n)/17 above g. Their product has degree at most
three. Splitting at both q and g gives the exact finite forcing sum.
The integer kink floor(exp(17)) is separately certified.

Second line: reverse the sums. Build P_j(q)=sum_(d<=q)|mu_d|log(d)^j,
j=0,1,2, with mu_d=lambda_d*d^(-sigma(a,X)). At each integer n put
f=min(D,floor(nT/n)), g=min(D,floor(exp(17)/n)), u=log(n), L=log(nT).
Since exp(17)>nT, g>=f. The inner d sum, before multiplication by f_n, is

    (P_2(f)+2u*P_1(f))/4
    +(L^2-u^2)/4 * (P_0(g)-P_0(f))
    +(L^2-u^2)/4 * ((2u/17-1)*(P_0(D)-P_0(g))
                                      +(2/17)*(P_1(D)-P_1(g))).

Integer segments are split where either floor changes. Within each segment
use modest integer blocks; enclose all log(n) and all f_n by endpoint
intervals. This gives a full mpmath.iv enclosure for the sum, independent
of the primary moments, and certifies the same bound <21. The driver also
checks enclosure containment. Nothing is omitted at either cutoff.

## 7. Reference and physical scale on the whole rectangle

Freeze E0(w)=product_(p<=47)(1-b_a(p)*p^(-w)). At (a,X) compute
q_p=b_a(p)*p^(-sigma), B0=product(1-q_p), L0=sum q_p log(p)/(1-q_p),
and the full-support difference sums U,V between E and E0. Then

    Emin=B0-U,
    K=L0+(V+U*L0)/(B0-U),
    Q=log(x/(4*pi))-4*cs*K,
    ell0=Q/(1+2e), cs=500000000001/10^12, e=1/10^20.

The union of the ENTIRE reference and mollifier supports is used, including
reference terms above D. Direct Arb and independent normalized iv product
expansion prove Emin>1/4, K<5, ell0>17 and the Emax/EprimeMax gates of
section 1. For fixed coefficients all q_p,U,V,L0 decrease as sigma
increases, B0 increases, so Emin increases and K decreases. Since c(X)>0,
sigma(t,x)>=sigma(a,X) for all t>=a and x>=X.

The exact saddle half-line estimates are consumed from memory line 609:
|w'|<=cs, 0<=eta'<=e and 4*Theta'>=log(x/(4*pi)), uniformly on our
closed time band and x>=10^11. Its hypotheses are satisfied at (a,X) and,
by the preceding sigma argument, at (t,X) for EVERY t in the band. The
phase scale lower bound thus holds everywhere x>=X; it is independent of
N. No claim that the actual oscillatory phase is monotone is needed.
Every physical weighted majorant is <=P_N since its scale exceeds 17.

## 8. Arithmetic, second-line rung, and safe replay

primary.py uses raw forward-sieve inverse coefficients, Arb at 192 bits,
and d-outer prefix scatter. prefix_second.c uses Arb at 224 bits, a
normalized proper-divisor inverse, and factors each product m to gather
all divisors; the prefix bins differ. second.py imports no primary helper
and uses mpmath.iv at 70 decimal precision for a full reversed forcing
calculation and every accepted spatial block with a different quadrature
partition. The driver checks imports by AST and logs source sha256 values.
No machine float enters a mathematical gate; clocks, if present, are only
observations. Signed floor/ceiling helpers have both negative-direction
self-tests. Ball endpoints are exact dyadic fractions, not nearest printer
strings used as one-sided bounds.

Known-anchor rung (a): the PRIMARY prefix core reproduces the main masses
in memory lines 593 (t=17/100) and 594 (t=21/125) with their exact directed
ten-place literals, live from source. New prefix transport, all-N forcing,
and time envelope receive separate mathematical derivations and the full
independent line above: rung (b) requested. The verifier chooses the rung.
The result is not inferred from agreement of two floating approximations.

check.py reruns the anchors, primary, and complete second line. The C source
is compiled in place to an extensionless temporary executable and always
removed. No external file reads or supplied numerical log trust occur.
CITATIONS.json authenticates banked premises for adversarial review, not
as a replacement for them. A fresh-copy full run is mandatory. Exact
coverage and the rational seam are live gates. The frozen vector is
constant across every time and spatial joint, avoiding any derivative
ambiguity about switching coefficients.
