# FOUNDATION — stage-one Euler-13 true-H collision-exclusion tail

## 1. Statement, novelty, and exact quantifier audit

Set a=333/2000, b=3/16, h=1499999, J=1500000, D=30030 and

    x_n(t)=4*pi*(n^2-t/16),
    X1=floor(4*pi*(J^2-b/16))=28274333882307.

**Theorem.** For EVERY real t in the CLOSED interval [a,b], EVERY integer
N>=h, and EVERY real x in the LEFT-CLOSED/RIGHT-OPEN interval
[x_N(t),x_(N+1)(t)),

    (H_t(x), dH_t(x)/dx) != (0,0).

Thus every REAL zero in those cells is simple. This is not a claim that
all complex zeros in that region are real. In particular the conclusion
holds on the CLOSED rectangle [a,b] x [X1,infinity), y=0, and by evenness
on its negative reflection. Every time endpoint and every RS wall is
included, with a wall belonging to its natural RIGHT-HAND index.

At each point the banked complete-coefficient majorant satisfies M<43/50,
and the actual L7 error budget is bounded by

    C <= Cstar = 751998000616933/130000000000000000000
                < 3/500000,
    1-M-C > 69997/500000.

The fractions, directed decimal presentations, and X1 are derived by the
checker. M and C refer to the SAME mollifier and exact shifted exponent,
not to independently chosen models.

**Novelty.** Verified-memory line 604 is a majorant and mollifier certificate
only: it expressly leaves H5, the true-H errors and collision exclusion open.
Line 607 supplies the general L7 theorem and H5, but its numeric corollary is
conditional on the chosen mollifier. Line 606 independently audits that
version. Line 605 supplies transition-inclusive raw errors and a family
charge theorem but no M bound or exclusion. This package closes their
analytic interface to prove an actual infinite H_t exclusion region. It
neither reclaims their individual proofs nor runs another coefficient sweep.

**Snapshot.** Exactly 608 bank entries were available at session start.
`frozen/memory.json` freezes the full cited statements, identifiers and
hashes. All consumption below names versions as of that snapshot. The
old domain negative, line 608, is not restated as a current gap: line 604
explicitly repairs the omitted lower-time tail region from its old input
line 595. No statement about absence of successors is made.

## 2. Cited modules and their consumption boundaries

| Memory line | Version | Exactly what is consumed |
|---|---|---|
| 604 | dynamics_astra-s5, L11-GT2 | all t in [a,b], all N>=h, whole half-open cells: M<43/50, nonvanishing/modulus/derivative bounds, Q0 and ell0 proxies; complete expansion including m>N |
| 605 | numerics_astra-s6, L8_DAMPING_FAMILY | ONLY the raw bounds v,d for the natural index, frozen on the Cauchy disk, on t in [a,b], x>=6000000185827; every transition and endpoint |
| 607 | prover_astra-s5, ce_l7_general_resultant_v1 | the general all-finite-support L7 implication and uniform H5; not its older denominator-16 numeric corollary |
| 606 | numerics_astra-s6, EXTERNAL_L7_SECOND_LINE | external second line of the exact manuscript version of 607 |
| 591 | wildcard_astra-s4, exact-phase interface | consistency of w, eta and fixed-index differentiation; derivative bounds are already in 604 |

The source writeups were read before adoption. Manuscript hashes identify
versions in `frozen/provenance.json`. No upstream manuscript, operator
numerical output, or live workspace is read by either verifier script.

Line 604 includes two independently implemented complete numerical lines
(prefix-bin/antiderivative and absolute-convolution/trapezoid). Line 605
also includes separately coded Arb and interval lines. This package does
not assert that its small sampled replay replaces either full calculation.
A final record's external adoption audit remains a distinct responsibility.

## 3. Model identity and discharge of the phase premises

