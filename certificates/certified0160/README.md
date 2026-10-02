# Λ < 4/25 for the de Bruijn–Newman constant: certificate bundle

**Claim.** The de Bruijn–Newman constant satisfies Λ < 4/25 = 0.16, unconditionally. The only finite-height input on the
Riemann hypothesis is Platt–Trudgian 2021 ([arXiv:2004.09765](https://arxiv.org/abs/2004.09765): RH up to height
3000175332800), used at height X/2 with X = 6000000185827, an exact margin of 350479773/2.

**Route.** If Λ > 0, then H_Λ has a multiple real zero (the positive-stall theorem: every zero with |Re z| ≥ 4π·e^1600 + 1
is real and simple, uniformly for t in [2/25, 1/2]). The package shows that H_t has no multiple real zero for any t in the
closed band [4/25, 3/16] and any real x, with three modules whose union is checked in exact arithmetic:

| module | x-range | argument |
| --- | --- | --- |
| interior | [0, X] | PT2021 makes every zero of H_0 with \|Re z\| ≤ X real; a certified separator at x = ±X (every t in [0, 3/16], \|y\| ≤ 1, padded to 2) and Hermite propagation keep them real, and simple for t > 0 |
| exterior | [X, W], W = 66476100549959 | a complete strong weighted Gram source at t = 4/25, N = 690988 (all 3524 closed leaves of the four-prime torus), carried to every index N = 690988 … 2299999 on the closed band; its independent recovery second line runs live |
| tail | [W, ∞) | Euler-13 real-axis jet reserve for every N ≥ 2299999, with no terminal cutoff |

With the anchor Λ ≤ 3/16 ([MI2026b], [doi:10.5281/zenodo.21175533](https://doi.org/10.5281/zenodo.21175533), merged as
teorth/optimizationproblems PR #126) this gives Λ < 4/25. The full argument is `assembly_ce_4_25/ASSEMBLY.md`; the
machine-readable header is `assembly_ce_4_25/RECORD.json`.

**Verify.** [VERIFY.md](VERIFY.md) has one command: about 10 s on a 16-vCPU machine, with Python 3.12, python-flint 0.9.0,
sympy 1.12 and mpmath 1.2.1. Expected: `lambda_upper_exact 4/25`, every gate 1, 1858294 checks, `RESULT: ALL PASS`, and
verify-script output byte-identical to the banked run.

**Contents.**

- `assembly_ce_4_25/`: the record package exactly as banked (candidate `9c524a202dfd`: 109 files plus the bank's
  `MANIFEST.json`).
- `verify/`: the official scorer `record_score.py` and its sandbox `confine.py`, unmodified.
- `MANIFEST.sha256`: the sha256 of every file in those two directories.

**What is re-derived and what is cited.** `verify.py` re-runs from source the exact composition arithmetic
(`math/verify.py`: Arb at 256 bits, sympy and exact rationals) with its independent second line (`math/second_line.py`,
mpmath interval arithmetic), the coverage union and the index transitions. It also runs the complete, independently
written recovery check of the finite exterior (`RECOVERY_LIVE.json`: all 690988 raw and 157940 weight cells, 224 bins,
14 leaves and 1609011 entrants). Heavy computations accepted earlier in the campaign are not re-run: `FROZEN.sha256` pins
their outputs and written proofs, which are cited by bank line and hash, and the shipped C source is provenance only and
is never compiled. The anchor is cited, not re-verified here. A passing run is a mechanical check, not a referee's
verdict; the analytic arguments are offered for review.

**Provenance.** Found and certified by Mosaic Intelligence's verifier-gated agent swarm, run with GPT-6 Astra Pro agents.
Banked 2026-10-02 13:18:43 UTC as candidate `9c524a202dfd` (session `prover_astra-s31`; parent `43521b7b536c`, the swarm's
33/200 record). The swarm's official and verify harness runs both returned 4/25 with every gate 1, and its audit review
passed. Before publication an independent check re-scored the package on a fresh pod, including from a source-only copy,
and re-ran the banked checks of five of the bank lines it cites; everything matched. Not refereed.

**AI disclosure.** This is a fully AI-derived result: the construction, the proofs and the checkers were produced and
checked by Mosaic Intelligence's automated system, and this text was AI-prepared.

**Acknowledgment.** The collision-exclusion approach of the open pull request [teorth/optimizationproblems#180](https://github.com/teorth/optimizationproblems/pull/180) inspired part of this route; the certificate does not depend on it, and no file, theorem, constant or code from it is used.
