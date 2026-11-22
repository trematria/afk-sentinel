# AFK Sentinel

<p align="center">
  <img src="assets/afk-sentinel-emblem.svg" alt="AFK Sentinel — white hawk emblem on black" width="192">
</p>

**A local-first, lock-aware webcam security project by TRELAB.**

**Public developer-alpha launch candidate: 23 November 2026.** This is source code for developers and testers; it is not a production-ready security appliance or a one-click end-user installer.

> **v0.1.0-alpha — developer preview, NOT a production security product.**
>
> The tested workstation installation (R05C) is separate. This repository must not
> replace or overwrite a working AFK Sentinel installation without an independent
> migration plan, a backup and explicit user approval.

## What currently works

- Watches `org.gnome.ScreenSaver.GetActive` on a GNOME graphical session.
- Starts a separate [Motion](https://motion-project.github.io/) process after a verified screen lock.
- Stops that process on unlock, lock-state query failure, process shutdown or service termination.
- Saves motion-triggered MKV footage locally, in private user-owned directories.
- Disables Motion's HTTP control and video stream (`webcontrol_port 0`, `stream_port 0`).
- Provides a **read-only** seven-day retention candidate preview; no deletion logic.
- Has automated Python tests that run without a webcam, network or root permissions.

## Deliberately NOT implemented

**Mobile push notifications, live viewing, authentication for a remote viewer, SMTP email alerts,
recording deletion and disk-space enforcement are NOT active in v0.1.** No notification is sent;
no remote service is started. The accepted direction is a private mobile push alert opening an
authenticated live view, with email as a separately configurable opt-in. See
[Remote Access Specification](docs/REMOTE_ACCESS_SPEC.md) and [Roadmap](ROADMAP.md).

## Compatibility

- Target: Ubuntu Linux, GNOME desktop, a webcam exposed as a V4L2 device, Python >= 3.11, Motion 4.7.x and `gdbus`.
- Lock detection was demonstrated on GNOME Wayland / Ubuntu 26.04.1 LTS; other versions and environments are untested.
- **Fingerprint hardware is not required.** Screen unlocking may use a password, fingerprint or other configured method.
- Locking a computer is **not the same as keeping it awake**: surveillance cannot operate while the laptop is suspended.

## Run offline developer checks (does not activate the webcam)

```bash
cd afk-sentinel-v0.1.0-alpha
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m afk_sentinel --config config.example.json --check
PYTHONPATH=src python3 -m afk_sentinel --config config.example.json --render-motion
PYTHONPATH=src python3 -m afk_sentinel --config config.example.json --retention-preview
```

The example configuration uses generic paths. Set `camera_device`, `recordings_dir` and `state_dir`
for a **separate test machine** before running a real camera test. No real-camera invocation is
performed by the above commands. The explicit opt-in command below is for an isolated test setup,
**not for an already operating R05C workstation**:

```bash
PYTHONPATH=src python3 -m afk_sentinel --config ./config.json --run --ack-camera-use
```

The process should run as the logged-in desktop user; never as root. Run it in a dedicated
graphical-session service only after local acceptance tests. **No installer is shipped in this
first community foundation package**: installation and migration require a separately audited gate.

## Data safety

- Do not commit recordings, actual `config.json`, cloud credentials, authentication tokens or host logs.
- Directory permissions are owner-only (`0700`) and generated Motion configuration is `0600`.
- Access by a process running as the same Linux user or as root is **not prevented**.
- No web endpoint or email notification is enabled by this version.
- This is not a burglar alarm and is not intended for covert or unlawful surveillance.

## Development and licensing

- New TRELAB Python sources: **MIT License**, see [LICENSE](LICENSE).
- Motion is an **external executable dependency** with its **own GPL licence**; it is not bundled here.
- Issues and security reports: see [SECURITY.md](SECURITY.md).
- Please do not include real camera captures, personally identifying footage or secrets in reports.

See [ROADMAP.md](ROADMAP.md) for release gates and [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md)
for known limitations.

## Public alpha launch

See [release notes](LAUNCH_NOTES_20261123.md) and [publish checklist](docs/PUBLISH_CHECKLIST_20261123.md). **Do not run alongside another AFK Sentinel service**, including the tested TRELAB R05C installation. Report issues without recordings or credentials.
