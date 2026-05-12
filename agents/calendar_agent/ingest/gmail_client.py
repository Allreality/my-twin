"""Gmail API wrapper. Read-only operations.

list_unread() returns message IDs since last poll.
fetch_message(id) returns parsed Email object.
"""
import base64
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TOKEN_FILE, SCOPES, MAX_EMAILS_PER_POLL


@dataclass
class Email:
    """Minimal email representation for triage + extraction."""
    message_id: str
    thread_id: str
    sender: str
    sender_email: str
    subject: str
    date: datetime
    body_text: str
    snippet: str
    is_reply: bool

    def context_block(self) -> str:
        """Format for LLM context."""
        return (
            f"From: {self.sender}\n"
            f"Date: {self.date.isoformat()}\n"
            f"Subject: {self.subject}\n"
            f"---\n"
            f"{self.body_text[:4000]}"
        )


class GmailClient:
    def __init__(self):
        if not TOKEN_FILE.exists():
            raise FileNotFoundError(
                f"{TOKEN_FILE} not found. Run scripts/oauth_setup.py first."
            )
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        self.service = build("gmail", "v1", credentials=creds)

    def list_unread(self, after_message_id: Optional[str] = None) -> list[str]:
        """Return list of message IDs from unread inbox. Excludes already-processed."""
        query = "is:unread in:inbox"
        result = self.service.users().messages().list(
            userId="me",
            q=query,
            maxResults=MAX_EMAILS_PER_POLL,
        ).execute()
        messages = result.get("messages", [])
        return [m["id"] for m in messages]

    def fetch_message(self, message_id: str) -> Email:
        """Fetch and parse a single message."""
        msg = self.service.users().messages().get(
            userId="me", id=message_id, format="full"
        ).execute()

        headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
        subject = headers.get("subject", "(no subject)")
        from_raw = headers.get("from", "")
        sender_email = self._extract_email(from_raw)
        sender_name = self._extract_name(from_raw) or sender_email
        date_raw = headers.get("date", "")
        try:
            date = parsedate_to_datetime(date_raw)
        except (TypeError, ValueError):
            date = datetime.now()

        body = self._extract_body(msg["payload"])
        is_reply = subject.lower().startswith(("re:", "fwd:", "fw:"))

        return Email(
            message_id=msg["id"],
            thread_id=msg["threadId"],
            sender=sender_name,
            sender_email=sender_email,
            subject=subject,
            date=date,
            body_text=body,
            snippet=msg.get("snippet", ""),
            is_reply=is_reply,
        )

    @staticmethod
    def _extract_email(from_field: str) -> str:
        """Pull email address from 'Name <addr@x.com>' or 'addr@x.com'."""
        if "<" in from_field and ">" in from_field:
            return from_field.split("<")[1].split(">")[0].strip().lower()
        return from_field.strip().lower()

    @staticmethod
    def _extract_name(from_field: str) -> Optional[str]:
        """Pull display name from 'Name <addr@x.com>'."""
        if "<" in from_field:
            name = from_field.split("<")[0].strip().strip('"')
            return name if name else None
        return None

    def _extract_body(self, payload: dict) -> str:
        """Recursively extract plain text body."""
        mime_type = payload.get("mimeType", "")

        if mime_type == "text/plain":
            data = payload.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

        if "parts" in payload:
            # Prefer text/plain; fall back to text/html stripped
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    body = self._extract_body(part)
                    if body:
                        return body
            for part in payload["parts"]:
                body = self._extract_body(part)
                if body:
                    return body

        if mime_type == "text/html":
            data = payload.get("body", {}).get("data", "")
            if data:
                html = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                return self._strip_html(html)

        return ""

    @staticmethod
    def _strip_html(html: str) -> str:
        """Crude HTML strip — good enough for triage. Replace with bs4 later if needed."""
        import re
        text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
