# AFK Sentinel v0.1.0-alpha — founding public source release

**Date:** 23 November 2026  
**Publisher:** TRELAB  
**Status:** developer alpha; not a production security appliance

## Overview

AFK Sentinel is a local-first workstation-monitoring prototype for Ubuntu/GNOME. It observes the GNOME screen lock state and starts the external Motion video recorder only while the screen is locked. On unlock or an invalid/unavailable lock-state response, the controller stops the recording process. Video evidence is stored locally, with web-control and camera streaming disabled.

## Included in this release

- Separate, MIT-licensed Python sources for lock-state polling and Motion lifecycle control
- Configuration validator and Motion configuration renderer
- No-root, explicit camera-use opt-in for developer tests
- Read-only seven-day retention candidate preview: **no deletion**
- Threat model, security policy, development roadmap, proposed mobile design
- 15 passing offline unit tests verified on 23 November 2026

## Not included

- Mobile push notifications or a private live-view link (primary planned v0.2 feature)
- Optional email alerts (future; off by default)
- Webcam streaming server, mobile application or cloud account
- Production installer, automatic recording retention/deletion, storage quota enforcement
- Verified reboot or suspend/resume recovery across multiple machines

## Compatibility and safety

Target is Ubuntu Linux with GNOME, `gdbus`, Motion 4.7.x, Python 3.11+, and a compatible V4L2 camera. The reference workstation proved local lock/unlock recording with a separate installed R05C service; **this repackaged alpha controller has only offline verification and requires fresh-machine testing**. A suspended computer cannot record. Do not run this code alongside an existing AFK Sentinel or Motion camera service. Do not use it for covert or unlawful recording.

## Licence

This repository's original Python code is MIT-licensed; Motion is an external dependency distributed under its own GPL terms and is not included in this package.

## Verification

Run `bash scripts/verify_source.sh` from the unpacked source root. The verification uses no webcam and no network. A published GitHub repository and passing GitHub Actions must be independently confirmed after upload.
