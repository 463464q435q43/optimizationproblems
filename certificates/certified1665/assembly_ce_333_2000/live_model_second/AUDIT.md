# FOUNDATION — external single-freeze exterior second line

## Audited version, independence and scope

This artifact audits functional_astra's `ce_single_freeze_exterior/PROOF.md`,
sha256 `764506e8a5120d92629a956517ebd2ad2373613534884f72ec34019aea6e7008`,
shipped as AUDITED_PROOF.md. It was pending at our opening bank_ref snapshot
617; none of its numerical assertions is a premise here. The only complete
mass input is BANKED memory 598, numerics_astra-s5, exactly selected in
CITATIONS.json. Source/execution code, cover, prefix ledger and transport
numbers of the producer were not read, imported, executed or copied.

We give a zero-shared-code full-domain numerical/proof second line, not
another singleton result. Our primary uses finite Neumann convolution for
the inverse, exact signed integer endpoint convolution for the entire short
prefix, a different geometric partition, an erfi antiderivative, and its own
greedy integer cover. The standalone scalar engine uses mpmath.iv (rather
than Arb), raw proper-factor inverse propagation, raw Euler expansion,
d-first global moment blocks rather than n-first quotient blocks for forcing,
and a convex trapezoidal integral rather than erfi. Its signed coefficient
probes are sensitivity/representation checks, not an independent full prefix
proof. The external primary itself, independent of the producer's two codes,
covers the full prefix and full quantified region.

Rung (a): both previously certified main-mass regimes 593 and 594 are
reproduced to their directed ten-place ceilings by the SAME full prefix
kernel. The 594/598 reference regimes are independently reconstructed.
Rung (b): the full new external code, cover, forcing enclosure and written
proof audit below, plus cross-library probes and all-block scalar rechecks.
The independent verifier chooses the rung accepted.

## Exact mathematical assertion

Write a=333/2000, b=3/16, X=6000000185827, K=1024, n=690988,
J=1499999 and H=b-a=21/1000. All logarithms are natural. Define

 c(x)=log(sqrt(1+x^2)/(4*pi))/4-1/(2*(1+x^2)),
 sigma(t,x)=1/2+t*c(x), b_t(j)=exp(t*log(j)^2/4).

The actual frozen coefficients are the EXACT inverse of b_a through K,
not integer midpoint approximations:

 lambda_1=1, lambda_d=-sum_(e|d,e<d)lambda_e*b_a(d/e).

Let C_m(t,N)=sum_(dj=m,d<=K,j<=N)lambda_d*b_t(j),
 v_m=max(1,2*log(m)/17-1), and
 P_N(t,x)=sum_(m=2)^(K*N) v_m*abs(C_m(t,N))*m^(-sigma(t,x)).

For EVERY real t in CLOSED [a,b], EVERY integer N in CLOSED [n,J], and
EVERY real x>=X in the natural cell

 [s_N(t),s_(N+1)(t)), s_q(t)=4*pi*(q^2-t/16), y=0,

this artifact certifies P_N(t,x)<47/50. Every right-hand index at an
internal RS wall is included; the terminal wall s_1500000(t) is EXCLUDED.
The closed rectangle [a,b] x [X,28274333882307] is contained, because the
right integer is strictly below s_1500000(b) and its index is J at both
time endpoints. The first cell is truncated at X. Monotonicity of the
index argument in x,t fills the rectangle; no index samples replace it.

The same frozen mollifier E(w)=sum lambda_d*d^(-w), evaluated at the EXACT
heat-shifted w=s+t*alpha(s)/2, s=(1+i*x)/2,
alpha(s)=1/(2*s)+1/(s-1)+Log(s/(2*pi))/2, satisfies throughout

 |E|>1/4, |E_w/E|<5, |E|<=Emax<41/20, |E_x|<=EprimeMax<51/50,
 4*(Theta-arg E)'/(1+2*eta')>17.

Thus P_N bounds the complete resultant majorant at the actual scale and
at every scale>=17, for every real resultant phase. This is finite-model
numerics and phase control only: no new H_t remainder, zero-exclusion
conclusion, RH verification or Lambda bound is inferred. The domain and
coefficients are compatible with banked family605 with zero perturbation;
any true-function composition remains explicit and separately owned.

