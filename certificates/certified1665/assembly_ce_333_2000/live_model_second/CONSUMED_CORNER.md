# FOUNDATION — independent RECIP-1024 combined corner, with charges

## Quantifier audit and non-duplication

This is a **single-point** certificate at

    t=333/2000, x=X=6000000185827, N=690988, y=0, K=1024.

No non-singleton t-interval, spatial interval, or range of N is covered by
the coefficient-mass computation. The accompanying L8 theorem covers the
full exterior error charges, but does not enlarge the domain of this mass
certificate. The two axes must not be conflated. The exact RS index at the
point is checked by the closed-band geometry in the included L8 checker.

The earlier memory-line-587 failure was for an unchanged Euler-29 per-pair
majorant at a different point. It is not a negative about this device. This
new bound combines the complete signed reciprocal convolution before taking
absolute values, including all products above N. Memory line 588 already
supplies a remote-tail/stall second line; that theorem is not re-claimed.
V1-H-213 supplies the site's historical geometry, not numerical inputs.

The producer's RECIP-1024 module was absent from its claims directory at the
inspected snapshot. This is a **prebuilt independent singleton line**, not a
claim of auditing an absent or future full-band package. SNAPSHOT.json pins
the producer RECIP64 writeups that were read to specify the family. No
producer source file was opened for this development, imported, copied, or
executed. Different parameter choices or freezing conventions must be
compared explicitly before this artifact is called their second line.

No RH hypothesis is used. This does not assert a Lambda improvement, an
exterior leg, a separator, or a completed collision-exclusion package.

## Exact finite model

All logarithms are natural. Put s=(1+i*x)/2 and

    alpha(s)=1/(2*s)+1/(s-1)+Log(s/(2*pi))/2,
    w=s+t*alpha(s)/2=sigma+i*tau,
    sigma=1/2+t*(log(sqrt(1+x^2)/(4*pi))/4-1/(2*(1+x^2))),
    tau=x/2+(t/4)*atan(x)-(3*t/2)*x/(1+x^2),
    b(n)=exp(t*log(n)^2/4).

Define the exact real reciprocal coefficients

    lambda(1)=1,
    lambda(d)=-sum_{e|d,e<d}lambda(e)*b(d/e), 2<=d<=K,
    E(w)=sum_{d<=K}lambda(d)*d^(-w), S(w)=sum_{n<=N}b(n)*n^(-w).

Both sums use the SAME heat-shifted w. For 1<=m<=K*N define

    c(m)=m^(-sigma)*sum_{d|m,d<=K,m/d<=N}lambda(d)*b(m/d).

Then E*S=sum c(m)*exp(-i*tau*log(m)). In particular c(1)=1 and c(m)=0
for 2<=m<=K by the defining reciprocal recurrence. The engines do NOT
force the small coefficients to zero; their interval residues are retained
adversely, making the numerical bound independent of a cancellation shortcut.

Let ell0 be the exact positive reference-derived quantity defined below.
The finite majorants are

    U0=sum_{m=2}^{K*N}|c(m)|,
    M=sum_{m=2}^{K*N}max(1,2*log(m)/ell0-1)*|c(m)|.

The entire product is evaluated, not just m<=N. M is enclosed by

    FLOOR12 0.891045392348, CEIL12 0.891101027766.

The independent second engine, with a different accumulator precision and
block partition, gives the wider but independently decisive enclosure

    FLOOR12 0.890965072958, CEIL12 0.891187848333.

The new edge weights matter. U0 is enclosed by
FLOOR12 0.881698591879 / CEIL12 0.881698591885, so setting every weight to
one after enlarging the support would silently lose at least
0.009346800463 FLOOR12 of the specified majorant. No claim is made that
this is the optimal phase bound or that a better reference cannot improve it.

## Phase/reference control with no imaginary-part sampling

Let P={2,3,5,7,11,13,17,19,23,29} and

    E0(w)=product_{p in P}(1-b(p)*p^(-w)),
    q_p=b(p)*p^(-sigma), B=product(1-q_p),
    L=sum q_p*log(p)/(1-q_p).

