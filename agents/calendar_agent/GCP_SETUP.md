# GCP Setup — Calendar Agent

One-time setup. ~15 minutes (longer if WSL networking needs configuration). Do this before running `oauth_setup.py`.

You'll create a Google Cloud project, enable two APIs (Gmail + Calendar), configure
the OAuth consent screen, **publish the app** (counterintuitive but required for
long-lived refresh tokens), and download a `credentials.json` file.

**WSL users:** scroll to "WSL prerequisite" before starting. The OAuth flow
fails without mirrored networking enabled.

---

## WSL prerequisite — mirrored networking (one-time, do first)

If you're running this from WSL (any Linux distro on Windows), the OAuth
callback flow will fail because Windows browser cannot reach WSL's localhost
on the random port Python opens. Symptom: browser shows "This site can't be
reached" or `ERR_CONNECTION_TIMED_OUT` after clicking Allow.

**Fix:** enable WSL2 mirrored networking. Requires WSL 2.0+ on Windows 11 22H2+.

Check WSL version:
```bash
wsl.exe --version
```

If `WSL version: 2.0.0` or higher, proceed. Otherwise update WSL via
`wsl.exe --update` from PowerShell.

Find your Windows username from inside WSL:
```bash
cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r\n'
```

Create `.wslconfig` on the Windows side (heredoc syntax, replace `<USERNAME>`
with the value from above):
```bash
cat > "/mnt/c/Users/<USERNAME>/.wslconfig" << 'EOF'
[wsl2]
networkingMode=mirrored

[experimental]
hostAddressLoopback=true
EOF
```

Verify the file wrote:
```bash
cat "/mnt/c/Users/<USERNAME>/.wslconfig"
```

Then from **PowerShell** (not WSL — you cannot shut yourself down):
```powershell
wsl --shutdown
```

Wait ~10 seconds. Reopen WSL. Your `[boot]` section in `/etc/wsl.conf` runs
again (trading bot, selfheal, etc. all restart automatically).

Verify mirrored mode is active:
```bash
ip addr show eth0 | grep inet | head -2
```

In mirrored mode, eth0 has your real LAN IP (e.g., 192.168.x.x), not a
WSL-internal 172.x.x.x address.

This is a one-time setup. Fixes OAuth callbacks for every future tool, not
just this agent. If you've already done this, skip to Step 1.

---

## Step 1 — Create the GCP project

1. Go to https://console.cloud.google.com/
2. Sign in as **midnight.trg@gmail.com**
3. You may see a "Try Google Cloud for free" trial pitch with payment fields.
   **DO NOT enter payment info.** Close that flow and go directly to:
   https://console.cloud.google.com/projectcreate
4. Project name: `midnight-trg-calendar`
5. Organization: leave as "No organization"
6. Location: leave as default
7. Click **CREATE**
8. Wait ~30 seconds. Confirm top bar shows `midnight-trg-calendar` as
   active project before continuing.

The Gmail and Calendar APIs run in the GCP always-free tier. You will never
need billing for this project.

---

## Step 2 — Enable Gmail API + Calendar API

1. Left sidebar → **APIs & Services** → **Library**
   (or direct: `https://console.cloud.google.com/apis/library?project=midnight-trg-calendar`)
2. Search "Gmail API" → click → **Enable**
3. Back to Library, search "Google Calendar API" → click → **Enable**

Both should show "API enabled" with a green check. Verify in
**APIs & Services → Enabled APIs & services** — scroll past the GCP defaults
(BigQuery, Cloud Storage, Cloud Logging, etc.) to find your two.

---

## Step 3 — Configure OAuth consent screen

**Note:** Google migrated this UI to the "Google Auth Platform" in 2025. The
left sidebar now splits the old single page into: Branding, Audience, Clients,
Data Access, Verification Center, Settings. The decisions are the same; the
layout is different.

1. Left sidebar → **OAuth consent screen** (lands you in the Auth Platform)
2. You'll see a multi-step form with **App Information**, **Audience**,
   **Contact Information**, **Finish**