Use the normalization and branches of line 607. On the real axis

    s=(1+i*x)/2, alpha(s)=1/(2s)+1/(s-1)+Log(s/(2*pi))/2,
    w=s+t*alpha(s)/2=sigma+i*tau, tau=x/2+eta,
    b_n(t)=exp(t*log(n)^2/4),
    E(w)=product_(p in {2,3,5,7,11,13})(1-b_p(t)*p^(-w)),
    lambda_d(t)=mu(d)*product_(p|d)b_p(t), d|D,
    A_N=sum_(n<=N)b_n(t)*n^(-w),
    E*A_N=sum_(m<=DN)c_m*m^(-w),
    c_m=sum_(d|D,d|m,m/d<=N)lambda_d(t)*b_(m/d)(t).

The coefficient at m=1 is exactly one. Every product m is present,
INCLUDING m>N. The signed coefficient is combined before absolute values.
The Euler coefficients depend on t but do not depend on x. L7 holds with
t,N and lambda fixed during x differentiation, so no time-derivative of
lambda is needed, and no freezing across different times is imposed.

Put c=500000000001/10^12, e=1/10^24, q_p=b_p*p^(-sigma),
K=sum_p q_p*log(p)/(1-q_p), and

    Q0=log(x/(4*pi))-4*c*K, ell0=Q0/(1+2*e).

The M in line 604 is EXACTLY

    sum_(m>=2) max(1,2*log(m)/ell0-1)*abs(c_m)*m^(-sigma).

Its certified interfaces are

    |E|>12/25, |E|<9/5, |E'|<3/5, |E_w/E|<=K<87/100,
    |w'|<c, 0<eta'<e, Q0>26, ell0>26.

Here E_w is the derivative with respect to the Dirichlet argument w at
fixed t; it is called E_s in the cited convention. The notation does not
mean the derivative with respect to the separate coordinate s.

All our cells have x>Y=26000000000000. To see this without a rounded pi,
use pi>3 and

    x>=x_h(b)>12*(h^2-b/16)>Y.

In particular x>=5100, x>=6000000185827, and a*(3*x-2)>6. H5 in line 607
gives 4*Theta'>log(x/(4*pi)) throughout this domain. For a local branch
of arg E let theta=Theta-arg E and k=theta'. Then

    4*k >= log(x/(4*pi))-4*abs(w')*abs(E_w/E) >= Q0 > 26.

Also tau'=1/2+eta'>0. The TRUE corrected resultant scale is

    ell=2*k/tau'=4*k/(1+2*eta') >= Q0/(1+2*e)=ell0.

Thus P0=26 and the producer's variable ell0 are admissible L7 lower
bounds. They are not assumed equal to the oscillatory true phase, and
we do not replace ell by the flat-saddle scale 4*k. Since the majorant
weights decrease when ell increases, the consumed M is conservative.

## 4. A monotone drift envelope on the entire half-line

The complete log moment in L7 is

    B1=sum_(m>=2)abs(c_m)*m^(-sigma)*log(m).

All weights in M are at least one, so its banked M<43/50<1 implies
B1<=log(D*N). This step is not circular: the M theorem was proved without
any error charge or zero-exclusion premise. The natural index satisfies
N<=sqrt(x), since pi>3, t<=1/2 and x/12+1/32<x. Consequently

    B1 <= L(x):=log(D)+log(x)/2.

The exact real-exponent derivative is

    sigma'=t*x/(4*(1+x^2))+t*x/(1+x^2)^2
           <=b*(1/(4*x)+1/x^3).

