# CR2 free-reference verification: HELD

The frozen geometric statement holds without a mathematical correction. This is an I1 audit: newly authored exact standard-library code, the same inherited model, and an independent finite proof. It is not external verification or a physical binding assignment.

## Failures and corrections first

Attempt 001 failed in the verifier's boundary comparison: it used positive adjacency weights where the frozen boundary stores signed Hamiltonian entries `-2`. Attempt 002 corrected that convention and the corresponding collision row-sum calculation. The failed code, sealed prediction record, logs and failure receipt remain intact. No source, frozen statement, normalization or acceptance criterion changed.

All five registered breaking mutations failed as predicted:

| Mutation | Exact rejection |
|---|---|
| Use `12I24` as a full-source lower | Normalized 64-entry vector `1/8` has energy 0; its `H-12I` quadratic form is -12. |
| Declare adjacent invariance | `H[(0,0),(0,1)]=-2`; true drift rank 18. |
| Delete complement response | At `z=1`, full-minus-compressed diagonal resolvent defect is `3064/116025 > 0`; defect and self-energy rank 18. |
| Declare all 40 omitted addresses dark | Cyclic closure dimension 47 leaves 23 hidden directions and only 17 invariant dark directions. No omitted coordinate vector is individually dark. |
| Subtract `12 tau` on one endpoint only | The connected-versus-free difference changes from `18 tau` to `6 tau`; a common shift preserves `18 tau`. |

## Established result

The raw 48 source events give two events per oriented cube edge and `h1=6I8-2A(Q3)`. The complete free pair is the 64-dimensional tensor sum with spectrum `4k`, multiplicities `binom(6,k)`, and floor zero. The actual 24-column injection, derived in original order from the independent-cell tuples, is isometric and has compression `12I24`. Thus every normalized adjacent-supported preparation has expectation `12 tau` against that zero. This is not a lower bound for arbitrary full-source preparations.

An analytic Fourier decomposition and exact replay both give drift rank 18 and cyclic dimensions `24,42,46,47`. The invariant dark multiplicities at energies `0,4,8,12,16,20,24` are `0,0,3,11,3,0,0`. The 40-dimensional omitted complement splits into 23 dynamically hidden receiving directions and a 17-dimensional invariant dark space. The original Euclidean metric, full signed complement and exact Schur self-energy are retained.

At registered `z=1`, the full receiving resolvent has diagonal `11989/116025`, while the compressed inverse has diagonal `1/13`. The exact positive defect above, the full 64-by-24 solve, rational Schur equality and positive LDL certificates are retained. More generally, the proof shows a positive-semidefinite rank-18 defect for every `z>0`.

The full three-free source is 512-dimensional with floor zero. Its actual pair-major 192-state compression is `I24 tensor h1 + 12I192`, with spectrum `12,16,20,24` and multiplicities `24,72,72,24`. It leaves 320 earlier omitted addresses. All 48 legal tuples with equal local digits across different cells remain. The subsequent 48-state connected injection has compression `18I48`, giving an additional preparation cost `6 tau` above the primary floor and total cost `18 tau` against the complete three-free floor.

The primary injection's cyclic closure is additionally proved to have dimension 376, with 184 hidden and 136 invariant dark directions, and drift rank 144. This is an exact tensor consequence, not a separate numerical rank fit.

The older 144-state all-distinct fragment chart, its operator, signed boundary and connected map were also reconstructed. The prior He3 theorem remains inherited in that named chart; it was not reproved or reassigned a physical all-free reference here.

## Evidence and replay

Attempt 002 passed 247 exact assertions. Every public freeze hash and every one of the 13 custody snapshot entries matched its own recorded hash. The source program/generator/replay/native logic and prior reports/results were not interpreted. Only frozen raw mathematical operands entered the reconstruction; prior files were hashed as opaque bytes.

- [Full proof](DERIVATION.md), [hypothesis map](HYPOTHESES.md), [working notes and correction history](NOTES.md), [machine result](RESULTS.json).
- [Completed exact attempt](attempts/attempt_002/output/COMPLETE.json), [all checks](attempts/attempt_002/output/CHECKS.json), [matrix and response certificates](attempts/attempt_002/output/RESOLVENT.json).
- [Preregistered predictions and script seal](attempts/attempt_002/EXECUTION_PREREGISTRATION.json). Authoritative script SHA-256: `9f31c15a382cb7a895d7c2a9b8265bc6a7e20381061b669760ea9b25ce541d73`.
- [Fixed-input authentication](provenance/INPUT_AUTHENTICATION.json), [custody snapshot authentication](provenance/CUSTODY_SNAPSHOT_AUTHENTICATION.json), [final file seal](SEAL.json).

Replay from this verifier directory, choosing new names if these exist:

```bash
python3 replay.py preregister --record attempts/replay_003_prereg.json
python3 replay.py run --registration attempts/replay_003_prereg.json --out attempts/replay_003_output
```

Python 3.12 standard library is sufficient. The CLI rejects an existing output directory or a script differing from its registration. Every output directory has its own start/completion or failure record and SHA-256 seal. All signs are integer or Fraction comparisons.

## Safe use in bridge/action work

The verified geometric operators, ordered isometries, preparation expectations, exact complement/self-energy and common-zero ledger can be used as geometric inputs. Interpret a preparation cost using one common nonnegative tau. A common shift by `-12 tau` moves the all-free floor to `-12 tau`; it does not erase the earlier preparation cost.

Physical transfer remains conditional on one common self-adjoint species/statistics Hamiltonian, metric and reference; receiving maps with motion/asymptotics; retained or bounded complement couplings; field, recoil, electrons, gates and counterterms at every endpoint; and an independently declared scale/unit law. Physical binding further needs a source upper and full competing-channel lower for that same Hamiltonian. No profile, isotope endpoint, radius, physical tau or binding value is selected by this audit. Director approval remains false.
