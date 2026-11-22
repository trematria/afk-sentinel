# Release gate — 23 November 2026

## Verified in isolated source-build environment
- Original reference-source ZIP SHA-256 integrity and manifest verified.
- 15 Python unit tests passed; compilation and configuration CLI checks passed.
- Local-only Motion configuration outputs `webcontrol_port 0` and `stream_port 0`.
- Public source tree excludes personal footage, machine-specific workstation configuration and credentials.
- New documentation-only launch delta; complete checksum manifest regenerated.

## Remain unverified
- Fresh-machine, new portable controller's full on-device recording cycle.
- GitHub repository publication and GitHub Actions CI.
- Reboot and suspend/resume recovery on the commissioned workstation.
- Mobile push, authenticated live view, optional email and automatic retention.
- Security assessment for broad deployment and legal review.

## Decision
Approved as **source-only developer alpha candidate**, not as a fully commissioned product, portable install package or completed public GitHub release. Publish with release warnings intact; verify repository and CI separately.
