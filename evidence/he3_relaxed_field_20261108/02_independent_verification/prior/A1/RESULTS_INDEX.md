# A1 completed result index

Start with [RESEARCH_REPORT.md](RESEARCH_REPORT.md). It consolidates all four questions, completed mathematical results and precise remaining inputs. The original [README.md](README.md), [TARGET.md](TARGET.md) and [BRIEF.md](BRIEF.md) preserve the launch preparation.

| Item | Path |
| --- | --- |
| D/C preparation algebra, colour/current maps | [ONE report](peers/ONE/REPORT.md), [operation/source map](peers/ONE/NATIVE_SOURCE_OPERATION_MAP.json) |
| Full192 complement, ground/memory and payment | [TWO report](peers/TWO/REPORT.md), [operation/source map](peers/TWO/SOURCE_OPERATION_MAP.json) |
| Complete Li-6 phase/reference and incidence | [THREE report](peers/THREE/REPORT.md), [receipt index](peers/THREE/NATIVE_RECEIPTS.json) |
| Event/frame/action and positive Write implementations | [FOUR report](peers/FOUR/REPORT.md), [receipt index](peers/FOUR/NATIVE_RECEIPTS.json) |
| Actual menu capability use | [EXECUTION_SUMMARY.md](EXECUTION_SUMMARY.md), [complete JSON inventory](EXECUTION_SUMMARY.json) |
| Completion checks | [COMPLETION_CHECK.json](COMPLETION_CHECK.json), [read-only verifier](host/verify_completed_run.py) |
| Clock and process/retention outcome | [NATIVE_CLOCK_CHECK.json](NATIVE_CLOCK_CHECK.json), [ORCHESTRATION_RESULT.json](ORCHESTRATION_RESULT.json) |
| Full native ledger and finalization | [OUTCOME_LEDGER.json](native_run/OUTCOME_LEDGER.json), [COMPLETE.json](native_run/COMPLETE.json) |
| Resource release/helper readback | [RESOURCE_RELEASE.json](native_run/RESOURCE_RELEASE.json), [HELPER_READBACK.json](native_run/HELPER_READBACK.json) |
| Full byte-checked native/helper copies | [FINAL_DATA_CUSTODY.json](FINAL_DATA_CUSTODY.json); native_run/ and helper_final_state/ |
| All four source/menu attestations | [READING_GATE_COMPLETE.json](READING_GATE_COMPLETE.json); host/reading_snapshots/ |
| Source inputs and runtime validation | [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json), [VERIFY_AFTER.json](VERIFY_AFTER.json) |
| Admitted program/source hashes and additional owning records | [ADMITTED_PROGRAM_SOURCE_INDEX.json](ADMITTED_PROGRAM_SOURCE_INDEX.json), [ADDITIONAL_SOURCE_CUSTODY.json](ADDITIONAL_SOURCE_CUSTODY.json) |
| Operational corrections and review scope | [RUN_NOTES.md](RUN_NOTES.md) |

All peer folders retain their complete generated operands, immutable tasks, notes, outboxes, failures, report, FINAL_STATUS.json, DONE and process output. Original qualified-runtime trees remain at the paths in SETUP.json. The raw native/header records retain their historical execution strings and exact original paths; the consolidated report states what actually ran in this campaign.

Run the read-only custody check on the original machine with:

```bash
python3 -B host/verify_completed_run.py
```

This checks timing, source preservation and all native/helper file copies. It does not rerun mathematical kernels. The final archive's readback/checksum receipt is delivered beside the archive.

After extracting the evidence archive on another machine, `python3 -B host/verify_archive_contents.py` checks its complete file manifest without access to the original runtime.