Hence the amplitude-derivative term is at most

    2*abs(sigma')*B1 <= F(x)
    F(x)=2*b*(1/(4*x)+1/x^3)*L(x).

As L(x)>1/2 on x>=Y,

    F'(x)=2*b*((1/2-L(x))/(4*x^2)+(1/2-3*L(x))/x^4)<0.

An Arb endpoint evaluation proves F(Y)<1/10^13. A separate interval
calculation and exact rational derivative identity verify the same
inequality. One endpoint and a global derivative sign prove the whole
half-line; sampled points are not used for that universal inference.

## 5. Raw-error adoption and true-H exclusion

Line 605, restricted to this tail, gives

    v=655217372417/10^18,
    d=37300347933869/10^18,
    |R_N(x)|<=v, |R_N'(x)|<=d,
    R_N=H_t/B_t-f_N.

The index is the natural one at the CENTER and is kept fixed on its
Cauchy disk of radius 4/log(x/(4*pi)). The theorem includes neighboring-
index terms and lower-half-disk reflection; we do not use the smaller
same-cell derivative bound at a wall. No derivative of N(x) is taken.

Take E0=9/5, E1=3/5, P0=26 and the drift bound of section 4 in L7. A
multiple real zero would force

    1-M <= C <= E0*v/2+2*(E1*v+E0*d+1/10^13)/P0 = Cstar.

The exact rational calculation gives Cstar as in section 1, strictly
less than 3/500000. Since M<43/50,

    M+C < 43/50+3/500000 = 430003/500000 < 1.

This contradicts the necessary multiple-zero inequality. This proves
all multiplicities at least two are excluded, at every point of every
stipulated cell. The stronger middle/infinite M caps of line 604 can
also be paired with the same charge, but are not needed for this theorem.

## 6. Exact rectangle and transition joints

The checker derives X1 by directed evaluation of x_J(b), and proves

    x_h(a)<X1<x_J(b),
    x_n'(t)=-pi/4<0.

For t in [a,b], x_h(t)<=x_h(a)<X1, so every x>=X1 has natural N>=h.
The included predecessor cell h=J-1 supplies the short strip BEFORE cell
J. This is why rounding DOWN does not leave a gap. The claimed rectangle
is closed at X1, whereas the underlying cells are right-open; their union
covers all real x>=X1 because the next cell includes each shared wall.
Time endpoints are closed in ALL input modules.

The output's single honest H_t coverage line is

    COVER module=tail t=[333/2000,3/16] x=[28274333882307,inf]

It is deliberately not a full record coverage union. At y=0 the theorem
covers all integer N>=1499999 with these natural-index joints. It gives
nothing for the finite exterior down to the stationary separator, nor a
zero-free off-axis strip. Evenness of H_t gives the negative reflection,
with the derivative changing sign and simultaneous vanishing unchanged.

## 7. Honesty block, RH height, credit, and verification ladder

No new Lambda upper bound is asserted. This theorem is RH-free. A future
collision-exclusion assembly would still consume PT2021 at height
6000000185827/2, with margin 350479773/2 below 3000175332800, as well as
the anchor V1-H-213. Neither initial RH nor the anchor is needed to prove
this tail theorem. Numerical separator second lines and the finite
exterior are not supplied by this package. The remote REAL-SIMPLE tail
needed for the stall theorem is already separately banked (lines 588/590);
this practical tail proves no multiple REAL zeros, not off-axis reality.

Credit Daniel Martin Kornaus, PR #180, for the collision-exclusion and
mollify-first resultant architecture. This proof consumes only our banked
re-proofs. No third-party source or output is shipped or cited as a leg.

FOUNDATION rung requested: (a), proportional to a composition of banked,
already independently checked universal machinery. The SAME charge
arithmetic reproduces the accepted line-606 older-corollary ceiling and
the line-605 family-charge ceiling in different parameter regimes. A
second code path uses real-coordinate L7 normalizations, mpmath.iv and
an exact alternating-series pi enclosure to verify the new charge, drift,
and rectangle. Source boundaries are hashed. These arithmetic tests are
not replacements for the analytic proofs or banked universal hypotheses.
The verifier chooses the accepted rung. Numerics_astra may independently
audit this final adoption without re-running the expensive tail sums.

Run `/usr/bin/python3 verify.py` from this directory or a clean copy.
It is pure Python; its only child is `[sys.executable, 'second_line.py']`.
There are no outside reads, compilers, other binaries or hidden state.
FROZEN.sha256 and the source pin all consumed outputs. The verifier checks
all frozen block joints and maxima and performs hash-selected Python
replays of the banked tail bound; it does not pretend those samples prove
all the underlying coefficients. The full producer computation is banked.

All displayed decimals are derived from exact rationals or outward ball
endpoints and labeled FLOOR/CEIL by self-tested truncation helpers. Both
negative rounding directions are tested first. Rational values are exact.
Clean-copy logs and mechanical pre-flight receipts ship with the bundle.
