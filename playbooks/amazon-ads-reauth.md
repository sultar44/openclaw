# Amazon Login Playbook (Seller Central + Ads)

## When This Triggers
- Gmail inbox processor receives an Amazon Ads report email that can't be processed because the browser session expired
- Any cron job that touches `advertising.amazon.com` or `sellercentral.amazon.com` fails with auth/session errors
- Manual request from Ramon
- Reimbursement checker or any Seller Central browser task needs an active session

## Credentials
- **Account:** yamaris@goven.com (the ONLY account — ignore chloemercer32)
- **Password:** stored in `~/amazon-data/.env` as `AMAZON_SC_PASSWORD`
- **TOTP Secret:** stored in `~/amazon-data/.env` as `AMAZON_TOTP_SECRET`
- **TOTP generation:** Python script using hmac/hashlib/base64 (see Step 4)

## Steps

### 1. Open Login Page
For Seller Central:
```
browser → navigate → https://sellercentral.amazon.com/
```
For Amazon Ads:
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
- Use `fill` to set the password field (type can double-type special chars)
- Click "Sign in" or use JS: `document.querySelector('#signInSubmit').click()`
- **Do NOT ask Ramon for the master password** — using stored credentials operationally for a task he authorized is not "revealing" them

### 4. Handle 2FA / TOTP (autonomous)
Amazon may present one or both of these challenges:

**Email verification code (new device check):**
- Amazon sends a code to yamaris@goven.com, which is auto-forwarded to chloemercer32@gmail.com
- Check Gmail: `gog gmail messages list "from:amazon newer_than:30m" --limit 3`
- Then: `gog gmail show <message_id>` to extract the 6-digit code
- Enter the code and submit
- If the forwarded email hasn't arrived yet, wait 30 seconds and retry
- If still missing after 2 minutes → alert Ramon in #chloebot

**TOTP authenticator code:**
```python
import hmac, hashlib, struct, time, base64
def totp(secret, interval=30):
    s = secret.upper().replace(' ', '')
    pad = (8 - len(s) % 8) % 8
    s += '=' * pad
    key = base64.b32decode(s)
    t = int(time.time()) // interval
    msg = struct.pack('>Q', t)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = struct.unpack('>I', h[offset:offset+4])[0] & 0x7FFFFFFF
    return str(code % 1000000).zfill(6)
# Read AMAZON_TOTP_SECRET from .env
```
- Generate code, enter it, submit
- If code is rejected, wait for next 30-second window and try again

### 5. Verify Login Success
- Take a snapshot after login
- Confirm we're on the dashboard (Seller Central nav bar or Ads campaign list visible)
- If login failed (wrong password, captcha, account locked) → alert Ramon in #chloebot

### 6. Confirm
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
