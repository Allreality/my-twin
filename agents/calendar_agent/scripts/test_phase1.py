"""Phase 1 test driver.

Runs the full pipeline on synthetic fixtures:
  Email → triage → (extract or skip) → JSON output

Writes results to phase1_output.json for inspection.

Usage:
    python scripts/test_phase1.py [--no-llm]

--no-llm flag: triage only, skip extraction (useful before API key is set up)
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.fixtures.sample_emails import FIXTURES
from triage.heuristics import score_email
from extraction.deadline_parser import extract_events, ExtractionError


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-llm", action="store_true", help="Skip extraction stage")
    ap.add_argument("--output", default="phase1_output.json")
    args = ap.parse_args()

    results = []

    for email in FIXTURES:
        print(f"\n[{email.message_id}] {email.sender_email} — {email.subject[:60]}")

        triage = score_email(email)
        print(f"  Triage: score={triage.score} decision={triage.decision} reasons={triage.reasons}")

        record = {
            "message_id": email.message_id,
            "sender": email.sender_email,
            "subject": email.subject,
            "triage": {
                "score": triage.score,
                "decision": triage.decision,
                "reasons": triage.reasons,
            },
            "extraction": None,
        }

        if triage.decision == "extract" and not args.no_llm:
            try:
                t0 = time.time()
                result = extract_events(email)
                elapsed = time.time() - t0
                print(f"  Extraction: has_events={result.has_events} "
                      f"count={len(result.events)} ({elapsed:.1f}s)")
                for ev in result.events:
                    print(f"    → [{ev.event_type}] {ev.title} @ {ev.start_datetime} "
                          f"(conf={ev.confidence:.2f})")
                    if ev.ambiguity_notes:
                        print(f"      ambiguity: {ev.ambiguity_notes}")
                record["extraction"] = result.model_dump(mode="json")
                record["extraction_seconds"] = round(elapsed, 2)
            except ExtractionError as e:
                print(f"  EXTRACTION ERROR: {e}")
                record["extraction"] = {"error": str(e)}
        elif triage.decision == "extract":
            print("  (LLM skipped: --no-llm)")
        else:
            print(f"  (no extraction: triage said {triage.decision})")

        results.append(record)

    output_path = Path(args.output)
    output_path.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n\nResults written to {output_path}")

    # Summary
    extracted = sum(1 for r in results if r["triage"]["decision"] == "extract")
    flagged = sum(1 for r in results if r["triage"]["decision"] == "flag")
    skipped = sum(1 for r in results if r["triage"]["decision"] == "skip")
    print(f"\nSummary: {len(results)} emails | "
          f"{extracted} extracted | {flagged} flagged | {skipped} skipped")


if __name__ == "__main__":
    main()
