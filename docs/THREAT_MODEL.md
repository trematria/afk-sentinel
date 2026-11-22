# Threat model — developer alpha

## Protected assets
- Personal video footage and motion timestamps.
- Webcam access and local session lock state.
- Optional future device pairing credentials, Web Push subscriptions and session cookies.

## Trust boundaries
- GNOME D-Bus lock state is a per-user desktop signal. It is not tamperproof against a malicious process
  with equivalent user privileges.
- Motion runs as the desktop user and accesses the camera; no root or privileged service required.
- Local recordings are readable by root and other processes running as the same user.
- Web Push providers receive minimal metadata required for delivery when opted in; footage stays local by default.

## Current mitigations
- Fail-closed camera stop on D-Bus error and abnormal state.
- Separate Motion subprocess controlled by SIGTERM with bounded shutdown and SIGKILL fallback.
- Screen-unlocked state does not start recording.
- No live HTTP streaming or web control ports.
- Read-only retention preview; no automated deletes.
- Strict user-owned private directories for created state and recordings.

## Known limitations
- Cannot record when host is sleeping or powered down, or physical camera is blocked.
- User/root-level malicious software can disable, modify or delete recordings.
- Motion detection is not an intrusion identity detector; some activity will be missed or false alarms raised.
- Process crash/reboot can interrupt current recording; verified post-reboot recovery is pending.
- `MotionRunner` suppresses Motion output; operational troubleshooting requires an audited logging plan.
- Filesystem owner-only permissions do not add encryption beyond whatever the host filesystem provides.
- A live-view architecture increases attack surface; no viewer is implemented or exposed in alpha.
- No protection against local same-user race or hostile config edits in this developer build.

## Out-of-scope
- Preventing malicious administrators, physical theft, or bypass of disk encryption.
- Stealth recording, hidden camera access, password interception or biometric manipulation.

## Mandatory gates before broad distribution
- Threat-model review of security-sensitive paths, dependency updates, safe installation/uninstallation,
  reboot and sleep testing, workload/CPU/storage ceilings, privacy and consent documentation.
