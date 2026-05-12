"""Synthetic email fixtures for Phase 1 testing.

Each fixture mimics the Email dataclass so we can test the full pipeline
without hitting Gmail API.
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class FixtureEmail:
    """Mirror of ingest.gmail_client.Email for offline testing."""
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
        return (
            f"From: {self.sender}\n"
            f"Date: {self.date.isoformat()}\n"
            f"Subject: {self.subject}\n"
            f"---\n"
            f"{self.body_text[:4000]}"
        )


FIXTURES = [
    # 1. SBDC reply with potential follow-up
    FixtureEmail(
        message_id="fix-001",
        thread_id="t-001",
        sender="Sarah Doran",
        sender_email="sadoran@clarku.edu",
        subject="Re: Pre-formation LLC structural review for SBA 8(a) path",
        date=datetime(2026, 5, 8, 10, 30),
        body_text=(
            "Hi Akil,\n\n"
            "Thanks for the detailed background. I'd like to schedule a call to "
            "walk through your structural questions. Are you available Tuesday May 12 "
            "at 2:00 PM Eastern? The call should take about 45 minutes.\n\n"
            "Before we meet, please complete client intake at msbdc.org/register and "
            "send me a draft of your proposed operating agreement language.\n\n"
            "Best,\nSarah Doran\nOperations Manager, Clark SBDC"
        ),
        snippet="Thanks for the detailed background...",
        is_reply=True,
    ),
    # 2. USPTO patent deadline reminder
    FixtureEmail(
        message_id="fix-002",
        thread_id="t-002",
        sender="USPTO Notifications",
        sender_email="notifications@uspto.gov",
        subject="REMINDER: Non-provisional deadline for Patent Application 63/917,456",
        date=datetime(2026, 5, 7, 9, 0),
        body_text=(
            "This is a reminder that your provisional patent application 63/917,456 "
            "(Hardware-Enforced Compliance Architecture) requires a non-provisional "
            "filing by November 14, 2026 to maintain priority date. Failure to file "
            "by this date will result in loss of priority.\n\n"
            "USPTO Patent Office"
        ),
        snippet="This is a reminder that your provisional patent application...",
        is_reply=False,
    ),
    # 3. Newsletter — should be skipped
    FixtureEmail(
        message_id="fix-003",
        thread_id="t-003",
        sender="TechCrunch Daily",
        sender_email="newsletter@techcrunch.com",
        subject="Today's tech news digest — May 7",
        date=datetime(2026, 5, 7, 6, 0),
        body_text=(
            "Top stories today: AI funding hits new highs, startup X raises $50M. "
            "Read more on TechCrunch.com. Unsubscribe from this newsletter."
        ),
        snippet="Top stories today...",
        is_reply=False,
    ),
    # 4. Calendar invite (.ics)
    FixtureEmail(
        message_id="fix-004",
        thread_id="t-004",
        sender="Kevin Kuros",
        sender_email="kevin.j.kuros@mass.gov",
        subject="Invitation: MOBD intro call @ Friday May 9, 11:00 AM",
        date=datetime(2026, 5, 7, 14, 30),
        body_text=(
            "You are invited to: MOBD Intro Call\n"
            "When: Friday, May 9, 2026, 11:00 AM - 11:30 AM Eastern\n"
            "Where: Phone — (617) 549-1803\n"
            "BEGIN:VCALENDAR\nBEGIN:VEVENT\nDTSTART:20260509T110000\nEND:VEVENT\nEND:VCALENDAR"
        ),
        snippet="You are invited to: MOBD Intro Call...",
        is_reply=False,
    ),
    # 5. SAM.gov status update — soft tickler
    FixtureEmail(
        message_id="fix-005",
        thread_id="t-005",
        sender="SAM.gov FSD",
        sender_email="fsd@sam.gov",
        subject="Update on case INC-GSAFSD20857720",
        date=datetime(2026, 5, 6, 16, 0),
        body_text=(
            "Your entity validation case is being reviewed. You can expect a "
            "response within 3-5 business days. Reference: INC-GSAFSD20857720."
        ),
        snippet="Your entity validation case is being reviewed...",
        is_reply=False,
    ),
    # 6. GitHub notification — should be skipped
    FixtureEmail(
        message_id="fix-006",
        thread_id="t-006",
        sender="GitHub",
        sender_email="notifications@github.com",
        subject="[Allreality/midnight-infrastructure] PR opened",
        date=datetime(2026, 5, 7, 11, 15),
        body_text="A new pull request was opened. View on GitHub.",
        snippet="A new pull request was opened...",
        is_reply=False,
    ),
    # 7. Ambiguous date — "next Tuesday"
    FixtureEmail(
        message_id="fix-007",
        thread_id="t-007",
        sender="Robert Jordan",
        sender_email="robert@example.com",
        subject="TAN DAO council sync next Tuesday",
        date=datetime(2026, 5, 7, 8, 0),
        body_text=(
            "Hey Akil — let's do the council sync next Tuesday at 7pm ET. "
            "I'll send the Solana treasury report ahead of time. Talk soon."
        ),
        snippet="Hey Akil — let's do the council sync...",
        is_reply=False,
    ),
    # 8. Multiple events in one email
    FixtureEmail(
        message_id="fix-008",
        thread_id="t-008",
        sender="Lindsey Systems Sales",
        sender_email="sales@lindsey-usa.com",
        subject="Demo scheduled + follow-up materials",
        date=datetime(2026, 5, 7, 13, 0),
        body_text=(
            "Hi Akil,\n\n"
            "Confirming our SIG hardware demo on Wednesday May 14, 2026 at 2:00 PM ET. "
            "After the demo, please submit your integration requirements doc by "
            "Friday May 23, 2026 so we can scope a pilot.\n\n"
            "Looking forward to the conversation."
        ),
        snippet="Confirming our SIG hardware demo...",
        is_reply=False,
    ),
    # 9. Marketing email — should be skipped
    FixtureEmail(
        message_id="fix-009",
        thread_id="t-009",
        sender="Some Vendor",
        sender_email="promo@vendor.com",
        subject="50% off this weekend only!",
        date=datetime(2026, 5, 7, 7, 0),
        body_text="Big sale this weekend. Click here to unsubscribe.",
        snippet="Big sale this weekend...",
        is_reply=False,
    ),
    # 10. Personal note with no date — should extract nothing
    FixtureEmail(
        message_id="fix-010",
        thread_id="t-010",
        sender="A Friend",
        sender_email="friend@gmail.com",
        subject="Saw this and thought of you",
        date=datetime(2026, 5, 7, 19, 0),
        body_text="Check out this article on Temne language preservation: https://example.com",
        snippet="Check out this article...",
        is_reply=False,
    ),
]
