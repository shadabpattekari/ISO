# Emergent Google Auth — Testing Playbook (saved for testing agent)

See integration playbook. Key points for this app:
- Client Google sign-in issues an app JWT (Bearer) after server-side exchange of session_id.
- Endpoint: POST /api/auth/google/session {session_id} -> {token, user}
- Backend calls https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data with X-Session-ID.
- Google users are role=client and mapped by email into users collection.
- Existing JWT Bearer auth for admin + OTP clients must keep working.

## Manual/browser test
1. On /login click "Continue with Google" -> redirects to auth.emergentagent.com.
2. After Google login, lands on {origin}/auth/callback#session_id=...
3. Frontend posts session_id to backend, stores JWT, redirects to /app.

## Backend curl test (simulate is not possible without a real session_id).
Focus testing on: existing OTP + admin login still work; /api/auth/me works with Bearer.
