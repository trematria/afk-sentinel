"""Read-only retention planning: NEVER deletes files in this release."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import stat

RECORDING = re.compile(r'^afk-sentinel-\d{8}-\d{6}\.mkv$')


def preview(recordings_dir: Path, days: int = 7, now: datetime | None = None) -> list[Path]:
    if not 1 <= days <= 365:
        raise ValueError('days must be between 1 and 365')
    if recordings_dir.is_symlink():
        raise ValueError('Refusing symlinked recordings directory')
    if not recordings_dir.is_dir():
        return []
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    candidates = []
    for item in recordings_dir.iterdir():
        meta = item.lstat()
        if stat.S_ISREG(meta.st_mode) and RECORDING.fullmatch(item.name):
            if datetime.fromtimestamp(meta.st_mtime, timezone.utc) < cutoff:
                candidates.append(item)
    return sorted(candidates)