Expand E0 exactly in all squarefree products of the primes. Subtract its
coefficients from those of E over the **union** of their supports, including
the reference terms above K. Let

    U=sum_d |lambda(d)-lambda0(d)|*d^(-sigma),
    V=sum_d |lambda(d)-lambda0(d)|*d^(-sigma)*log(d),
    Lstar=L+(V+U*L)/(B-U).

Every 0<q_p<1 and B>U is interval-certified. For every imaginary part at
this fixed real part, triangle inequality gives |E|>=B-U. The exact identity

    E_w/E-E0_w/E0=(R_w-(E0_w/E0)*R)/(E0+R), R=E-E0,

gives |E_w/E|<=Lstar. No Euler-product identity for E is assumed.
The bound is |E|>=0.249258957244 FLOOR12.

Let Theta=arg Mt((1+i*x)/2), with the Polymath Mt. Define

    vcap=500000000001/1000000000000,
    eta_cap=7*(3/16)/(4*X^2),
    Q=log(X/(4*pi))-4*vcap*Lstar,
    ell0=Q/(1+2*eta_cap).

Both Q and ell0 are bounded below by FLOOR12 16.323213748562.

Here is the analytic sign proof behind this choice. Write alpha=A+iBalpha,
alpha'=C+iD at s=(1+i*x)/2. Direct differentiation gives

    A=log(sqrt(1+x^2)/(4*pi))/2-1/(1+x^2),
    Balpha=atan(x)/2-3*x/(1+x^2),
    C=(7*x^2-5)/(1+x^2)^2,
    D=-x*(x^2+5)/(1+x^2)^2,
    sigma_x=-t*D/4, tau_x=1/2+t*C/4,
    4*Theta'=2*A+t*(A*C-Balpha*D).

At our point, A>0, C>0, Balpha>3/4 and -D>1/(4*x). The last inequality
is equivalent to 3*x^4+18*x^2-1>0. Also 2*A>log(x/(4*pi))-2/x^2.
Thus 3*t*x>32 proves 4*Theta'>log(x/(4*pi)). Each sufficient inequality
is gated in exact or outward arithmetic; this is not a nearest-rounded
comparison of nearly equal phase terms.

The identities also give

    0<tau_x-1/2<=eta_cap,
    |sigma_x|<=(3/16)*(1/(4*X)+1/X^3), |w_x|<vcap.

If theta=Theta-arg(E), then 4*theta'>=Q. The correct heat-shifted
scale is ell_actual=2*theta'/tau_x, hence ell_actual>=ell0. It is NOT
simply 4*theta' unless the imaginary heat shift is discarded. The corrected
scale lies below log(K*N), which is precisely why high-edge weights remain.

This reference estimate does NOT verify the convenient Q>=20 hypothesis in
the generic L8 corollary. The corner therefore substitutes its own Q into
the charge formula rather than applying that corollary without its premise.

## Resultant and true-function charge

With Shat=E*S and Lhat=sum c(m)*log(m)*exp(-i*tau*log(m)), put

    G=exp(i*theta)*(Shat-Lhat/ell_actual)
       +exp(-i*theta)*conj(Lhat)/ell_actual.

The m=1 term has modulus one. Every other term is bounded by
|c(m)|*(|1-log(m)/ell_actual|+log(m)/ell_actual), which equals the
specified max weight and is nonincreasing in ell_actual. Therefore
|G|>=1-M, for every phase consistent with the model (indeed arbitrary unit
coefficient phases obey the same triangle bound).

The included L8_PROOF.md supplies genuine Polymath remainder bounds Ev,Ed
for the exact fixed-index model, with the entire Cauchy circle, reflection,
and neighboring-index charge accounted for. The corresponding checker is
rerun; no submitted log or unbanked external claim supplies those constants.
The proof at a hypothetical double zero gives

    |G|<=Emax*Ev/2+(2/Q)*(Eprime*Ev+Emax*Ed+Asigma),
    Emax=sum |lambda(d)|*d^(-sigma),
    Eprime=vcap*sum |lambda(d)|*d^(-sigma)*log(d),
    Asigma=2*sigmax_cap*log(K*N)*U0_upper.