3. App information:
   - App name: `TRG Calendar Agent`
   - User support email: `midnight.trg@gmail.com`
4. Audience: **External**
5. Contact information: `midnight.trg@gmail.com`
6. Finish → **Create**

You'll land on the Google Auth Platform Overview with a green
"OAuth configuration created!" toast.

---

## Step 4 — Add scopes (Data Access page)

1. Left sidebar → **Data Access**
2. Click **Add or Remove Scopes**
3. The scope picker opens. **Don't use the filter table** — it's slow and
   the scopes you need don't always surface cleanly. Scroll past it to the
   **Manually add scopes** textbox at the bottom
4. Paste all three scope strings (one per line):
   ```
   https://www.googleapis.com/auth/gmail.readonly
   https://www.googleapis.com/auth/calendar.events
   https://www.googleapis.com/auth/calendar
   ```
5. Click **Add to table**
6. Three scopes appear in the upper table with checkboxes ticked
7. Click **Update** at the bottom of the scope picker panel
8. Back on the Data Access page, click **Save** to persist

You should see:
- **Sensitive scopes:** `calendar`, `calendar.events`
- **Restricted scopes:** `gmail.readonly`

The Sensitive/Restricted classifications are how Google tracks data exposure.
They affect verification requirements *for verified apps*. Since you're
staying in "Published, Unverified" mode, the classification is informational.

The `calendar` (full) scope is only needed for `create_calendars.py` in
Step 9. You can narrow scope after — see "Optional: scope tightening" at
the bottom.

---

## Step 5 — PUBLISH THE APP (do not skip)

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
1. Left sidebar → **Audience**
2. Find the **Publishing status** section (top of page)
3. Click **PUBLISH APP**
4. Confirmation dialog warns "Your app will be available to any user with a
   Google Account" → click **Confirm**

Status changes from "Testing" → "In production". A gold "Your app requires
verification" banner will appear and stay there forever — that's normal and
irrelevant for personal use. **Ignore it.** Do not click "Go to verification
center."

**You will NOT submit for Google verification.** Verification requires a
homepage URL, privacy policy URL, demo video, and ~4–6 weeks of review.
None of that applies to a personal-use cron agent.

