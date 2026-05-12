"""One-time OAuth setup. Run locally (not on VPSBG).

Requires browser. Writes secrets/token.json on success.

Usage:
    python scripts/oauth_setup.py
"""
import sys
from pathlib import Path

# Make config importable from scripts/
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from config import CREDENTIALS_FILE, TOKEN_FILE, SCOPES, SECRETS_DIR


def main():
    SECRETS_DIR.mkdir(exist_ok=True)

    if not CREDENTIALS_FILE.exists():
        print(f"ERROR: {CREDENTIALS_FILE} not found.")
        print("Download from GCP Console → APIs & Services → Credentials → OAuth client ID.")
        print("See GCP_SETUP.md Step 4.")
        sys.exit(1)

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow. Browser will open.")
            print("Sign in as midnight.trg@gmail.com.")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())
        print(f"Token saved to {TOKEN_FILE}")

    print("OAuth setup complete.")
    print(f"  Scopes granted: {len(SCOPES)}")
    for s in SCOPES:
        print(f"    - {s}")


if __name__ == "__main__":
    main()