No factor of Emax is dropped. The new mollifier bounds are
Emax<=2.046776838028 CEIL12 and Eprime<=1.019116801204 CEIL12.
The total charge is <=0.000029392484070474 CEIL18. Thus

    M+charge <=0.891130420250 CEIL12 <9/10,
    1-M-charge >=0.108869579750 FLOOR12.

This discharges the frozen-point budget with the true saddle and true-function
errors. It does not constitute transport to any neighboring time or x, let
alone the required exterior band. The preregistered singleton gate passes;
the full-band prediction was NOT tested in this session. The amendment says
this explicitly and retains the original record of the prediction.

## Independent arithmetic architecture and reproducibility

Run `/usr/bin/python3 verify.py` in a clean copy. Both C engines are compiled
locally from source to extensionless temporary filenames, then removed. No
precompiled object, shared library, archive, or binary data is shipped.

First engine (`kernel.c`):
- Arb at 144-bit initializes every normalized a_n=b(n)*n^(-sigma) and every
  normalized reciprocal mu_d=lambda(d)*d^(-sigma).
- Endpoints are rounded by ARF_FLOOR/CEIL to exact multiples of 2^-58.
- A divisor-gather inverse is followed by d-outer product accumulation in
  coefficient slabs of width 262139. All coefficient endpoints and their
  absolute values are exact signed 128-bit integers at scale 2^-116.
- The triangle envelope (sum_d max|mu_d endpoints|)*(sum_n a_n upper)
  is strictly below 2^126, checked BEFORE any signed products or aggregate
  coefficients are formed. Input-size guards make even that multiplication
  safe. Thus signed overflow is not an unproved C assumption.
- Every product pair is counted and every coefficient index is partitioned
  exactly. The omitted-tail routine yields zero because R=K*N.

Second engine (`rebuild.c` plus mpmath.iv initialization):
- Independently expands sigma using log(x), log(1+x^-2), and exact rationals;
  derives raw lambda with its own divisor recurrence; normalizes afterward.
- Recomputes ALL a_n and mu_d in mpmath.iv, checking the first engine's
  fixed-point intervals. It separately rounds its OWN enclosures to 2^-50.
- Uses n-outer product accumulation, all four endpoint products (rather than
  the first engine's sign-specialized multiplication), and coefficient slabs
  of width 1048573. Signed arithmetic is independently capacity-checked.
- It has no Arb dependency and shares no helper, arithmetic initialization,
  multiplication routine, or accumulator code with kernel.c.
- It recomputes B,U,V,Lstar, Q and ell0 in mpmath.iv, using raw reference
  coefficients and the algebraically alternative (B*L+V)/(B-U).

Each engine bounds weights on a coefficient slab [a,b] by its monotone
endpoint values max(1,2*log(a)/ell0-1) and max(1,2*log(b)/ell0-1).
Nonnegative coefficient masses then give a rigorous complete M enclosure;
this is a spatial *summation* bound, not a transport assumption.

Additional checks: literal small convolutions in two distinct time regimes;
exact floor/ceil negative-direction tests; all reciprocal initializer rows;
all transcendental input rows; signed coefficients at endpoints and at
hash-seeded, pre-value-selected divisor-product points; exact coverage,
pair count and block-total recombination; producer-document snapshot hashes;
source manifest and import whitelist. Each printed decimal is produced from
exact rational endpoints, not Arb's nearest-rounded printer.

Rung requested: (b), for the novel reciprocal/combined fixed-point machinery.
This is separate implementation and a separate arithmetic library from the
producer's draft Arb paths, backed by another independently coded integer
line and whole-input-table re-evaluation. The verifier decides the rung; a
successful point certificate is not advertised as a full-band second line.

Credit: Kornaus for collision-exclusion/mollify-first architecture; the
functional seat's RECIP64 reference-product device and the operator's
combined-edge extension motivate the experiment. Neither unrefereed code
nor a third-party certificate is a mathematical input or included file.
