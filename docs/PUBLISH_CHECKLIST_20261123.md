# TRELAB AFK Sentinel — public alpha publication checklist

Status: **publication requires a GitHub repository and an explicit final release action**. This file alone does not publish anything.

## Before publication

- [x] Archive contains source, tests, documentation, MIT licence and no recorded footage.
- [x] All 15 tests passed locally on 23 November 2026.
- [x] Mobile push, live view and email are clearly marked not implemented.
- [ ] Check GitHub account owner and create `trematria/afk-sentinel` as a new public repository, if available.
- [ ] Upload/push source files (not personal test archives, credentials or footage).
- [ ] Confirm `.github/workflows/ci.yml`, `.gitignore`, LICENSE and source are present.
- [ ] Confirm GitHub Actions passes on its configured Python versions.
- [ ] Create tag `v0.1.0-alpha` and a **pre-release** entry with the contents of `LAUNCH_NOTES_20261123.md`.
- [ ] Verify public release URL and source archive checksums before announcing on social media.

## Suggested GitHub CLI publish workflow (run on your own laptop)

Only after ensuring the repo name is available, and reviewing the source: 

```bash
# From the extracted afk-sentinel-v0.1.0-alpha directory:
command -v git
command -v gh
gh auth status
bash scripts/verify_source.sh
git init -b main
git add .
git diff --cached --stat
# Confirm no private files; review staged names before commit.
git commit -m 'Initial public AFK Sentinel v0.1.0-alpha source'
gh repo create trematria/afk-sentinel --public --source=. --remote=origin --push \n  --description 'Local-first Linux workstation security with GNOME lock-aware motion recording'
# Check GitHub Actions status and issue disclosure before release creation.
```

If `git commit` requests your identity, configure your preferred Git author name and a GitHub-associated **no-reply email**; do not expose your private address unintentionally. The `gh` authentication flow is interactive and should never be pasted into public chat.

If `gh` is unavailable, create an empty public repository at https://github.com/new (do not pre-add README or licence), then use GitHub's browser **Add file → Upload files** to upload the extracted source tree, preserving hidden `.github` and `.gitignore` files. Confirm that the folder hierarchy was preserved. Do not upload this ZIP as a single code file: source must be committed as individual files.

## GitHub release

Once the repository and CI exist, open Releases → Draft a new release, set tag `v0.1.0-alpha`, mark **This is a pre-release**, paste `LAUNCH_NOTES_20261123.md`, and optionally attach the verified source archive. Confirm the release was published before posting public announcements.

## Rollback / preservation

No action in this checklist requires installing or modifying the commissioned R05C workstation service. Avoid `systemctl` changes or running the alpha controller on that workstation.