**Test users are no longer relevant** once published. The Audience page may
or may not show a "Test users" section in the new UI; if it does, it's a
fallback that only applies if you ever click "Back to testing" (don't).

---

## Step 6 — Create OAuth client credentials

1. Left sidebar → **Clients**
2. Click **+ Create client** (or **+ Create Credentials** → **OAuth client ID**
   in older UI)
3. Application type: **Desktop app** ← critical, not "Web application"
4. Name: `calendar-agent-cli`
5. Click **Create**
6. Popup shows Client ID and Secret → click **Download JSON**

**Why Desktop app, not Web application:**

| Type | OAuth callback handling |
|------|-------------------------|
| Web application | Requires registering exact callback URLs (e.g., `https://yourapp.com/callback`) |
| **Desktop app** | Uses `http://localhost:PORT` automatically — perfect for local Python scripts |

If you accidentally pick Web application, you'll get `redirect_uri_mismatch`
errors at OAuth time. Delete the client and recreate as Desktop app.

The JSON file downloads to `/mnt/c/Users/<USERNAME>/Downloads/` with an
auto-generated name like `client_secret_xxxxxx-yyyyyy.apps.googleusercontent.com.json`.

---

## Step 7 — Place credentials securely

```bash
cd /mnt/c/projects/twin/agents/calendar_agent/secrets/
mv /mnt/c/Users/<USERNAME>/Downloads/client_secret_*.json credentials.json
chmod 600 credentials.json
```

Replace `<USERNAME>` with your Windows username (find via
`cmd.exe /c "echo %USERNAME%"` from WSL).

Verify:
```bash
ls -la credentials.json
cat credentials.json | python -m json.tool | head -5
```

The top-level key must be **`installed`** (not `web`). If it shows `web`,
you picked the wrong client type — go back to Step 6 and recreate.

**WSL `chmod` caveat:** WSL on `/mnt/c/` mounts of NTFS filesystems sometimes
ignores chmod by default. If after `chmod 600` you still see `-rwxrwxrwx`,
that's WSL display behavior — Windows NTFS ACLs are protecting the file
based on your Windows user account. Not a real problem for personal use.

`.gitignore` should already exclude `secrets/` — verify with:
```bash
cat /mnt/c/projects/twin/agents/calendar_agent/.gitignore
```

Should contain `secrets/` on its own line.

---

## Step 8 — Run the OAuth flow (WSL)

```bash
cd /mnt/c/projects/twin/agents/calendar_agent
source ../../venv/bin/activate
python scripts/oauth_setup.py
```

**WSL behavior:** `xdg-open` will fail with a long list of
"x-www-browser: not found", "firefox: not found", etc. This is **expected
and harmless** — WSL has no Linux browser installed. The script handles this
by printing the URL for you to paste into your Windows browser manually.

**What you should see:**
```
======================================================================
Starting OAuth flow.
Listener bound to 0.0.0.0:8765 (WSL-compatible).

STEPS:
  1. Copy the URL below into your Windows browser.
  2. Sign in as midnight.trg@gmail.com.
  3. Click 'Advanced' -> 'Go to TRG Calendar Agent (unsafe)'.
  4. Click 'Allow' for the requested scopes.
  5. Browser redirects to localhost:8765 - wait for
     'authentication flow has completed' to appear.
======================================================================

Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?response_type=code&...
```

**Then:**
1. Carefully select the entire URL starting with `https://` and ending with
   `=offline` (or wherever the URL ends). The URL wraps across multiple
   terminal lines — copy the WHOLE thing.
2. Paste into your Windows browser. **No leading quote** — if your paste
   has a `'` at the start, Chrome treats the URL as a search query and
   sends it to Google Search instead of navigating to it.
3. Sign in as midnight.trg@gmail.com
4. "Google hasn't verified this app" → **Advanced** → **Go to TRG Calendar
   Agent (unsafe)**
5. Consent screen shows three scopes → click **Allow**
6. Browser redirects to `localhost:8765` (or whatever port the script
   chose) and shows: **"The authentication flow has completed. You may
   close this window."**
7. Switch back to WSL terminal. Script prints:
   ```
   Token saved to /mnt/c/projects/twin/agents/calendar_agent/secrets/token.json
   OAuth setup complete.
     Scopes granted: 3
       - https://www.googleapis.com/auth/gmail.readonly
       - https://www.googleapis.com/auth/calendar
       - https://www.googleapis.com/auth/calendar.events
   ```

If the script hangs after you click Allow (browser shows "site can't be
reached"), mirrored networking didn't take effect. Verify with
`ip addr show eth0`. The eth0 IP must match your Windows network.

---

## Step 9 — Create the two calendars

```bash
python scripts/create_calendars.py
```

This creates:
- **TRG Deadlines** — for hard deadlines (patent dates, filing deadlines, RSVPs)
- **TRG Meetings** — for scheduled events (calls, meetings, appointments)

Calendar IDs are written to `config.py` automatically.

**Important:** `config.py` should be committed to git (calendar IDs are opaque
identifiers, not secrets). Verify it's NOT in `.gitignore` before committing.

Verify in browser at `https://calendar.google.com` — left sidebar should
show "TRG Deadlines" and "TRG Meetings" as new calendars.

---

## Step 10 — Deploy to VPSBG (later, not now)

After Phase 1 is validated locally and Phase 2/3 are built, transfer
credentials to VPSBG with proper directory permissions:

```bash
ssh root@87.121.52.49
mkdir -p /home/calendar-agent/secrets
chmod 700 /home/calendar-agent/secrets
exit

scp secrets/credentials.json root@87.121.52.49:/home/calendar-agent/secrets/
scp secrets/token.json root@87.121.52.49:/home/calendar-agent/secrets/

ssh root@87.121.52.49 "chmod 600 /home/calendar-agent/secrets/*.json"
```

The refresh token works server-side — no need to re-OAuth on VPSBG. Because
the app is Published in production, the token will not expire.

VPSBG runs Ubuntu — no WSL networking concerns there. The OAuth flow only
needs to happen once on a machine with a browser; the server side just
consumes the existing token.json.

---

## Optional: scope tightening (post-Step 9)

The `https://www.googleapis.com/auth/calendar` (full) scope is only needed to
*create* the two calendars in Step 9. After calendars exist, the agent only
needs `gmail.readonly` and `calendar.events` (which can read/write events on
existing calendars).

If you want tighter scope hygiene:

1. **Auth Platform → Data Access** → **Add or Remove Scopes**
2. Uncheck `https://www.googleapis.com/auth/calendar`
3. Update → Save
4. Re-run `oauth_setup.py` to get a new token with narrower scope
5. Replace the old `token.json`

For a personal-use agent on your own account, this is optional. For multi-user
or audit-sensitive deployments, it's recommended.

---

## Optional: rotate the OAuth client secret

If the client secret is ever exposed (e.g., pasted into a shared chat, sent
in plaintext email, committed to a public repo), rotate it:

1. **Auth Platform → Clients** → click `calendar-agent-cli`
2. Scroll to **Client secrets** section
3. Click **+ Add secret** — popup shows new secret value with a Download
   button. **Click Download JSON immediately** — the secret value is only
   shown once.
4. Replace local `credentials.json` with the downloaded file (same rename
   + chmod as Step 7)
5. Re-run `oauth_setup.py` to get a new token (old token may still work
   briefly; new one is cleaner)
6. Back in Clients page: find the OLD secret in the list, click **Disable**,
   then **Delete**

You can hold at most 2 secrets simultaneously (Google's limit). Always
download the new one before disabling the old.

---

## Troubleshooting

**`xdg-open: x-www-browser: not found` (and similar)**
→ Expected in WSL. The script handles this by printing the URL. Copy into
Windows browser manually.

**Browser shows "This site can't be reached" / `ERR_CONNECTION_TIMED_OUT` after clicking Allow**
→ WSL2 mirrored networking is not active. See "WSL prerequisite" at top of
this doc. After enabling, run `wsl --shutdown` from PowerShell and reopen.

**`Error 400: invalid_request` on Google's Access blocked page**
→ The redirect URI in the OAuth flow doesn't match what Google expects.
Likely cause: `oauth_setup.py` is using `host='0.0.0.0'` in
`run_local_server()`, which makes the redirect URI `http://0.0.0.0:PORT/`
(rejected by Google). Use `host='localhost'` for the redirect URI; bind to
all interfaces happens automatically with mirrored networking.

**"Access blocked: TRG Calendar Agent has not completed Google verification"**
→ App is in Testing status with you not listed as a test user. Either add
yourself in Audience → Test users, or publish the app (Step 5).

**`redirect_uri_mismatch`**
→ You picked "Web application" instead of "Desktop app" in Step 6. Delete
the client and recreate as Desktop app.

**Token expires unexpectedly (after ~7 days)**
→ App is still in "Testing" status. Refresh tokens for testing apps expire
after 7 days. Publish the app per Step 5, then re-run `oauth_setup.py`.

**"This app is blocked" with no Advanced option**
→ Browser cached an older auth state, or you're signed in as a Google
Workspace user with admin-blocked third-party apps. Try incognito window
first; if that fails, sign in with the right account.

**Browser opens to Google Search instead of OAuth page**
→ You pasted the URL with a leading quote character. Re-copy the URL
without the quote and paste again.

**`xdg-open` warnings followed by stack trace ending in `WSGITimeoutError`**
→ The script's local listener started but Windows browser never reached it.
Mirrored networking issue (see "Browser shows This site can't be reached"
above) or you took longer than ~5 minutes to complete the consent flow
(the listener has a timeout). Re-run the script.

**`oauth_setup.py` reports `AttributeError: 'NoneType' object has no attribute 'replace'`**
→ Same as above — the OAuth flow timed out without the listener receiving
the callback. Re-run and complete the browser steps quickly.