The inequality is RH-free. For eventual assembly the unchanged initialization
is PT2021 T=3000175332800, required X/2=6000000185827/2, exact margin
350479773/2. Tail613 begins at the stated rational seam; its true-H theorem
is contextual only, not a premise for our finite-model bound.

## 1. Weight containment against the one consumed corner

Memory598 bounds its COMPLETE weighted mass by B=891101027766/10^12.
Its lambda, t, x and n are exactly ours at (a,X,n). Its weight uses the
exact Euler-29 proxy ell29 given in its archived WRITEUP, not merely a
reported lower decimal. We recompute that proxy with the full reference
support and eta_cap=7*b/(4*X^2), and prove 0<ell29<17. Since
ell -> max(1,2*log(m)/ell-1) is nonincreasing for ell>0, our weights are
termwise smaller. Therefore P_n(a,X)<=B, including ALL m>n.
A lower bound on ell29 alone would not prove this containment.

The prefix coefficient for 2<=m<=K is exactly zero at time a. Uniqueness
of a triangular Dirichlet inverse proves this, independently of any interval
width. Our Neumann form is sum_{r>=0}(-g)^{*r}, g=b_a-delta; every index in
g is >=2, so r>floor(log_2 K) contributes nothing on [1,K]. It agrees
algebraically with the raw proper-divisor propagation used by the IV line.
We never retain the zero identity at later times: the n=2 derivative is
strictly positive, and all such regrowth is paid below.

## 2. Prefix mass constraint as a positive Laplace gain

Let A_m=v_m*abs(C_m(a,n))*m^(-sigma(a,X)). Their total is <=B.
For K<m<=n we have v_m=1, checked by log(n)<17. The exact integer
convolution bounds the full signed prefix, with bin totals A(I_j)<=U_j,
I_j=[l_j,r_j], consecutive integer bins. Set r=n+1 and delta>=0.

For m>=r, exp(-delta*log(m))<=exp(-delta*log(r)). Consequently

 sum A_m*m^(-delta)
 <= B*r^(-delta)+sum_j A(I_j)*(l_j^(-delta)-r^(-delta))
 <= B*r^(-delta)+sum_j U_j*(l_j^(-delta)-r^(-delta)).          (1)

Every gain multiplier is NONNEGATIVE. This is the reason upper, rather
than lower, prefix masses can be substituted. The tail by itself is NOT
bounded by B-sum U_j; the checker verifies sum U_j<B only to allow the
algebraic rewriting (B-sum U_j)r^-delta+sum U_j*l_j^-delta.
No false separate tail inequality is consumed.

Take delta=a*(c(x)-c(X)). Direct differentiation gives
c'(x)=x/(4*(1+x^2))+x/(1+x^2)^2>0, so (1) transports to all x>=X.
For a complete integer block L<=N<=U, use x_L=X at L=n, otherwise
x_L=floor(s_L(b)). Exact interval checks prove the floor is unique and
x_L>=X. Every natural x in the intended block is >=x_L since s_L(t)
decreases in t. N need not be the natural index at the auxiliary time a:
(1) is an algebraic polynomial inequality for arbitrary fixed N,x.

The new terms j>n obey the exact polynomial identity
 E(w)*A_N(w)-E(w)*A_n(w)=E(w)*sum_(n<j<=N)b_a(j)j^(-w).
Triangle inequality on these new terms only, together with v_(dj)<=v_(dU),
gives

 P_N(a,x)<=old_prefix_bound(x_L)
       +sum_(d<=K)|lambda_d|d^(-sigma_L)*v_(dU)
                       *integral_n^U exp(a*log(z)^2/4)*z^(-sigma_L) dz. (2)

Here sigma_L=1/2+a*c(x_L). The endpoint inequality
(a/2)*log(U)<sigma_L proves the integrand decreasing for 1<=z<=U.
Each entering integer is charged by its entire preceding unit interval.
There is no discarded cancellation or per-pair fall credit.

After z=exp(v), complete the square in (a/4)v^2+(1-sigma_L)v.
An exact primitive is sqrt(pi)/(2*sqrt(a/4))*exp(-(1-sigma_L)^2/a)
 times erfi(sqrt(a/4)*v+(1-sigma_L)/(2*sqrt(a/4))).
