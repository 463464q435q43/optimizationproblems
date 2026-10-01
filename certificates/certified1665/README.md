# Λ < 333/2000 for the de Bruijn–Newman constant: certificate bundle

**Claim.** The de Bruijn–Newman constant satisfies Λ < 333/2000 = 0.1665, unconditionally. The only finite-height input
on the Riemann hypothesis is Platt–Trudgian 2021 ([arXiv:2004.09765](https://arxiv.org/abs/2004.09765): RH up to height
3000175332800), used at height X/2 with X = 6000000185827, an exact margin of 350479773/2.

**Route.** If Λ > 0, then H_Λ has a multiple real zero (the positive-stall theorem, which uses an explicit radius beyond
which all zeros are real and simple, uniformly in t). The package shows that H_t has no multiple real zero for any t in
the closed band [333/2000, 3/16] and any real x, with three modules whose union is checked in exact arithmetic:

| module | x-range | argument |
| --- | --- | --- |
| interior | [0, X] | PT2021 makes every zero with \|Re z\| ≤ X real at t = 0; a certified zero-free boundary at x = ±X and the Hermite normal form keep them real, and simple for t > 0 |
| exterior | [X, W], W = 28274333882307 | one exact mollifier inverse of support 1024 frozen at t = 333/2000, every index N = 690988 … 1499999 |
| tail | [W, ∞) | Euler-13 majorant for every N ≥ 1499999, through infinity |

With the anchor Λ ≤ 3/16 ([MI2026b], [doi:10.5281/zenodo.21175533](https://doi.org/10.5281/zenodo.21175533), merged as
teorth/optimizationproblems PR #126) this gives Λ < 333/2000. The full argument is `assembly_ce_333_2000/ASSEMBLY.md`;
the machine-readable header is `assembly_ce_333_2000/RECORD.json`.

**Verify.** [VERIFY.md](VERIFY.md) has the commands: about two minutes on one core, with Python 3.12, python-flint 0.9.0,
sympy 1.12 and mpmath 1.2.1. Expected: `lambda_upper_exact 333/2000`, `coverage_ok 1`, `frozen_ok 1`, 156 checks,
`RESULT: ALL PASS`.

**Contents.**

- `assembly_ce_333_2000/`: the record package exactly as banked (candidate `b3a1b79ca032`: 63 files plus the bank's
  `MANIFEST.json`).
- `verify/`: the official scorer `record_score.py` and its sandbox `confine.py`, unmodified.
- `MANIFEST.sha256`: the sha256 of every file in those two directories.

**What is re-derived and what is cited.** `verify_assembly.py` re-derives the exact arithmetic, the index transitions and
the coverage union, and re-runs from source the exterior conversion and two independently written checkers
(`live_model_second/`, `live_adoption_second/`). The heavy C/Arb computations are not re-run: `FROZEN.sha256` pins their
outputs, and selected rows are replayed in Python. Lemmas accepted earlier in the campaign are cited from
`frozen/memory.json` by line and hash, with their written proofs in `frozen/` and `exterior/`. The anchor is cited, not
re-verified here. A passing run is a mechanical check, not a referee's verdict; the analytic arguments are offered for
review.

**Provenance.** Found and certified by Mosaic Intelligence's verifier-gated agent swarm, run with GPT-6 Astra Pro agents.
Banked 2026-09-30 19:45:31 UTC as candidate `b3a1b79ca032` (session `prover_astra-s9`; lineage `742687dfad45` →
`ddfc2b7d7ced` → `b3a1b79ca032`). The official evaluation and an independent re-score both returned 333/2000 with
coverage_ok 1, frozen_ok 1, conditional 0, 156 checks, 3 cover boxes and 9 legs, and the audit review passed. Not
refereed.

**AI disclosure.** This is a fully AI-derived result: the construction, the proofs and the checkers were produced and
checked by Mosaic Intelligence's automated system, and this text was AI-prepared.

**Acknowledgment.** The collision-exclusion approach of the open pull request [teorth/optimizationproblems#180](https://github.com/teorth/optimizationproblems/pull/180) inspired part of this route; the certificate does not depend on it, and no file, theorem, constant or code from it is used.
