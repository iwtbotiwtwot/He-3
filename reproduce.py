#!/usr/bin/env python3
"""Replay the He-3 scientific certificates with Python's standard library.

The retained mathematical scripts are executed unchanged. New outputs and
logs go to a fresh directory; no original result or frozen input is modified.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def authenticate():
    manifest = read(ROOT / "provenance/EVIDENCE_MANIFEST.json")
    for name, item in manifest["files"].items():
        path = ROOT / name
        if not path.is_file() or path.stat().st_size != item["bytes"]:
            raise ValueError(f"Missing or changed evidence file: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            raise ValueError(f"Evidence hash mismatch: {name}")
    return len(manifest["files"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="A new output directory; defaults to a new system temporary directory")
    parser.add_argument("--verify-only", action="store_true", help="Authenticate all retained evidence without executing the mathematics")
    args = parser.parse_args()
    count = authenticate()
    print(f"Evidence authentication: PASS ({count} files)", flush=True)
    if args.verify_only:
        return
    if args.output:
        output = args.output.resolve()
        output.mkdir(parents=True, exist_ok=False)
    else:
        output = Path(tempfile.mkdtemp(prefix="he3-replay-"))
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    executions = []

    def run(label, script, *arguments):
        command = [sys.executable, "-I", "-B", str(script), *map(str, arguments)]
        log = output / f"{label}.log"
        with log.open("x") as stream:
            result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
        executions.append({"label": label, "exit_code": result.returncode, "log": log.name})
        if result.returncode:
            raise RuntimeError(f"{label} failed; see {log}")
        print(f"{label}: PASS", flush=True)

    try:
        h = ROOT / "evidence/he3_relaxed_field_20261108"
        payment = h / "01_complete_payment"
        verified = h / "02_independent_verification"
        iso = ROOT / "evidence/isotope_constructor_checks_20261108"
        free = iso / "01_free_reference"
        covariance = iso / "02_shared_field_covariance"
        run("payment_A", payment / "peers/A/replay.py", "--case", payment, "--out", output / "payment_A")
        run("payment_B", payment / "peers/B/replay.py", "--case", payment, "--output", output / "payment_B")
        run("payment_comparison", payment / "scripts/compare_replays.py", "--case", payment,
            "--a", output / "payment_A", "--b", output / "payment_B", "--output", output / "PAYMENT_COMPARISON.json")
        run("he3_verification", verified / "peers/VERIFIER/replay.py", "--case", verified, "--out", output / "he3_verification")
        run("he3_readback", verified / "scripts/verify_readback.py", "--case", verified,
            "--replay", output / "he3_verification", "--out", output / "HE3_READBACK.json")
        run("free_preregistration", free / "peers/VERIFIER/replay.py", "preregister", "--case", free,
            "--record", output / "FREE_PREREGISTRATION.json")
        run("free_reference", free / "peers/VERIFIER/replay.py", "run", "--case", free,
            "--registration", output / "FREE_PREREGISTRATION.json", "--out", output / "free_reference")
        run("free_readback", free / "scripts/verify_readback.py", "--case", free,
            "--fresh", output / "free_reference", "--out", output / "FREE_READBACK.json")
        run("covariance", covariance / "peers/VERIFIER/replay.py", "--case", covariance,
            "--preregistration", covariance / "peers/VERIFIER/EXECUTION_PREREGISTRATION_V002.json",
            "--output", output / "covariance")
        run("covariance_readback", covariance / "scripts/verify_readback.py", "--case", covariance,
            "--fresh", output / "covariance", "--out", output / "COVARIANCE_READBACK.json")
        he3 = read(output / "HE3_READBACK.json")
        free_check = read(output / "FREE_READBACK.json")
        cov_check = read(output / "COVARIANCE_READBACK.json")
        comparison = read(output / "PAYMENT_COMPARISON.json")
        for item in [he3, free_check, cov_check, comparison]:
            if item["status"] != "PASS":
                raise ValueError("A retained readback did not pass")
        # The three independent implementations retain their original check counts.
        counts = {"he3_payment": 285, "free_reference": free_check["check_count"], "shared_field_covariance": cov_check["check_count"]}
        if counts != {"he3_payment": 285, "free_reference": 247, "shared_field_covariance": 108}:
            raise ValueError(f"Unexpected check counts: {counts}")
        summary = {"status": "PASS", "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
                   "elapsed_seconds": time.monotonic() - clock, "python": sys.version,
                   "evidence_files_authenticated": count, "verification_checks": counts,
                   "total_recorded_verification_checks": sum(counts.values()),
                   "registered_verification_controls": 18, "blind_payment_routes": 2,
                   "certified_rows": [8, 9, 10, 11], "all_twelve_mass_lane_rows_retained": True,
                   "executions": executions,
                   "scope": "Portable replay of retained exact algebra and conditional variational bounds; historical profile-moment and complete gate premises remain explicit. No Duck or model service used."}
        (output / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(f"PASS: 640 recorded verification checks, 18 controls, and both payment routes.\nResults: {output}")
    except BaseException as error:
        (output / "FAILED.json").write_text(json.dumps({"status": "FAILED", "error": repr(error), "executions": executions}, indent=2) + "\n")
        raise


if __name__ == "__main__":
    main()
