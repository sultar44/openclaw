# Amazon Ads Re-Authentication Playbook

## When This Triggers
- Gmail inbox processor receives an Amazon Ads report email that can't be processed because the browser session expired
- Any cron job that touches `advertising.amazon.com` fails with auth/session errors
- Manual request from Ramon

## Credentials
- **Account:** yamaris@goven.com
- **Password:** stored in `~/amazon-data/.env` as `AMAZON_SC_PASSWORD`
- **2FA:** May be required (SMS or authenticator) — this is the only step that needs Ramon

## Steps

### 1. Open Amazon Ads Login
```
browser → navigate → https://advertising.amazon.com/
```
Amazon will redirect to the sign-in page if the session expired.

### 2. Handle Passkey Popup (if it appears)
Chrome may show a "Sign in with a passkey" modal overlay. This blocks the password field.
- Look for a "Cancel" or "X" button on the passkey dialog
- Click it to dismiss
- If no cancel button is visible, press `Escape`
- **Prevention:** Chrome Preferences have been modified to disable conditional WebAuthn UI. If the popup returns, re-apply the fix (see "Passkey Prevention" section below).

### 3. Enter Credentials
- The login page shows the email (yamaris@goven.com) pre-filled
- Read password from `~/amazon-data/.env` (`AMAZON_SC_PASSWORD`)
- Type password into the password field
- Click "Sign in" or press Enter
- **Do NOT ask Ramon for the master password** — using stored credentials operationally for a task he authorized is not "revealing" them

### 4. Handle 2FA (if prompted)
- If Amazon asks for OTP/2FA verification → **alert Ramon immediately** in #chloebot
- Message: "🔐 Amazon Ads login needs 2FA. Can you provide the code or approve on your phone?"
- Wait for Ramon's response, enter the code, submit
- If no 2FA → proceed

### 5. Verify Login Success
- Take a snapshot after login
- Confirm we're on the Amazon Ads dashboard (campaigns visible, account selector, etc.)
- If login failed (wrong password, captcha, etc.) → alert Ramon

### 6. Confirm in Thread
- Reply in the original alert thread confirming login is restored
- If this was triggered by a cron failure, note that the next scheduled run should succeed

## Passkey Prevention (Chrome Settings)

The openclaw Chrome profile has been configured to disable passkey conditional UI:
- File: `~/.openclaw/browser/openclaw/user-data/Default/Preferences`
- Keys set: `credentials_enable_service.enabled = false`, `webauthn.allow_conditional_ui = false`
- If Chrome updates reset these, re-apply:
  1. Stop browser (`browser → stop`)
  2. Modify Preferences JSON
  3. Restart browser (`browser → start`)

## Proactive Session Monitoring

To avoid surprise failures, add a lightweight check to the daily cron audit:
- Navigate to `https://advertising.amazon.com/` in the openclaw browser
- If it redirects to sign-in → session expired → re-authenticate immediately
- If it loads the dashboard → session is active → no action needed

## Notes
- "Keep me signed in" checkbox should always be checked
- Amazon sessions typically last 1-2 weeks before requiring re-auth
- The account may occasionally show a "select your advertising account" page after login — just select the correct profile
