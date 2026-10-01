# FOUNDATION — ASSEMBLY_CE_333_2000_v1

## Statement and status

This source-only collision-exclusion assembly proves

    Lambda < 333/2000.

The exact board value is lambda_upper=333/2000. The inequality itself is
strict. Its sole finite-height RH input is the published PT2021 theorem,
T_PT=3000175332800, consumed at X/2=6000000185827/2. The exact available
margin is 350479773/2. Thus the conclusion is unconditional, not conditional
on any unproved extension of RH. No publishing action is authorized here.

Let a=333/2000, A=3/16, X=6000000185827, W=28274333882307,
n0=690988, nT=1499999. The adopted anchor is V1-H-213, Lambda<=A,
independently audited in V1-H-220. All load-bearing accepted sources are
identified in frozen/memory.json by verified-memory line, session and hash.
New code and proofs are executed LIVE where they are not banked facts.
Passing the arithmetic harness is not itself an independent theorem verdict.

Pre-registration: PREREG.md, with LIVE_PREREG.md recording the decision to
rerun independent source-only lines before any candidate evaluation. The
score, strict improvement and directed decimal representations are derived
from exact fractions in verify_assembly.py. No measured score is input to it.

## A. Criterion: closed-band collision exclusion and the remote stall tail

The accepted positive-stall theorem is memory590, with external proof and
arithmetic audit memory588. For every real r in (0,1/2], every complex zero
of H_t with |Re z|>=4*pi*exp(128/r)+1 is real and simple uniformly for ALL
t in CLOSED [r,1/2]. This is a theorem about all complex zeros, not merely
simple zeros on the real axis. The cutoff-free analytic two-chirality model
and its complete Rouche phase-cell covering are reproduced in
frozen/remote_tail.txt and frozen/remote_tail_second.txt. The exact error
reserve epsilon<1/1024 is re-gated here; no sample supplies universality.

If Lambda>0, take r=Lambda/2. The single tail radius is valid for all t in
[Lambda/2,1/2], including a left neighbourhood of Lambda. If every real
zero of H_Lambda were simple, finitely many disjoint symmetric disks in
a compact rectangle, plus that uniform tail, would keep all zeros real
for some t<Lambda, a contradiction. Thus H_Lambda has a finite multiple
real zero. The accepted proof covers also Lambda=1/2 and uses no RH.

For the present band a<=Lambda<=A one could alternatively use the fixed
r=a/2=333/4000 and radius 4*pi*exp(512000/333)+1. This explicit remote
radius is used ONLY for compactness at a hypothetical stall. It is not our
practical exterior wall W. No need to enumerate or bridge to that radius
is hidden in the argument.

Now assume for contradiction Lambda>=a. The banked anchor yields
0<a<=Lambda<=A. Sections C, D and T below exclude every multiple real
zero at every t in [a,A] and all real x. This contradicts the positive-stall
theorem at t=Lambda. Hence Lambda<a. If Lambda<=0 the same conclusion
is immediate, so a nonnegativity theorem is not needed for this implication.

This reasoning only needs real-axis collision exclusion on the practical
tail, NOT reality of every complex zero there. It deliberately uses the
stall component of590, not its stronger sufficient composition statement
that assumed a real-simple complex-zero tail at the practical wall.

## B. RH and separator height

Use the stationary separator s(t)=X, continuous and positive on [0,A].
The identity H_0(z)=xi(1/2+i*z/2)/8 identifies the initial requirement as
RH to height X/2, no more. PT2021 arXiv:2004.09765 proves RH to T_PT.
Exact arithmetic establishes X/2<=T_PT with margin350479773/2.

The anchor itself uses the same site and no greater height. No later
time statement or model transport consumes a larger RH height. No initial
simplicity of H_0 is assumed. The contextual constant N=690988 belongs to
the separator's boundary evaluation, not to every interior point.

## C. Hermite normal form, boundary and interior

Memory590's generic compact-separator theorem is independently audited
in617. For any jointly analytic real-type backward-heat solution F_t=-F_zz,
a continuous positive separator with a nonzero full rectangular boundary
and real initial interior zeros propagates reality on [0,A] and simplicity
on (0,A]. The all-m parabolic normal form is the real-rooted Hermite
polynomial forward and its imaginary rotation backward. Finite clusters,
a compact boundary collar and Rouche justify continuation for all times,
without differentiability of the separator. These are banked universal
lemmas, not inferred from finite-degree controls in this script.

