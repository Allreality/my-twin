"""Create TRG Deadlines and TRG Meetings calendars.

Run after oauth_setup.py succeeds. Writes calendar IDs into config.py.

Usage:
    python scripts/create_calendars.py
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from config import TOKEN_FILE, SCOPES, BASE_DIR


CALENDARS_TO_CREATE = [
    {
        "summary": "TRG Deadlines",
        "description": "Hard deadlines: patent dates, filing deadlines, RSVPs.",
        "timeZone": "America/New_York",
        "config_var": "CALENDAR_DEADLINES_ID",
    },
    {
        "summary": "TRG Meetings",
        "description": "Scheduled events: calls, meetings, appointments.",
        "timeZone": "America/New_York",
        "config_var": "CALENDAR_MEETINGS_ID",
    },
]


def find_existing(service, summary: str) -> str | None:
    """Return calendar ID if a calendar with this summary already exists."""
    page_token = None
    while True:
        result = service.calendarList().list(pageToken=page_token).execute()
        for cal in result.get("items", []):
            if cal.get("summary") == summary:
                return cal["id"]
        page_token = result.get("nextPageToken")
        if not page_token:
            return None


def update_config(var_name: str, calendar_id: str):
    """Patch config.py with the calendar ID."""
    config_path = BASE_DIR / "config.py"
    text = config_path.read_text()
    pattern = rf'^{var_name}\s*=\s*"[^"]*"'
    replacement = f'{var_name} = "{calendar_id}"'
    new_text, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count == 0:
        print(f"WARN: could not find {var_name} in config.py — set manually:")
        print(f"  {var_name} = \"{calendar_id}\"")
        return
    config_path.write_text(new_text)
    print(f"  config.py updated: {var_name} = {calendar_id}")


def main():
    if not TOKEN_FILE.exists():
        print("ERROR: token.json not found. Run oauth_setup.py first.")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    service = build("calendar", "v3", credentials=creds)

    for cal_spec in CALENDARS_TO_CREATE:
        summary = cal_spec["summary"]
        existing_id = find_existing(service, summary)
        if existing_id:
            print(f"Calendar exists: {summary} ({existing_id})")
            calendar_id = existing_id
        else:
            body = {k: v for k, v in cal_spec.items() if k != "config_var"}
            created = service.calendars().insert(body=body).execute()
            calendar_id = created["id"]
            print(f"Created: {summary} ({calendar_id})")

        update_config(cal_spec["config_var"], calendar_id)

    print("\nDone. Both calendars ready.")


if __name__ == "__main__":
    main()
