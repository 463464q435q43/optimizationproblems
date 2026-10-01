# Verifying Λ < 333/2000

Run everything below from this directory. It takes about two minutes on one CPU core with less than 0.5 GB of RAM, and
needs no network access once the packages are installed.

## Environment

Reference: a fresh Ubuntu 24.04 x86_64 machine or container, as root. The official evaluation used Python 3.12.3,
python-flint 0.9.0, sympy 1.12 and mpmath 1.2.1 (sympy and mpmath are Ubuntu 24.04's own packages).

```sh
# for example: docker run --rm -it -v "$PWD":/bundle:ro -w /bundle ubuntu:24.04
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq --no-install-recommends python3 python3-pip python3-sympy python3-mpmath
python3 -m pip install --break-system-packages python-flint==0.9.0
python3 -c 'import sys, flint, sympy, mpmath; print(sys.version.split()[0], flint.__version__, sympy.__version__, mpmath.__version__)'
```

`record_score.py` runs the verify script with `/usr/bin/python3` whenever that interpreter can import sympy and mpmath,
and otherwise with the interpreter that runs `record_score.py`. Install python-flint for the one it picks; the receipt's
`metrics.python` names it.

## 1. Integrity

```sh
sha256sum -c --quiet MANIFEST.sha256 && echo "MANIFEST.sha256: all $(wc -l < MANIFEST.sha256) files OK"
python3 - <<'EOF'
import hashlib, json, pathlib
root = pathlib.Path("assembly_ce_333_2000")
man = json.loads((root / "MANIFEST.json").read_text())
disk = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
ok = [f for f, h in man["files"].items() if (root / f).is_file() and hashlib.sha256((root / f).read_bytes()).hexdigest() == h]
print(f"bank MANIFEST.json, candidate {man['candidate_id']}: {len(ok)}/{len(man['files'])} match, unlisted files: {sorted(disk - set(man['files']))}")
EOF
```

On macOS use `shasum -a 256 -c MANIFEST.sha256`. The package's own `FROZEN.sha256` is checked by both the scorer and the
verify script.

## 2. Official scorer

```sh
rm -rf /tmp/dbn_score && mkdir -p /tmp/dbn_score
python3 verify/record_score.py --candidate assembly_ce_333_2000 --out /tmp/dbn_score/score.json --timeout 1500
python3 -c 'import json; m = json.load(open("/tmp/dbn_score/score.json"))["metrics"]; print({k: m[k] for k in ("lambda_upper_exact", "coverage_ok", "frozen_ok", "checks_run", "cover_boxes", "legs", "conditional", "criterion_ok", "anchor_ok", "rh_ok", "script_ok", "lint_ok", "record_lines_ok", "confine_violations")})'
```

The scorer copies the package to `/tmp/dbn_score/pkg` without `RECORD.json` and `MANIFEST.json` and runs
`verify_assembly.py` there under `verify/confine.py`, a PEP 578 audit hook that refuses file access outside the package
and the interpreter's libraries, network sockets, and any subprocess other than the same interpreter. It then checks the
script's output against `RECORD.json` in exact rational arithmetic. `confine.py` also permits reads of
`/opt/mosaic/dbn_v1`, an archive on the original host; this package never reads it.

## 3. The verify script directly

```sh
rm -rf /tmp/dbn_direct && cp -r assembly_ce_333_2000 /tmp/dbn_direct
(cd /tmp/dbn_direct && python3 verify_assembly.py > stdout.txt 2> stderr.txt; echo "verify_assembly.py exit code: $?"; tail -n 7 stdout.txt)
```

The script writes its outputs next to itself, hence the scratch copy.

## 4. Optional: byte-level comparison with the banked runs

```sh
python3 - <<'EOF'
import hashlib, json, pathlib, re
want = json.loads(pathlib.Path("assembly_ce_333_2000/CLEAN_COPIES.json").read_text())["mathematical_outputs_sha256"]
for run in ("/tmp/dbn_score/pkg", "/tmp/dbn_direct"):
    ok = sum(pathlib.Path(run, f).is_file() and hashlib.sha256(pathlib.Path(run, f).read_bytes()).hexdigest() == h for f, h in want.items())
    print(f"{run}: {ok}/{len(want)} generated JSON outputs match CLEAN_COPIES.json")
norm = lambda s: [re.sub(r'"cpu_seconds_diagnostic": [0-9.]+', '"cpu_seconds_diagnostic": T', l) for l in s.splitlines() if "CPU_SECONDS_DIAGNOSTIC" not in l]
same = norm(pathlib.Path("/tmp/dbn_direct/stdout.txt").read_text()) == norm(pathlib.Path("assembly_ce_333_2000/clean_copy_1.log").read_text())
print("stdout equals the banked clean_copy_1.log apart from CPU-time diagnostics:", same)
EOF
```

## Expected output

```text
MANIFEST.sha256: all 66 files OK
bank MANIFEST.json, candidate b3a1b79ca032: 63/63 match, unlisted files: []
{"ok": true, "score": 0.1665, "error": null}
{'lambda_upper_exact': '333/2000', 'coverage_ok': 1, 'frozen_ok': 1, 'checks_run': 156, 'cover_boxes': 3, 'legs': 9, 'conditional': 0, 'criterion_ok': 1, 'anchor_ok': 1, 'rh_ok': 1, 'script_ok': 1, 'lint_ok': 1, 'record_lines_ok': 1, 'confine_violations': 0}
verify_assembly.py exit code: 0
TOTAL CHECKS RUN: 156
RESULT: ALL PASS
RECORD_LAMBDA_UPPER = 333/2000
RECORD_T_LO = 333/2000
RECORD_T_HI = 3/16
RECORD_ANCHOR = 3/16
RECORD_X = 6000000185827
/tmp/dbn_score/pkg: 6/6 generated JSON outputs match CLEAN_COPIES.json
/tmp/dbn_direct: 6/6 generated JSON outputs match CLEAN_COPIES.json
stdout equals the banked clean_copy_1.log apart from CPU-time diagnostics: True
```
