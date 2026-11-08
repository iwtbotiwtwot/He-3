# He-3: exact source reduction and complete field payment

This repository accompanies **Exact Source Reduction and Complete Field-Energy Certificates for a He-3 Model**, by Sean Brady, 8 November 2026. It contains the manuscript source, a rendered working draft, and portable evidence from the connected A1, relaxed-payment, independent-verification, free-reference and shared-field campaigns.

The main result is a conditional variational energy certificate below a declared fragment lower. The finite source has an exact ground law on its full 192-by-64 parent. The field account retains placement variance, the full sharp frequency profile, both physical helicities, source/Fock complements, recoil and the stated localized-gate allowance. Four nonempty parameter intervals are certified by exact rational signs and monotonicity.

## Reproduce

Python 3.12 or later, standard library only:

```bash
python3 -I -B reproduce.py
```

The command authenticates every retained scientific evidence file, runs two distinct payment reconstructions and three verification cases, and compares the fresh mathematical results with their sealed references. It writes results and logs to a new temporary directory and prints its location. No Duck engine, AI service, network, SciPy, private project checkout or original absolute path is needed.

To select a new destination:

```bash
python3 -I -B reproduce.py --output /tmp/he3-my-first-replay
```

An existing output directory is refused. All 12 mass/lane rows and the noncertifying controls are retained. Expected result: **PASS, 640 recorded verification checks, 18 registered controls, and both earlier payment routes**. These counts measure retained checks, not independent theorems or external reviews.

## Read

- [Manuscript PDF](paper/He3_Source_Field_Certificates.pdf) and [LaTeX source](paper/main.tex).
- [Claims and evidence map](docs/CLAIMS.md): theorem-level results, assumptions and exact replay routes.
- [Hypotheses](docs/HYPOTHESES.md): the finite model, inherited continuum/gate premises and physical assignments.
- [Reproducibility guide](docs/REPRODUCIBILITY.md): expected outputs, original scripts and portability.
- [Provenance and corrections](docs/PROVENANCE.md): campaign relationships and unchanged historical records.
- [Evidence manifest](provenance/EVIDENCE_MANIFEST.json): SHA-256 and origin of every retained evidence file.

The title's He-3 designation identifies the declared ppn source model. The parameter intervals are dimensionless sufficient certificates. The profile moments and complete gate inequality are explicit inherited premises. Physical species/current assignments, coupling normalization and complete atomic endpoints are identified in the paper as further model inputs.

## Build the paper

With a standard TeX installation containing `pdflatex`:

```bash
python3 -I -B tools/build_paper.py
```

The committed PDF allows the paper to be read without TeX. Building the paper does not run a new scientific campaign.

## Evidence organization

`evidence/he3_relaxed_field_20261108/` retains the two payment reconstructions and the subsequent verification. `evidence/isotope_constructor_checks_20261108/` retains the free-reference and shared-field proofs and replays. `evidence/context/` provides the A1 and constructor reports needed to follow the derivation. Historical files are copied verbatim, including failures, corrections and their original workflow terminology. Current paper claims are stated in `docs/CLAIMS.md`.

License terms have not yet been selected. No third-party paper is bundled; literature is cited by its public reference.