Boundary596, externally audited numerically over the full continuum by616,
proves |H_t(X+i*y)/B_t(X+i*y)|>7/800 for every t in CLOSED [0,A] and y
in CLOSED [0,1]. Real-type symmetry and evenness cover both full vertical
segments |y|<=1 at +/-X. There is no empirical radius or sampled monotonicity.
For the padded rectangle |Im z|<=2, the published strip exclusion handles
1<|y|<=2 and both horizontal edges. Their squared clearance is >=3.
The closed low strip and open high strip share no missing y-endpoint.

Memory599 instantiates this boundary and PT2021;617 independently audits
that analytic instantiation. Memory616 supplies the separate full-domain
numerical qualification explicitly required by596/599. Consequently ALL
zeros with |Re z|<=X are real on [0,A] and simple on (0,A]. Since a>0,
this gives the CLOSED collision rectangle [a,A] x [0,X]. The boundary x=X
is included because it has no zeros. The record prints no simplicity
COVER box starting at time zero.

## D. Finite exterior: exact inverse, full products, live conversion

Accepted memory618 supplies the full finite-model premise on

    t in CLOSED [a,A], N integer in [690988,1499999],
    x>=X in [4*pi*(N^2-t/16),4*pi*((N+1)^2-t/16)), y=0.

One exact real inverse lambda of b_a(n)=exp(a*log(n)^2/4) on d<=1024 is
frozen over that entire domain. Both the finite sum and mollifier use the
same exact heat-shifted w=s+t*alpha(s)/2, s=(1+i*x)/2. Its combined product
has ALL C_m=sum_(d*n=m)lambda_d*b_t(n), including m>N and their non-unit
weights. Its complete mass at fixed scale17 is <47/50, |E|>1/4,
|E_w/E|<5, |E|<41/20, |E_x|<51/50 and the actual corrected scale >17.

The new true-H conversion is proved LIVE in exterior/THEOREM.md and its
checker. It does not cite this session's pending adoption claim. The exact
inverse is the zero-perturbation member of bank605's universal anchor family
at tau=a. Different Euler references are only proof witnesses for the same
E. Line605's transition-inclusive family charge is at most
529085205861/50000000000000000. General L7 from607, externally re-proved
in606, then gives the contradiction

    1-M > 3/50 > C,
    1-M-C >2999470914794139/50000000000000000>2999/50000.

