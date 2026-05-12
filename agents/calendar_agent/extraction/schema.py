"""Pydantic schemas for extraction output."""
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class ProposedEvent(BaseModel):
    """A single calendar event proposal extracted from an email."""
    event_type: Literal["deadline", "meeting", "tickler"] = Field(
        description="deadline = hard date (filing, RSVP, expiry); "
                    "meeting = scheduled gathering with time; "
                    "tickler = soft follow-up reminder ('expect reply in 3-5 days')"
    )
    title: str = Field(description="Short event title, < 80 chars")
    start_datetime: datetime = Field(description="Event start in ISO format with timezone")
    end_datetime: Optional[datetime] = Field(
        default=None,
        description="Event end. If omitted, defaults to +30min for meetings, all-day for deadlines"
    )
    is_all_day: bool = Field(default=False, description="True for deadline-style events")
    location: Optional[str] = Field(default=None)
    description: str = Field(description="Context for the event — who, why, what action needed")
    confidence: float = Field(ge=0.0, le=1.0, description="LLM confidence in extraction")
    ambiguity_notes: Optional[str] = Field(
        default=None,
        description="Anything the reviewer should double-check (vague dates, missing year, etc.)"
    )


class ExtractionResult(BaseModel):
    """Top-level result from one email — may contain 0, 1, or many proposed events."""
    has_events: bool
    events: list[ProposedEvent] = Field(default_factory=list)
    skip_reason: Optional[str] = Field(
        default=None,
        description="If has_events=False, why was nothing extracted"
    )
