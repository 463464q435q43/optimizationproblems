# Verifying Λ < 4/25

Run the commands below from this directory on a fresh Ubuntu 24.04 x86_64 machine or container, as root. Nothing needs
the network once the packages are installed.

## Environment

The official evaluation used Python 3.12.3, python-flint 0.9.0, sympy 1.12 and mpmath 1.2.1 (sympy and mpmath are
Ubuntu 24.04's own packages).

```sh
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq --no-install-recommends python3 python3-pip python3-sympy python3-mpmath
python3 -m pip install --quiet --break-system-packages python-flint==0.9.0
```

## Reproduce

```sh
sha256sum -c --quiet MANIFEST.sha256 && echo "MANIFEST.sha256: all $(wc -l < MANIFEST.sha256) files OK" && mkdir -p /tmp/dbn0160 && python3 verify/record_score.py --candidate assembly_ce_4_25 --out /tmp/dbn0160/score.json --timeout 1500 && python3 -c 'import json; m = json.load(open("/tmp/dbn0160/score.json"))["metrics"]; print({k: m[k] for k in ("lambda_upper_exact", "criterion_ok", "anchor_ok", "rh_ok", "script_ok", "record_lines_ok", "lint_ok", "frozen_ok", "coverage_ok", "torus_ok", "conditional", "confine_violations", "checks_run", "cover_boxes")})' && cmp /tmp/dbn0160/verify_stdout.txt assembly_ce_4_25/record_gate.log && echo "verify stdout: byte-identical to the banked record_gate.log"
```

Expected output:

```text
MANIFEST.sha256: all 112 files OK
{"ok": true, "score": 0.16, "error": null}
{'lambda_upper_exact': '4/25', 'criterion_ok': 1, 'anchor_ok': 1, 'rh_ok': 1, 'script_ok': 1, 'record_lines_ok': 1, 'lint_ok': 1, 'frozen_ok': 1, 'coverage_ok': 1, 'torus_ok': 1, 'conditional': 0, 'confine_violations': 0, 'checks_run': 1858294, 'cover_boxes': 3}
verify stdout: byte-identical to the banked record_gate.log
```

The scorer reports `"score": 0.16` only when every gate passes; any failed gate gives 1.0. The verify script's output,
`/tmp/dbn0160/verify_stdout.txt` (4,021 bytes, sha256 `d628a6a7089e2cff2ba9b29317821a1a56675e453e7cb03268fc07c56abcf663`),
ends with `RECORD_LAMBDA_UPPER = 4/25`, `TOTAL CHECKS RUN: 1858294` and `RESULT: ALL PASS`. On macOS, check the manifest
with `shasum -a 256 -c MANIFEST.sha256`.

**Runtime and cost.** Measured before publication on a fresh RunPod CPU pod (ubuntu:24.04, 16 vCPU AMD EPYC 4564P,
$0.56/h): the scorer takes 8–9 s and the package install about 25 s. That pod's whole life, including start-up and four
scorer runs, was 110 s and cost about $0.017. On a loaded 8-vCPU host the scorer took 34–39 s.

## What the scorer does

`record_score.py` is the swarm's official scorer, unmodified. It first checks the 82 hashes in `FROZEN.sha256`. It then
copies the package to `/tmp/dbn0160/pkg` without `RECORD.json` and `MANIFEST.json`, so the verify script must derive
everything it prints, and runs `verify.py` there under `verify/confine.py`: a PEP 578 audit hook that refuses file access
outside the package and the interpreter's libraries, network sockets, and any subprocess other than the same interpreter
(it guards against outside reads, it is not a security sandbox). Finally it checks, in exact rational arithmetic, that the
printed `RECORD_*` lines equal `RECORD.json` and that the three printed `COVER` boxes cover t in [4/25, 3/16] and
x in [0, ∞) exactly.

`record_score.py` runs the verify script with `/usr/bin/python3` whenever that interpreter can import sympy and mpmath,
and otherwise with the interpreter running `record_score.py`; the receipt's `metrics.python` names it. `confine.py` also
permits reads of `/opt/mosaic/dbn_v1`, an archive on the original host, which this package never reads. `RECORD.json` has
no `torus_certs`, so the torus gate passes vacuously and its checker is not needed.

## Optional checks

The package's content address equals its candidate id:

```sh
python3 -c 'import hashlib, json, pathlib; r = pathlib.Path("assembly_ce_4_25"); f = {str(p.relative_to(r)): hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob("*") if p.is_file() and str(p.relative_to(r)) != "MANIFEST.json"}; m = json.loads((r / "MANIFEST.json").read_text()); print(m["candidate_id"], hashlib.sha256(json.dumps(f, sort_keys=True).encode()).hexdigest()[:12], f == m["files"])'
```

Expected: `9c524a202dfd 9c524a202dfd True`.

The generated outputs come from source alone. This scores a copy holding only the 86 source inputs listed in
`CLEAN_COPIES.json` plus `RECORD.json`, then compares the 16 regenerated products with the hashes recorded there:

```sh
rm -rf /tmp/dbn0160_src && mkdir -p /tmp/dbn0160_src/out && python3 -c 'import json, pathlib, shutil; s = pathlib.Path("assembly_ce_4_25"); d = pathlib.Path("/tmp/dbn0160_src/pkg"); [((d / f).parent.mkdir(parents=True, exist_ok=True), shutil.copyfile(s / f, d / f)) for f in json.loads((s / "CLEAN_COPIES.json").read_text())["source_input_files"] + ["RECORD.json"]]' && python3 verify/record_score.py --candidate /tmp/dbn0160_src/pkg --out /tmp/dbn0160_src/out/score.json --timeout 1500 && python3 -c 'import hashlib, json, pathlib; w = json.loads(pathlib.Path("assembly_ce_4_25/CLEAN_COPIES.json").read_text())["copies"][0]["products"]; o = pathlib.Path("/tmp/dbn0160_src/out/pkg"); n = [f for f in w if f not in ("CHECK_RESULT.json", "record_gate.log", "record_gate_stderr.log")]; print(sum((o / f).is_file() and hashlib.sha256((o / f).read_bytes()).hexdigest() == w[f] for f in n), "of", len(n), "products match CLEAN_COPIES.json")' && cmp /tmp/dbn0160_src/out/verify_stdout.txt assembly_ce_4_25/record_gate.log && echo "source-only verify stdout: byte-identical"
```

Expected: `{"ok": true, "score": 0.16, "error": null}`, `16 of 16 products match CLEAN_COPIES.json` and
`source-only verify stdout: byte-identical`. The other three entries in `CLEAN_COPIES.json` come from the producing
seat's wrapper, not from the verify script.
