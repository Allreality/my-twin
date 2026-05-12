# GCP Setup — Calendar Agent

One-time setup. ~15 minutes. Do this before running `oauth_setup.py`.

You'll create a Google Cloud project, enable two APIs (Gmail + Calendar), configure
the OAuth consent screen, **publish the app** (counterintuitive but required for
long-lived refresh tokens), and download a `credentials.json` file.

---

## Step 1 — Create the GCP project

1. Go to https://console.cloud.google.com/
2. Sign in as **midnight.trg@gmail.com**
3. Top bar → project dropdown → **New Project**
4. Project name: `midnight-trg-calendar`
5. Organization: (leave as "No organization" unless you have a Workspace)
6. Click **Create**
7. Wait ~30 seconds, then select the new project from the dropdown

---

## Step 2 — Enable Gmail API + Calendar API

1. Left sidebar → **APIs & Services** → **Library**
2. Search "Gmail API" → click → **Enable**
3. Back to Library, search "Google Calendar API" → click → **Enable**

Both should show "API enabled" with a green check.

---

## Step 3 — Configure OAuth consent screen

1. Left sidebar → **APIs & Services** → **OAuth consent screen**
2. User type: **External** → Create
3. App information:
   - App name: `TRG Calendar Agent`
   - User support email: `midnight.trg@gmail.com`
   - App logo: skip
4. App domain: skip everything optional
5. Developer contact: `midnight.trg@gmail.com`
6. Click **Save and Continue**

### Scopes screen
1. Click **Add or Remove Scopes**
2. Search and check these three scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/calendar.events`
   - `https://www.googleapis.com/auth/calendar` (needed in Step 7 to create the two new calendars; can be removed after if you want stricter scope hygiene — see "Optional: scope tightening" at the bottom)
3. **Update** → **Save and Continue**

### Test users screen
1. Click **Add Users**
2. Add `midnight.trg@gmail.com`
3. **Save and Continue**

### Summary
1. Review → **Back to Dashboard**

---

## Step 4 — PUBLISH THE APP (do not skip)

This step is counterintuitive but critical for a cron-deployed agent.

**Why this matters:** by default, Google sets your app to "Testing" status.
In Testing status, OAuth refresh tokens expire after 7 days — meaning the
calendar agent on VPSBG would stop working every Monday until you re-OAuth.
That's operationally untenable for a 15-minute polling cron.

Publishing the app (without submitting for verification) keeps the agent in
"Published, Unverified" state. Refresh tokens persist indefinitely. The
"unverified app" warning still appears when *anyone* tries to use it — but
since nobody else has your credentials, that's irrelevant.

**Steps:**
1. Still on the **OAuth consent screen** page
2. Find the **Publishing status** section near the top
3. Click **PUBLISH APP**
4. Confirmation dialog warns "Your app will be available to any user with a Google Account" — click **Confirm**

After publishing, status changes from "Testing" → "In production". This does
NOT mean Google has verified your app. It means refresh tokens won't expire.

**You will NOT submit for Google verification.** Verification requires a
homepage URL, privacy policy URL, demo video, and ~4–6 weeks of review.
None of that applies to a personal-use cron agent. You're staying in
"Published, Unverified" indefinitely.

---

## Step 5 — Create OAuth client credentials

1. Left sidebar → **APIs & Services** → **Credentials**
2. **+ Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `calendar-agent-cli`
5. **Create**
6. Popup shows Client ID and Secret → click **Download JSON**
7. Save the downloaded file as `credentials.json`

**File goes here (DO NOT commit to git):**
```
/mnt/c/projects/twin/agents/calendar_agent/secrets/credentials.json
```

`.gitignore` is already set up to exclude `secrets/`.

---

## Step 6 — Verify credentials file

```bash
ls -la /mnt/c/projects/twin/agents/calendar_agent/secrets/credentials.json
cat /mnt/c/projects/twin/agents/calendar_agent/secrets/credentials.json | python -m json.tool
chmod 600 /mnt/c/projects/twin/agents/calendar_agent/secrets/credentials.json
```

