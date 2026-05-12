"""Triage heuristics — score emails before sending to LLM.

Goal: cut LLM calls by ~90% by filtering out newsletters, notifications,
and emails with no date-bearing content.

Score >= TRIAGE_SCORE_EXTRACT → send to LLM
Score >= TRIAGE_SCORE_FLAG → flag for manual review
Below → skip silently
"""
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ingest.gmail_client import Email


# Senders we always want to extract from (gov, certification bodies, advisors)
HIGH_SIGNAL_DOMAINS = {
    "uspto.gov",
    "sam.gov",
    "sba.gov",
    "mass.gov",
    "clarku.edu",
    "calendar-notification@google.com",
}

HIGH_SIGNAL_KEYWORDS_SUBJECT = [
    "deadline", "due", "rsvp", "meeting", "call", "appointment",
    "scheduled", "reminder", "expires", "filing", "submission",
    "interview", "review", "follow up", "follow-up", "confirm",
]

# Senders/patterns we want to skip
SKIP_DOMAINS = {
    "noreply@github.com", "notifications@github.com",
    "no-reply@accounts.google.com",
    "newsletter@", "marketing@", "promo@", "deals@",
}

SKIP_KEYWORDS_SUBJECT = [
    "newsletter", "digest", "unsubscribe", "% off", "sale",
    "shipping confirmation", "order confirmation", "receipt",
]

# Date patterns — broad regex catches most natural mentions
DATE_PATTERNS = [
    # ISO and slash dates
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    # Month name + day
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?\s+\d{1,2}",
    # "by Friday", "next Tuesday"
    r"\b(by|on|next|this)\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(day)?\b",
    # Time mentions
    r"\b\d{1,2}:\d{2}\s*(am|pm|AM|PM)?\b",
    r"\b\d{1,2}\s*(am|pm|AM|PM)\b",
    # Relative dates
    r"\b(tomorrow|today|tonight|yesterday)\b",
    r"\b(next week|this week|next month|in \d+ days?|in \d+ weeks?)\b",
]
DATE_REGEX = re.compile("|".join(DATE_PATTERNS), re.IGNORECASE)


@dataclass
class TriageResult:
    score: int
    decision: str  # "extract" | "flag" | "skip"
    reasons: list[str]


def score_email(email: "Email") -> TriageResult:
    """Score an email. Higher = more likely to contain a deadline/event."""
    score = 0
    reasons = []

    sender_lower = email.sender_email.lower()
    subject_lower = email.subject.lower()
    body_sample = email.body_text[:2000].lower()

    # --- Hard skip signals ---
    for skip in SKIP_DOMAINS:
        if skip in sender_lower:
            return TriageResult(score=-10, decision="skip", reasons=[f"skip-domain:{skip}"])

    for kw in SKIP_KEYWORDS_SUBJECT:
        if kw in subject_lower:
            return TriageResult(score=-5, decision="skip", reasons=[f"skip-subject:{kw}"])

    # Likely marketing if List-Unsubscribe equivalent in body
    if "unsubscribe" in body_sample and len(body_sample) < 1500:
        return TriageResult(score=-5, decision="skip", reasons=["likely-marketing"])

    # --- Positive signals ---
    for domain in HIGH_SIGNAL_DOMAINS:
        if domain in sender_lower:
            score += 3
            reasons.append(f"high-signal-sender:{domain}")
            break

    for kw in HIGH_SIGNAL_KEYWORDS_SUBJECT:
        if kw in subject_lower:
            score += 2
            reasons.append(f"keyword-subject:{kw}")
            break  # one keyword is enough

    if email.is_reply:
        score += 1
        reasons.append("is-reply")

    # Date pattern in subject
    if DATE_REGEX.search(email.subject):
        score += 2
        reasons.append("date-in-subject")

    # Date patterns in body — count distinct matches
    body_dates = DATE_REGEX.findall(body_sample)
    if len(body_dates) >= 1:
        score += 1
        reasons.append(f"date-in-body:{len(body_dates)}")
    if len(body_dates) >= 3:
        score += 1
        reasons.append("multiple-date-mentions")

    # Calendar invite (.ics) — explicit signal
    if "begin:vcalendar" in body_sample or "calendar invitation" in body_sample:
        score += 4
        reasons.append("calendar-invite-detected")

    # Decide
    from config import TRIAGE_SCORE_EXTRACT, TRIAGE_SCORE_FLAG
    if score >= TRIAGE_SCORE_EXTRACT:
        decision = "extract"
    elif score >= TRIAGE_SCORE_FLAG:
        decision = "flag"
    else:
        decision = "skip"

    return TriageResult(score=score, decision=decision, reasons=reasons)
