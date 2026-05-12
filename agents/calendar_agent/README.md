# Calendar Agent — Phase 1

Email-to-calendar agent for midnight.trg@gmail.com. Extends Digital Twin.

Phase 1 scope: Gmail ingest → triage → LLM extraction → JSON output for review.
No calendar writes yet (Phase 3). No approval CLI yet (Phase 2).

---

## Architecture

```
Gmail (midnight.trg@gmail.com)
    ↓ poll (Phase 4)
gmail_client.py — fetch unread
    ↓
heuristics.py — score (skip/flag/extract)
    ↓ (only "extract" continues)
deadline_parser.py — Claude Haiku extraction
    ↓
ProposedEvent[] → JSON (Phase 1)
            → SQLite queue (Phase 2)
            → Google Calendar (Phase 3)
```

---

## Quickstart

### 1. Install deps
```bash
cd /mnt/c/projects/twin/agents/calendar_agent
source ../../venv/bin/activate
pip install -r requirements.txt
```

### 2. GCP setup (one-time)
Follow `GCP_SETUP.md` to create OAuth credentials. Save as `secrets/credentials.json`.

### 3. OAuth flow (one-time, local with browser)
```bash
python scripts/oauth_setup.py
```
Writes `secrets/token.json`.

### 4. Create the two TRG calendars
```bash
python scripts/create_calendars.py
```
Updates `config.py` with calendar IDs.

### 5. Test the pipeline (no Gmail, no calendar writes)
```bash
# Triage only — no LLM cost
python scripts/test_phase1.py --no-llm

# Full pipeline with LLM extraction (uses ANTHROPIC_API_KEY from midnight .env)
python scripts/test_phase1.py
```

Output goes to `phase1_output.json`.

---

## File structure

```
calendar_agent/
├── GCP_SETUP.md             — One-time Google Cloud setup
├── README.md                — This file
├── requirements.txt
├── .gitignore               — Excludes secrets/, state, db, logs
├── config.py                — Paths, scopes, model selection, calendar IDs
├── ingest/
│   ├── gmail_client.py      — Gmail API wrapper, Email dataclass
│   └── state.py             — Processed-message dedup
├── triage/
│   └── heuristics.py        — Pre-LLM scoring (skip/flag/extract)
├── extraction/
│   ├── schema.py            — ProposedEvent + ExtractionResult pydantic models
│   ├── prompts.py           — System + user prompt templates
│   └── deadline_parser.py   — Claude Haiku call
├── gcal/                    — (Phase 3) Calendar write — empty
├── memory/                  — (Phase 3) ChromaDB writer — empty
├── proposal/                — (Phase 2) Approval queue — empty
├── tests/
│   └── fixtures/
│       └── sample_emails.py — 10 synthetic test emails
└── scripts/
    ├── oauth_setup.py       — One-time OAuth (run locally)
    ├── create_calendars.py  — Create TRG Deadlines + TRG Meetings
    └── test_phase1.py       — Run full pipeline on fixtures
```

---

## Phase 1 validation results (on fixtures)

```
10 emails | 5 extracted | 1 flagged | 4 skipped

✓ SBDC reply, USPTO deadline, Kevin Kuros invite, SAM.gov, Lindsey demo → extract
✓ TechCrunch, GitHub, promo, friend with no date → skip
⚠ TAN DAO sync (unknown sender) → flag (will improve in Phase 2 with sender learning)
```

---

## What's NOT in Phase 1

- Real Gmail polling (we have the client, no scheduler yet)
- Calendar writes
- Approval CLI
- ChromaDB integration
- Cron deployment to VPSBG

Each is a separate phase. Phase 1 proves the brain works before we wire it to your inbox.

---

## Tuning

If extraction quality is off, adjust in this order:
1. `triage/heuristics.py` — too many false negatives → lower `TRIAGE_SCORE_FLAG`
2. `extraction/prompts.py` — wrong dates / missed events → tighten system prompt
3. `extraction/schema.py` — missing fields → add and re-prompt
4. `tests/fixtures/sample_emails.py` — add real emails (sanitized) to regression set

---

## Costs

At ~50 extracted emails/day on Haiku ($1/MTok input, $5/MTok output):
- Avg input: ~1500 tokens × 50 = 75K tokens/day = $0.075
- Avg output: ~300 tokens × 50 = 15K tokens/day = $0.075
- **Roughly $0.15/day, $4.50/month**

If volume spikes or extraction quality issues appear, switch model in `config.py`:
```python
EXTRACTION_MODEL = "claude-sonnet-4-6"  # ~5x cost, higher accuracy
```