Arb encloses this expression outward, including any subtraction cancellation.
The separate line uses 257 log panels and the theorem that the density's
second derivative is positive; therefore its composite trapezoid is an
UPPER integral bound, not numerical quadrature used without an error theorem.

The primary generates a new greedy integer cover using binary search for
U. Each accepted block is checked against the stronger internal reserve
939/1000, so the independent quadrature can still certify the stated
47/50. Binary search is only an economy: the whole-block gate and exact
integer union, not an assumed optimizer property, establish the certificate.
No producer block count or endpoint is imported.

## 3. Removing common decay without erasing small-index regrowth

Fix any N<=J,x>=X,h=t-a>=0. For each pair dj=m set
 z_dj=lambda_d*b_a(j)*m^(-sigma(a,x)),
 L_m=log(min(m,N)), k_m=c(x)*log(m)-L_m^2/4,
 r_dj=(L_m^2-log(j)^2)/4.
Then r_dj>=0 and

 C_m(a+h,N)*m^(-sigma(a+h,x))
     =exp(-k_m*h)*sum_(dj=m)z_dj*exp(-r_dj*h).               (3)

All k_m>=0 because c(X)>log(J)/4, and k_m>34 for m>K:
replace N by J and c(x) by c(X); on [K+1,J] the resulting quadratic
in log(m) is concave so its minimum is at an endpoint; beyond J it is
increasing. Both endpoint evaluations exceed34 on both arithmetic lines.

For any finite complex z_j and r_j>=0,
 abs(sum z_j*exp(-r_j*h))<=abs(sum z_j)+h*sum abs(z_j)*r_j,
by subtraction, triangle inequality, and 1-exp(-r*h)<=r*h.
At m<=K the initial sum vanishes, but the forcing term remains. At m>K
retain the exp(-34h) on the initial coefficient; drop only nonincreasing
factors on the forcing. Summing (3) yields

 P_N(a+h,x)<=exp(-34h)*P_N(a,x)+h*R_N(x).                   (4)

This proof is valid at all coefficient zeros and sign changes. No absolute
value derivative, sampled monotonicity, or per-coefficient sign assumption
is needed. An equivalent upper-Dini-derivative integrating factor also
leads to (4), but is not required for the implementation.

Increasing N to J only adds nonnegative pairs and increases log(min(m,N));
increasing x decreases all their positive magnitudes. Hence R_N(x)<=R_J(X)
for every N,x under discussion. Both codes enclose the COMPLETE R_J(X)<21.
One must not replace J by the smaller n when claiming this dominance.

Now (2) gives P_N(a,x)<47/50; (4) gives the scalar envelope
 (47/50)*exp(-34h)+21h on CLOSED h in [0,H]. Its second derivative is
positive. Its h=0 value is47/50, and the exact terminal interval value is
strictly below47/50. Convexity bounds every intermediate h. Strictness at
h=0 is inherited from (2), so the stated strict mass bound holds on both
time endpoints as well as the entire interior.

## 4. Full finite forcing, two representations

Let f_j=b_a(j)*j^(-sigma(a,X)), mu_d=lambda_d*d^(-sigma(a,X)),
p_k(q)=sum_(d<=q)|mu_d|log(d)^k, k=0,1,2. Let C17=floor(exp(17)),
computed and uniquely enclosed on both arithmetic lines. For fixed j set
f=min(K,floor(J/j)), g=min(K,floor(C17/j)), u=log(j), L=log(J).
C17>J implies f<=g. Exact splitting of d at f and g gives the inner sum

 (p_2(f)+2u*p_1(f))/4
 +(L^2-u^2)/4 * [p_0(g)-p_0(f)
             +(2u/17-1)*(p_0(K)-p_0(g))
             +(2/17)*(p_1(K)-p_1(g))].                    (5)

Multiply by f_j and sum j=1..J. Primary partitions j exactly where either
integer quotient changes, with additional ratio1025/1024 subdivisions.
It encloses every log(j), rate, and decreasing f_j on the WHOLE integer
block and multiplies by its exact number of terms. These are interval
blocks, not samples. The full integer union is gated.

