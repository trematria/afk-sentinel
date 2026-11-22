# Remote Alert + Live View — Accepted Product Design (NOT IMPLEMENTED)

## Experience
1. Workstation GNOME session locks; local Motion camera records triggered events.
2. On motion event, notifier applies cooldown (proposed default: one alert per 60 s).
3. Paired mobile device receives small, non-sensitive push: `Motion detected at workstation`.
4. A tap opens the private live-view application; authentication is required and **no token is in the URL**.
5. Live stream is only available if the desktop is still locked, session remains awake, camera is active,
   and the phone is authorised to access this workstation.
6. Unlock, shutdown, identity revocation or lock-state failure closes and revokes live access.

## Security constraints
- **Disabled until opted in.** No background public API and no port forwarding.
- Prefer loopback-bound viewer with Tailnet-only HTTPS access through Tailscale Serve. Never Funnel.
- Tailscale access control is necessary but *not sufficient*: app-layer authorisation and per-device pairing.
- Viewer must read lock state for each session and enforce camera shutdown on unlock; never rely on UI-only controls.
- Use short-lived sessions, revocation, protection against CSRF, rate limiting and device unlinking.
- Event URL is not itself a secret credential; it must be safe to forward or log without granting entry.
- Do not embed snapshots, GPS, personal names, sensitive frames or secrets in push payloads by default.
- Phone must be online and push notifications permission granted; push delivery is best-effort, not guaranteed.
- Web Push commonly relies on third-party browser push infrastructure even for an otherwise local-first app.

## Notification preferences
- Mobile push: preferred product capability, user opt-in during setup (unavailable in alpha).
- Private live viewing: paired and user authorised, must be explicitly enabled (unavailable in alpha).
- Email: completely optional toggle, **off by default**; provider credentials stored outside version control,
  and any SMTP integration must be separately audited (unavailable in alpha).

## Proposed implementation boundaries
- Local `MotionEvent` event publisher from file/event callbacks, no shell interpolation.
- Notification gateway with Web Push VAPID private key stored in an OS secret store / protected credentials.
- Paired device registry and revocation; minimal event metadata.
- Tailnet-only mobile viewer with origin/CSRF protection and strict lock-state gate.
- Integration tests: stale links, lock/unlock races, offline phone, wrong owner, invalid session,
  different users, suspend/resume, reconnect, replay and revoked pairing.

The current desktop has no configured remote streaming listener or push delivery service.
