#!/usr/bin/env python3
"""Official harness of the `lambda_upper` board: score a RECORD PACKAGE (objectives/lambda_upper/README.md).

    record_score.py --candidate DIR --out OUT_JSON [--timeout 1500]

The candidate is a self-contained record package (the v1 assembly_1875 pattern): RECORD.json (machine-readable header),
the writeup, and ONE standalone verify script that discharges every hypothesis of Thm 1.2 of arXiv:1904.12438 (citing banked
verified facts, re-deriving the rest live) and exits 0 iff all of its checks pass.

What this harness certifies MECHANICALLY (exact rationals, no floats in any gate):
  criterion  0 < t0, 0 < y0^2, y0^2 + 2 t0 <= 1, and lambda_upper >= t0 + y0^2/2
  rh         X/2 <= rh_height <= 3000175332800 (Platt-Trudgian 2021, arXiv:2004.09765 - the only accepted RH input) and
             conditional == false: the board is UNCONDITIONAL only
  script     the verify script runs from a fresh writable copy of the package WITHOUT RECORD.json / MANIFEST.json (it must
             derive what it prints), with no network, confined to the package by lib/confine.py (no outside file reads
             except the interpreter's libraries and /opt/mosaic/dbn_v1, no subprocess except confined children of the
             same interpreter, e.g. a second-line .py; no binaries); it exits 0, prints exactly one
             RESULT line "RESULT: ALL PASS", no failure marker (FAIL_MARK: [FAIL] / [FAILED] / [ERROR] anywhere, or a line
             starting FAIL / FAILED / FAILURE / ERROR, any case), no Traceback on stderr, and exactly one of each
             RECORD_LAMBDA_UPPER / RECORD_T0 / RECORD_Y0SQ / RECORD_X line whose exact values equal RECORD.json
  lint       every leg names its hypothesis, what it cites and what it consumes; coverage states all three axes (t, N, y)
  frozen     optional FROZEN.sha256 (sha256sum format) of frozen heavy-leg outputs: every listed file is inside the package
             and matches its hash in the submitted package (the script re-checks what it consumes)

RECORD.json `route` selects the bound structure; absent means "polymath_barrier" (everything above). The second route,
"collision_exclusion", is the no-multiple-real-zero argument: if H_t has no multiple real zero for every t in [t_lo, t_hi] and
Lambda <= anchor_upper <= t_hi is proved, then Lambda < t_lo. Its gates replace only the criterion and the RECORD_ lines:
  criterion  0 < t_lo < anchor_upper <= t_hi <= 1/2, lambda_upper >= t_lo
  anchor     anchor_source names a banked anchor fact (BANKED_ANCHORS) and anchor_upper >= its proven bound (so >= the
             verified board best): an anchor below what is banked is refused
  rh         unchanged, with X = the largest real abscissa the argument needs real zeros of H_0 on (the separator at t = 0)
  script     unchanged, with RECORD_LAMBDA_UPPER / RECORD_T_LO / RECORD_T_HI / RECORD_ANCHOR / RECORD_X equal to RECORD.json
  coverage   the script prints machine-readable boxes, one per line (exact rationals; x_hi may be "inf"; <= MAX_COVER lines)
                 COVER module=interior|exterior|tail t=[a,b] x=[c,d]
             and their union, as closed boxes, must cover [t_lo, t_hi] x [0, inf) exactly (every open t-slab AND every
             t-breakpoint, i.e. joints on both axes); interior boxes stay at x <= X (the separator consumes RH only to X/2)
  lint       unchanged (legs; coverage t, N, y)

What it does NOT certify: that the cited legs exist, are banked verified facts, and cover exactly what the package consumes
(the quantifier audit). That is the verifier seat's review (target.yaml verifier.llm_review) and the doctrine's two-line rule.

Score = float(lambda_upper) (minimize). A package that fails a gate gets a receipt with the gate metric 0 (the objective's
constraints reject it) and score 1.0; an unreadable RECORD.json is ok=false.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

RH_MAX = 3000175332800  # PT2021 (arXiv:2004.09765): RH verified to height T = 3,000,175,332,800
REQUIRED = ("lambda_upper", "t0", "y0_sq", "X", "rh_height", "rh_source", "verify_script", "writeup", "legs", "coverage", "conditional")
REQUIRED_CE = ("lambda_upper", "t_lo", "t_hi", "anchor_upper", "anchor_source", "X", "rh_height", "rh_source", "verify_script",
               "writeup", "legs", "coverage", "conditional")
ROUTES = ("polymath_barrier", "collision_exclusion")
RECORD_LINE = re.compile(r"^RECORD_(LAMBDA_UPPER|T0|Y0SQ|X|T_LO|T_HI|ANCHOR)\s*=\s*(\S+)\s*$", re.MULTILINE)
RATIONAL = re.compile(r"^\s*-?\d+(\s*/\s*\d+)?\s*$|^\s*-?\d+\.\d+\s*$")
FAIL_MARK = re.compile(r"\[\s*(fail(ed|ure)?|error)\s*\]|^\s*(fail(ed|ure)?|error)\b", re.IGNORECASE)
HIDDEN = ("RECORD.json", "MANIFEST.json")
CONFINE = Path(__file__).resolve().parent / "confine.py"
VIOLATION = "CONFINE-VIOLATION"
# Banked facts a collision_exclusion package may use as its anchor, with the Lambda bound each one PROVES. The minimum is the
# verified board best; add a row only when a new record is banked as a verified fact (V1 id or mosaic2 memory line).
BANKED_ANCHORS = {"V1-H-213": Fraction(3, 16)}
BOARD_BEST = min(BANKED_ANCHORS.values())
ANCHOR_ID = re.compile(r"\bV1-[A-Z]-\d+\b|\bmemory line \d+\b", re.IGNORECASE)
COVER_LINE = re.compile(r"^COVER\s+module=(\S+)\s+t=\[([^,\]]+),([^\]]+)\]\s+x=\[([^,\]]+),([^\]]+)\]\s*$", re.MULTILINE)
COVER_MODULES = ("interior", "exterior", "tail")
MAX_COVER = 2000
INF = float("inf")
FROZEN = "FROZEN.sha256"
FROZEN_LINE = re.compile(r"^([0-9a-fA-F]{64}) [ *](\S.*?)\s*$")


def exact(v, name: str) -> Fraction:
    """An exact rational from a JSON value: an int, or a string 'p/q' / terminating decimal. Binary floats are refused."""
    if isinstance(v, bool):
        raise ValueError(f"{name}: boolean is not a number")
    if isinstance(v, int):
        return Fraction(v)
    if isinstance(v, float):
        raise ValueError(f"{name}: write exact values as strings ('p/q' or a terminating decimal), not JSON floats")
    if isinstance(v, str) and RATIONAL.match(v):
        try:
            return Fraction(v.replace(" ", ""))
        except ZeroDivisionError:
            raise ValueError(f"{name}: zero denominator: {v!r}") from None
    raise ValueError(f"{name}: not an exact rational: {v!r}")


def x_covered(intervals: list) -> str | None:
    """None if the closed intervals cover [0, inf), else the first gap."""
    if not intervals:
        return "no box"
    reach: Fraction | float = Fraction(0)
    for lo, hi in sorted(intervals, key=lambda iv: iv[0]):
        if lo > reach:
            return f"x-gap ({reach}, {lo})"
        reach = max(reach, hi)
        if reach == INF:
            return None
    return f"x-gap ({reach}, inf)"


def coverage_gaps(boxes: list, t_lo: Fraction, t_hi: Fraction) -> list:
    """Exact check that the closed boxes (t_a, t_b, x_c, x_d) cover [t_lo, t_hi] x [0, inf): every open slab between
    consecutive t-breakpoints and every breakpoint itself (the joints) must be covered in x."""
    cuts = sorted({t_lo, t_hi} | {v for b in boxes for v in b[:2] if t_lo < v < t_hi})
    gaps = []
    for i, t in enumerate(cuts):
        g = x_covered([(c, d) for a, b, c, d in boxes if a <= t <= b])
        if g:
            gaps.append(f"t = {t}: {g}")
        if i + 1 < len(cuts):
            u = cuts[i + 1]
            g = x_covered([(c, d) for a, b, c, d in boxes if a <= t and b >= u])
            if g:
                gaps.append(f"t in ({t}, {u}): {g}")
        if len(gaps) >= 5:
            break
    return gaps


def check_frozen(cand: Path) -> tuple:
    """Optional FROZEN.sha256 (sha256sum format, '<64 hex>  <path inside the package>', '#' comments): the harness itself
    checks every listed frozen output against the SUBMITTED package before the script runs. Returns (errors, n_files)."""
    man = cand / FROZEN
    if not man.exists():
        return [], 0
    errs, n = [], 0
    for i, ln in enumerate(man.read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        mt = FROZEN_LINE.match(ln)
        if not mt:
            errs.append(f"{FROZEN} line {i}: not '<sha256>  <path>'")
            continue
        try:
            p = inside(cand, mt.group(2))
        except ValueError as e:
            errs.append(f"{FROZEN} line {i}: {e}")
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != mt.group(1).lower():
            errs.append(f"{FROZEN} line {i}: sha256 mismatch for {mt.group(2)}")
        n += 1
    if not n and not errs:
        errs.append(f"{FROZEN}: lists no files")
    return errs[:6], n


def parse_cover(out: str, X: Fraction) -> tuple:
    boxes, errs = [], []
    for mod, a, b, c, d in COVER_LINE.findall(out)[: MAX_COVER + 1]:
        try:
            ta, tb, xc = exact(a.strip(), "COVER t"), exact(b.strip(), "COVER t"), exact(c.strip(), "COVER x")
            xd = INF if d.strip().lower() == "inf" else exact(d.strip(), "COVER x")
        except ValueError as e:
            errs.append(str(e))
            continue
        if mod not in COVER_MODULES:
            errs.append(f"COVER module {mod!r}: known modules are {list(COVER_MODULES)}")
        elif not (ta <= tb and xc <= xd):
            errs.append(f"COVER box t=[{ta},{tb}] x=[{xc},{xd}] is empty")
        elif mod == "interior" and xd > X:
            errs.append(f"COVER interior box reaches x = {xd} > X = {X} (the separator consumes RH only to X/2)")
        else:
            boxes.append((ta, tb, xc, xd))
    if len(COVER_LINE.findall(out)) > MAX_COVER:
        errs.append(f"more than {MAX_COVER} COVER lines: aggregate boxes per module and t-slab")
    return boxes, errs


def floor_str(fr: Fraction, k: int) -> str:
    n = (fr * 10**k).numerator // (fr * 10**k).denominator
    s = str(abs(n)).rjust(k + 1, "0")
    return ("-" if n < 0 else "") + s[:-k] + "." + s[-k:]


def pick_python() -> str:
    for py in ("/usr/bin/python3", sys.executable):
        try:
            r = subprocess.run([py, "-c", "import mpmath, sympy"], capture_output=True, timeout=60)
            if r.returncode == 0:
                return py
        except (OSError, subprocess.TimeoutExpired):
            continue
    return "/usr/bin/python3"


def inside(root: Path, rel: str) -> Path:
    p = (root / rel).resolve()
    if not str(p).startswith(str(root.resolve()) + "/") or not p.is_file():
        raise ValueError(f"{rel!r} is not a file inside the package")
    return p


def score(cand: Path, work: Path, timeout: int) -> dict:
    rec = json.loads((cand / "RECORD.json").read_text(encoding="utf-8"))
    if not isinstance(rec, dict):
        raise ValueError("RECORD.json must be an object")
    route = rec.get("route", "polymath_barrier")
    if route not in ROUTES:
        raise ValueError(f"RECORD.json route {route!r}: known routes are {list(ROUTES)}")
    missing = [k for k in (REQUIRED if route == "polymath_barrier" else REQUIRED_CE) if k not in rec]
    if missing:
        raise ValueError(f"RECORD.json missing keys: {missing}")
    lam = exact(rec["lambda_upper"], "lambda_upper")
    X, rh = exact(rec["X"], "X"), exact(rec["rh_height"], "rh_height")
    notes = []
    if route == "polymath_barrier":
        t0, y0sq = exact(rec["t0"], "t0"), exact(rec["y0_sq"], "y0_sq")
        functional = t0 + y0sq / 2
        crit = t0 > 0 and y0sq > 0 and y0sq + 2 * t0 <= 1 and lam >= functional
        want = {"LAMBDA_UPPER": lam, "T0": t0, "Y0SQ": y0sq, "X": X}
        if not crit:
            notes.append(f"criterion gate: need 0 < t0, 0 < y0^2, y0^2 + 2 t0 <= 1, lambda_upper >= t0 + y0^2/2 "
                         f"(= {functional.numerator}/{functional.denominator})")
    else:
        t0, t_hi, anchor = exact(rec["t_lo"], "t_lo"), exact(rec["t_hi"], "t_hi"), exact(rec["anchor_upper"], "anchor_upper")
        y0sq = Fraction(0)
        functional = t0
        crit = 0 < t0 < anchor <= t_hi <= Fraction(1, 2) and lam >= t0
        want = {"LAMBDA_UPPER": lam, "T_LO": t0, "T_HI": t_hi, "ANCHOR": anchor, "X": X}
        if not crit:
            notes.append("criterion gate (collision_exclusion): need 0 < t_lo < anchor_upper <= t_hi <= 1/2, lambda_upper >= t_lo")
        named = {i.upper() for i in ANCHOR_ID.findall(str(rec.get("anchor_source") or ""))} & set(BANKED_ANCHORS)
        proven = min((BANKED_ANCHORS[i] for i in named), default=None)
        anchor_ok = proven is not None and anchor >= proven >= BOARD_BEST
        if not anchor_ok:
            notes.append(f"anchor gate: anchor_source must name a banked anchor fact {sorted(BANKED_ANCHORS)} and anchor_upper "
                         f"must be >= its proven bound (the verified board best is {BOARD_BEST}); got named={sorted(named)}, "
                         f"anchor_upper={anchor}")
    m: dict = {
        "route": route,
        "lambda_upper_exact": f"{lam.numerator}/{lam.denominator}",
        "lambda_upper_floor10": floor_str(lam, 10),
        "t0_exact": f"{t0.numerator}/{t0.denominator}",
        "y0_sq_exact": f"{y0sq.numerator}/{y0sq.denominator}",
        "X_exact": str(X),
        "rh_height": str(rh),
        "functional_exact": f"{functional.numerator}/{functional.denominator}",
        "legs": len(rec["legs"]) if isinstance(rec["legs"], list) else 0,
        "conditional": 1 if rec["conditional"] is not False else 0,
    }
    if route == "collision_exclusion":
        m["t_hi_exact"] = f"{t_hi.numerator}/{t_hi.denominator}"
        m["anchor_exact"] = f"{anchor.numerator}/{anchor.denominator}"
    src = str(rec.get("rh_source") or "")
    rh_ok = X > 0 and X / 2 <= rh <= RH_MAX and ("2004.09765" in src or "PT2021" in src.upper().replace(" ", "")) and rec["conditional"] is False
    if not rh_ok:
        notes.append(f"rh gate: need X/2 <= rh_height <= {RH_MAX}, rh_source citing PT2021 / arXiv:2004.09765, conditional false")
    m["rh_margin"] = str(RH_MAX - X / 2) if X > 0 else "n/a"
    lint = []
    legs = rec["legs"] if isinstance(rec["legs"], list) else []
    if not legs:
        lint.append("legs: empty")
    for i, leg in enumerate(legs):
        if not isinstance(leg, dict) or not all(str(leg.get(k) or "").strip() for k in ("hypothesis", "cites", "consumes")):
            lint.append(f"legs[{i}]: needs non-empty hypothesis, cites, consumes")
    cov = rec["coverage"] if isinstance(rec["coverage"], dict) else {}
    for axis in ("t", "N", "y"):
        if not str(cov.get(axis) or "").strip():
            lint.append(f"coverage.{axis}: missing (coverage inventories state all three axes)")
    m["lint_ok"] = 0 if lint else 1
    notes += lint
    frozen_errs, m["frozen_files"] = check_frozen(cand)
    m["frozen_ok"] = 0 if frozen_errs else 1
    notes += frozen_errs
    script = inside(cand, str(rec["verify_script"]))
    inside(cand, str(rec["writeup"]))
    pkg = work / "pkg"
    shutil.rmtree(pkg, ignore_errors=True)
    shutil.copytree(cand, pkg, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", *HIDDEN))
    for p in pkg.rglob("*"):
        try:
            p.chmod(0o755 if p.is_dir() else 0o644)
        except OSError:
            pass
    py = pick_python()
    site = work / "confine_site"
    shutil.rmtree(site, ignore_errors=True)
    site.mkdir()
    shutil.copyfile(CONFINE, site / "sitecustomize.py")
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(site), "MOSAIC2_CONFINE_PKG": str(pkg),
                "MOSAIC2_CONFINE_SITE": str(site), "MOSAIC2_CONFINE_LIB": str(CONFINE.parent)})
    run_script = pkg / script.relative_to(cand.resolve())
    t = time.time()
    try:
        r = subprocess.run([py, str(CONFINE), str(pkg), str(run_script)], cwd=run_script.parent, capture_output=True, text=True,
                           timeout=timeout, env=env)
        rc, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        rc, out, err = -9, (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), f"timeout after {timeout}s"
    m["script_seconds"] = round(time.time() - t, 1)
    (work / "verify_stdout.txt").write_text(out, encoding="utf-8")
    (work / "verify_stderr.txt").write_text(err or "", encoding="utf-8")
    fails = [ln for ln in out.splitlines() if FAIL_MARK.search(ln)]
    results = [ln.strip() for ln in out.splitlines() if ln.strip().upper().startswith("RESULT")]
    all_pass = results == ["RESULT: ALL PASS"]
    violations = [ln.strip() for ln in (err or "").splitlines() if VIOLATION in ln]
    traceback = "Traceback (most recent call last)" in (err or "")
    m["confine_violations"] = len(violations)
    m["script_ok"] = 1 if (rc == 0 and all_pass and not fails and not violations and not traceback) else 0
    if not m["script_ok"]:
        notes.append(f"script gate: exit {rc}, RESULT lines {results[:3]!r} (need exactly ['RESULT: ALL PASS']), "
                     f"{len(fails)} failure-marker line(s) {[ln[:80] for ln in fails[:2]]!r}, {len(violations)} confinement "
                     f"violation(s) {violations[:2]!r}, traceback {'yes' if traceback else 'no'}; stderr: {(err or '')[-300:]}")
    nc = re.search(r"^TOTAL CHECKS RUN:\s*(\d+)", out, re.MULTILINE)
    m["checks_run"] = int(nc.group(1)) if nc else 0
    found: dict = {}
    for key, val in RECORD_LINE.findall(out):
        found.setdefault(key, []).append(val)
    line_ok = True
    for key, v in want.items():
        vals = found.get(key, [])
        try:
            if len(vals) != 1 or exact(vals[0], key) != v:
                line_ok = False
                notes.append(f"record line RECORD_{key}: printed {vals!r}, RECORD.json says {v}")
        except ValueError as e:
            line_ok = False
            notes.append(f"record line RECORD_{key}: {e}")
    m["record_lines_ok"] = 1 if line_ok else 0
    cover_ok = True
    if route == "collision_exclusion":
        boxes, errs = parse_cover(out, X)
        gaps = coverage_gaps(boxes, t0, t_hi) if boxes else ["no COVER lines"]
        cover_ok = not errs and not gaps
        m["cover_boxes"] = len(boxes)
        m["anchor_ok"] = 1 if anchor_ok else 0
        if not cover_ok:
            notes.append("coverage gate: " + "; ".join((errs + gaps)[:6]))
        crit = crit and anchor_ok
    m["coverage_ok"] = 1 if cover_ok else 0
    m["criterion_ok"] = 1 if crit else 0
    m["rh_ok"] = 1 if rh_ok else 0
    m["python"] = py
    m["notes"] = " | ".join(notes)[:1500]
    gates = crit and rh_ok and m["script_ok"] and line_ok and cover_ok and not lint and not frozen_errs
    return {"ok": True, "score": float(lam) if gates else 1.0, "metrics": m, "error": None, "artifacts": ["verify_stdout.txt"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--timeout", type=int, default=1500)
    a = ap.parse_args()
    work = a.out.parent
    try:
        receipt = score(a.candidate, work, a.timeout)
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError) as e:
        receipt = {"ok": False, "score": None, "metrics": {}, "error": f"{type(e).__name__}: {e}"}
    a.out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("ok", "score", "error")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