The IV line instead forms T_k(q)=sum_(j<=q)f_j*log(j)^k for k=0..3,
using its own global integer partition of ratio4097/4096 containing every
needed cutoff. For each d it splits j at q=floor(J/d),g=floor(C17/d).
Below q the relative rate is (log(d)^2+2log(d)log(j))/4; above q it is
(L^2-log(j)^2)/4. The weight is1 below g and affine in log(j) above g.
Multiplication gives a polynomial of degree<=3 evaluated against these
complete moment enclosures. No primary moment or quotient ledger is read.
Different conservatisms need not produce intersecting aggregate enclosures;
each must independently prove the required upper cap21.

## 5. Reference, phase and half-line transfer

For p<=47 freeze beta_p=b_a(p), and E0(w)=product(1-beta_p*p^-w).
At (a,X), expand the ENTIRE reference support, including d>K. Let
 q_p=beta_p*p^-sigma, B0=product(1-q_p),
 L0=sum q_p*log(p)/(1-q_p),
 U=sum_d|lambda_d-lambda0_d|d^-sigma,
 V=sum_d|lambda_d-lambda0_d|d^-sigma*log(d).
Triangle inequality and the exact logarithmic derivative identity give

 Emin=B0-U, K1=L0+(V+U*L0)/(B0-U).

The primary normalizes each prime before expanding; IV expands raw
reference coefficients and then normalizes each complete product.
All q_p are strictly between0 and1. Both full-support sums prove Emin>1/4,
K1<5, Emax<41/20 and EprimeMax<51/50. Lambda and beta are constants, so as
sigma increases B0 increases while U,V,L0 decrease; Emin increases and K1
decreases. c(X)>0 and c'>0 give sigma(t,x)>=sigma(a,X) on the entire domain.
These directions are analytic and preserve all closed endpoints.

Bank609 supplies exactly the required half-line derivative estimates for
t in [a,b], x>=10^11: |w'|<=500000000001/10^12, 0<=eta'<=1/10^20,
4*Theta'>=log(x/(4*pi)). This independent artifact does not re-claim that
banked theorem. Its hypotheses for the full frozen reference are discharged
above. Therefore, everywhere x>=X,

 ell_actual>= [log(X/(4*pi))-4*vcap*K1(a,X)]/(1+2/10^20)>17.

This is the shifted denominator, not4*Theta' alone. The mollifier and finite
sum use the same shifted w, so the COMPLETE coefficients are the C_m above.
Every high-edge term is retained. References are bounds for E, not different
actual mollifiers. Family605 uses another reference but precisely this
inverse, so its coefficient-distance premise is zero if later composed.

## 6. Arithmetic, mutation checks and reproducibility

The primary rounds each Arb input OUTWARD to multiples of2^-90, with sign
specialized multiplication of interval endpoints. Integer coefficient sums
and absolute values use Python's unbounded integers at scale2^-180; no
floating arithmetic or overflow assumption enters. Both main masses and all
prefix bins are obtained from EVERY relevant pair (d,j), d*j<=n, d<=K.
The separate raw-divisor code checks hash-selected signed coefficients,
mandatory ends and bin boundaries against these exact endpoint intervals.
These probes validate representation only; full-domain scope comes from
complete prefix enumeration and analytic domination of its complement.

All decimal floors/ceilings come from exact rational interval endpoints,
with negative-direction self-tests. No nearest Arb printed string is a
gate or a directed endpoint. Clocks are labeled diagnostic and do not enter
any mathematical acceptance condition. Sources are local and self-contained.

Mutation controls detect missing last/interior cells, removed cover blocks,
incorrect persistence of inverse cancellation, uncharged new pairs, and a
one-sided scale-direction misuse. They are counterexamples to weakened
hypotheses, not allegations against the pinned correct manuscript. The full
checks also cannot pass if the decisive numeric bounds are violated.

Run `/usr/bin/python3 check.py` in a fresh source-only copy. It regenerates
all arithmetic, independent_certificate.json and iv_results.json, invokes
only its independent scalar child, and prints RESULT: ALL PASS only after
all gates. The consumed bank598 mass is explicit; no full D*n corner
re-enumeration is falsely advertised. No upstream or other workspace files
are read at runtime. Credit functional_astra for this frozen-prefix device,
wildcard_astra for the common-decay idea, and Kornaus for the collision/
resultant architecture; no unrefereed theorem or numerical leg is consumed.