The charge denominator Q=4*(Theta-arg E)' and the corrected mass scale
Q/(1+2*eta') are NOT equated. No denominator-at-least-20 shortcut occurs.
Both mollifier multipliers and the real-exponent derivative are retained.

The same live manuscript supplies a separate real-gauge proof. With
u=H_t/|M_t|, real projection of the fixed-index remainder derivative gives
|u'-V'|<=d without an artificial phase-speed charge. The resulting bound
has coefficients229/200 and41/170, and a finite-support log-moment drift.
Its direct charge is strictly smaller than the banked family cap. This
also proves true-H exclusion under exactly618's premises.

### Full independent LIVE numerical and analytic lines

All mathematical code in live_model_second/ and live_adoption_second/ was
independently authored by numerics_astra from the pinned manuscripts, not
our checking helpers. It is copied with exact source digests and attribution
in LIVE_PROVENANCE.json. Its authors' current claim statuses are NOT used
as premises. Instead both complete checkers are executed LIVE, from source,
inside the record's confinement, and must pass before the record can pass.

The numerical external line uses an exact-integer prefix convolution,
an independently generated integer cover, analytic erfi integrals and a
separate interval forcing/reference line. It consumes only accepted598's
complete corner and609's phase transport; their exact versions are pinned.
It re-proves the full model region, not just probes or a frozen ledger.
Known anchor593/594 regimes reproduce. This is extra verification of618,
not circular acceptance of a pending external claim.

The independently authored adoption line supplies a complete conditional
proof of both this finite conversion and bank613's tail adoption. The
finite premise is discharged by accepted618 and the live model check.
Its proof and exact arithmetic, not the pending claim's PASS log, are used.
It also checks the two normalizations, complete coefficient identity,
phase scales and domain endpoints. This is the explicit external record-use
adoption audit; no pending fact is relabelled as banked. Source copies are
never modified to force a numerical gate.

## E. Transitions and joint semantics

At a real center use N=floor(sqrt(x/(4*pi)+t/16)), then keep that index
and the chosen coefficients fixed for analytic differentiation. At the
natural wall x=4*pi*(n^2-t/16), the index is n, the right-hand cell.
Bank605's fixed-index derivative remainder includes the neighbouring terms
and the exact wall center. Every internal index n<=1499999 is in618.
The finite mass alone does not cover the final wall at index1500000.

Choose W=floor(4*pi*(1500000^2-3/256)). Two independent arithmetic
representations prove

    s_690988(a)<X<s_690989(A),
    s_1499999(a)<W<s_1500000(A)<W+1.

Since each wall decreases in t, X and W remain in their respective cells
throughout the CLOSED time band. Thus the finite region contains the
CLOSED rational rectangle [X,W]. Rounding up W would be unsound with
that last finite index; a mutation explicitly rejects it.

## T. The practical collision tail through infinity

Bank604's complete Euler-13 majorant includes all t in [a,A], every natural
N>=1499999 and the whole left-closed/right-open cell. Its global cap is
43/50; two complete numerical lines and independent verifier reconstruction
are already accepted. Bank613 identifies the same exact Euler product,
phase and remainder with general L7, giving true-H collision exclusion
on every such cell and the CLOSED rectangle [a,A] x [W,infinity).
Bank614 independently derives a stronger real-gauge transversality form
on the same rectangle, confirming the distinct normalization route.

For record use the external adoption proof is rerun LIVE as described in D.
It verifies the drift envelope from Y=26000000000000 through infinity,
the phase condition and exact charge

    751998000616933/130000000000000000000 <3/500000,
    1-M-C >69997/500000.

The root checker audits ALL finite tail-ledger block joints and bounds
and the accepted analytic infinite closure. Hash-selected rows re-evaluate
transport integrals in Python against the banked frozen outputs. Those
samples are provenance/representation audits, not replacement proofs of
the universal tail mass. Heavy C source and outputs are pinned under
FROZEN.sha256, citing bank604's source-only accepted check. No C is executed.

This practical tail asserts simplicity of REAL zeros, not reality of
all complex tail zeros. Section A's separate explicit remote theorem is
what the stall argument needs. Neither conclusion is silently promoted
to the other.

## F. Exact coverage on every axis

The checker emits exactly these three closed boxes, from the same rational
values used in its inclusion and union gates:

    COVER module=interior t=[333/2000,3/16] x=[0,6000000185827]
    COVER module=exterior t=[333/2000,3/16] x=[6000000185827,28274333882307]
    COVER module=tail t=[333/2000,3/16] x=[28274333882307,inf]

Their union is [a,A] x [0,infinity), including both times and both spatial
seams; evenness covers all negative real x. Each point is covered by at
least one proved no-multiple-real-zero module. Interior has no N restriction.
Exterior covers every natural N=n0..nT, and the tail covers N>=nT, including
the predecessor cell. The natural cell intervals are all left-closed/right-
open; each right endpoint uses the next index, and the last finite endpoint
is taken by the already overlapping tail. No N is skipped.

The y axis for collision exclusion is exactly0. Separately, the boundary
input covers all |y|<=1 over [0,A], padded to |y|<=2 by the published strip;
the remote stall-tail theorem covers all imaginary parts. These different
quantifiers remain separate. Exact breakpoint/open-slab union checks and
missing-time, missing-spatial-seam and premature-tail mutations are included.

## G. Conclusion, margin and verification

The accepted anchor and sections A--F prove Lambda<333/2000. The numerical
value and both exact improvements (against the banked3/16 and the preregistered
comparison target86211/500000) are derived LIVE. No claim from that comparison
target is a mathematical input. Credit Daniel Martin Kornaus for the collision-
exclusion architecture; all lemmas and certificates consumed here are our
accepted work or independently re-proved LIVE. No PR180 file enters this
package. The unchanged PT2021 height and exact margin are printed explicitly.

Run `/usr/bin/python3 verify_assembly.py` from a fresh copy. The root program
never reads RECORD.json, uses only local pinned files, no compiler/binary,
and invokes children only as [sys.executable,'name.py'] with inherited
confinement. The whole numerical external line is rerun; no trust in its
previous unbanked outputs is needed. Child logs are preserved and prefixed
on stdout so the root emits exactly one RESULT line. Exit zero requires
all proof-interface, arithmetic, coverage and child checks.

The foundational analytic arguments remain mathematics for adversarial
review, not a claim that finite unit tests are a formal proof assistant.
Two clean copies, strict claim_lint, candidate precheck and official scoring
are required. Digits use self-tested FLOOR/CEIL conversion of exact rational
or outward endpoints; nearest ball output and timings never enter a gate.
