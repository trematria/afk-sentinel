# TRELAB AFK Sentinel Roadmap

Status reviewed for public alpha launch, 2026-11-23. Each gate needs measured evidence, not assumptions.

## R05C: commissioned workstation reference (not in this source repository)
- PASS — GNOME lock/unlock camera start and graceful stop under a user service.
- PASS — local motion-triggered recordings and playback confirmed.
- OPEN — test user service after reboot and new graphical login.
- OPEN — suspend/resume, camera contention and failure recovery.
- OPEN — seven-day retention and disk limits, deletion-free dry run first.

## v0.1.0-alpha — community foundation (this package)
- [x] Portable, unprivileged Python controller and Motion config generator.
- [x] GNOME lock-state fail-closed logic and local-only Motion settings.
- [x] Source tests for lock state and recording start/stop.
- [x] Read-only retention planner, not deletion.
- [x] Security threat model and mobile system design specification.
- [ ] Test on a clean non-production Ubuntu GNOME machine.
- [ ] Prove install/uninstall and absence of user-service conflicts.
- [ ] Re-run lock, unlock, reboot, suspend and resume acceptance tests.

## v0.2 — private mobile experience
- [ ] Authenticated pairing of a phone with an individual workstation.
- [ ] Mobile push alert upon motion detection (per-device opt-in; cooldown).
- [ ] Notification opens viewer URL **without embedding a bearer token**.
- [ ] Authenticated, time-limited stream access restricted to locked state.
- [ ] Tailscale Serve proof-of-concept under strict tailnet access policy.
- [ ] Disabled-on-unlock stream and explicit revocation tests.
- [ ] No server on public network and no `Funnel` exposure.

## v0.3 — operational reliability and privacy
- [ ] Playback interface for locally recorded events.
- [ ] Dry-run reviewed retention *then* approved seven-day cleanup.
- [ ] Storage quota and minimum-free-space protection.
- [ ] Security and audit logs with sensitive content minimised.
- [ ] Suspend/resume, lid closed, camera busy, sleep, network loss and reboot tests.
- [ ] Optional email alert toggle; no email password in project config.
- [ ] Harden service sandboxing and protocol safety; review threat model.

## v1.0 — public stable
- [ ] Release packages with signed checksums and reproducibility evidence.
- [ ] Third-party review and cross-device test matrix.
- [ ] Documentation for lawful use, consent, secure defaults and uninstall.
- [ ] No reliability or security claims without documented independent testing.