Should show valid JSON with `client_id`, `client_secret`, `auth_uri`, `token_uri`.

The `chmod 600` enforces user-read-write only — this file is effectively a
password for your Google account, treat it like one.

---

## Step 7 — Run the OAuth flow

```bash
cd /mnt/c/projects/twin/agents/calendar_agent
source ../../venv/bin/activate
python scripts/oauth_setup.py
```

What happens:
1. Script opens your browser
2. Sign in as midnight.trg@gmail.com
3. You'll see "Google hasn't verified this app" — click **Advanced** → **Go to TRG Calendar Agent (unsafe)**
   (This warning is normal and expected for unverified apps. You're authorizing
   your own app with your own credentials.)
4. Grant the three scopes
5. Browser shows "The authentication flow has completed"
6. Script writes `secrets/token.json` (the refresh token)
7. Set restrictive permissions: `chmod 600 secrets/token.json`

Done. Token refreshes automatically from this point forward — and because the
app is Published, the refresh token will not expire after 7 days.

---

## Step 8 — Create the two calendars

```bash
python scripts/create_calendars.py
```

This creates:
- **TRG Deadlines** — for hard deadlines (patent dates, filing deadlines, RSVPs)
- **TRG Meetings** — for scheduled events (calls, meetings, appointments)

Calendar IDs are written to `config.py` automatically.

**Important:** `config.py` should be committed to git (calendar IDs are opaque
identifiers, not secrets). Verify it's NOT in `.gitignore` before committing.

---

## Step 9 — Deploy to VPSBG (later, not now)

After Phase 1 is validated locally, transfer credentials to VPSBG with
proper directory permissions:

```bash
ssh root@87.121.52.49
mkdir -p /home/calendar-agent/secrets
chmod 700 /home/calendar-agent/secrets
exit

scp secrets/credentials.json root@87.121.52.49:/home/calendar-agent/secrets/
scp secrets/token.json root@87.121.52.49:/home/calendar-agent/secrets/

ssh root@87.121.52.49 "chmod 600 /home/calendar-agent/secrets/*.json"
```

The refresh token works server-side — no need to re-OAuth on VPSBG.

---

## Optional: scope tightening (post-Step 8)

The `https://www.googleapis.com/auth/calendar` (full) scope is only needed to
*create* the two calendars in Step 8. After calendars exist, the agent only
needs `gmail.readonly` and `calendar.events` (which can read/write events on
existing calendars).

If you want tighter scope hygiene:

1. Go to **OAuth consent screen** → **Edit App** → **Scopes**
2. Remove `https://www.googleapis.com/auth/calendar`
3. Save
4. Re-run `oauth_setup.py` to get a new token with narrower scope
5. Replace the old `token.json`

For a personal-use agent on your own account, this is optional. For multi-user
or audit-sensitive deployments, it's recommended.

---

## Troubleshooting

**"Access blocked: TRG Calendar Agent has not completed Google verification"**
→ You're not in the test users list (only relevant if app is still in Testing
status — if you published in Step 4, this shouldn't happen). Go back to OAuth
consent screen → Test users → add midnight.trg@gmail.com.

**"redirect_uri_mismatch"**
→ You picked "Web application" instead of "Desktop app" for the OAuth client.
Delete it, recreate as Desktop app.

**Token expires unexpectedly**
→ App is still in "Testing" status. Refresh tokens for testing apps expire
after 7 days. Go to OAuth consent screen and click PUBLISH APP per Step 4.
Re-run `oauth_setup.py` after publishing to get a persistent refresh token.

**"This app is blocked" with no Advanced option**
→ You're signed in as a Google Workspace user with admin-blocked third-party
apps. Either sign in as a different account, or get a Workspace admin to
whitelist the OAuth client ID.

**Browser opens but immediately shows "Connection refused"**
→ Local port 8080 is in use (Flask service?). Stop the conflicting service or
specify a different port in `oauth_setup.py`:
```python
flow.run_local_server(port=8765)
```