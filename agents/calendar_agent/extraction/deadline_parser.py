"""Deadline/event extraction via Anthropic Claude.

Uses claude-haiku-4-5 for cost — extraction is well-defined enough that Haiku handles it.
Returns ExtractionResult or raises on hard failures (API errors, malformed JSON).
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import anthropic
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import ANTHROPIC_API_KEY, EXTRACTION_MODEL, EXTRACTION_MAX_TOKENS, USER_TIMEZONE
from extraction.schema import ExtractionResult
from extraction.prompts import SYSTEM_PROMPT, build_user_message

if TYPE_CHECKING:
    from ingest.gmail_client import Email


class ExtractionError(Exception):
    pass


_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        if not ANTHROPIC_API_KEY:
            raise ExtractionError(
                "ANTHROPIC_API_KEY not set. Check midnight-infrastructure/.env"
            )
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def extract_events(email: "Email") -> ExtractionResult:
    """Run extraction on a single email. Raises ExtractionError on failure."""
    client = get_client()
    today_iso = datetime.now().strftime("%Y-%m-%d (%A)")

    try:
        response = client.messages.create(
            model=EXTRACTION_MODEL,
            max_tokens=EXTRACTION_MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": build_user_message(email.context_block(), today_iso)}
            ],
        )
    except anthropic.APIError as e:
        raise ExtractionError(f"Anthropic API error: {e}") from e

    raw_text = "".join(
        block.text for block in response.content if hasattr(block, "text")
    ).strip()

    # Strip ```json fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ExtractionError(
            f"LLM returned invalid JSON: {e}\nRaw output:\n{raw_text[:500]}"
        ) from e

    try:
        result = ExtractionResult.model_validate(parsed)
    except ValidationError as e:
        raise ExtractionError(
            f"LLM output failed schema validation: {e}\nParsed:\n{json.dumps(parsed, indent=2, default=str)[:500]}"
        ) from e

    return result
