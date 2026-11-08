#!/usr/bin/env python3
"""Build the manuscript with a standard local TeX installation."""
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
paper = root / "paper"
latex = shutil.which("pdflatex")
if not latex:
    raise SystemExit("pdflatex is required to build; the repository also includes the rendered PDF.")
build = Path(tempfile.mkdtemp(prefix="he3-tex-"))
for _ in range(2):
    result = subprocess.run([latex, "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape",
                             "-output-directory", str(build), "main.tex"], cwd=paper,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (build / "BUILD_STDOUT.txt").write_text(result.stdout)
    if result.returncode:
        raise SystemExit(f"TeX build failed; retained log: {build / 'BUILD_STDOUT.txt'}")
destination = paper / "He3_Source_Field_Certificates.pdf"
shutil.copy2(build / "main.pdf", destination)
print(f"PDF: {destination}\nBuild logs: {build}")
