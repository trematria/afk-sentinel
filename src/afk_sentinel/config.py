"""Configuration validation. No network credentials or cloud services in v0.1."""
from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    camera_device: Path
    recordings_dir: Path
    state_dir: Path
    motion_binary: Path = Path('/usr/bin/motion')
    gdbus_binary: Path = Path('/usr/bin/gdbus')
    width: int = 640
    height: int = 480
    fps: int = 10
    motion_threshold: int = 1500
    poll_seconds: float = 1.0
    shutdown_seconds: float = 15.0

    @classmethod
    def from_file(cls, path: Path) -> 'Settings':
        payload = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(payload, dict):
            raise ValueError('Config must be a JSON object')
        allowed = set(cls.__dataclass_fields__)
        unknown = set(payload) - allowed
        if unknown:
            raise ValueError('Unknown configuration keys: ' + ', '.join(sorted(unknown)))
        mandatory = {'camera_device', 'recordings_dir', 'state_dir'}
        missing = mandatory - set(payload)
        if missing:
            raise ValueError('Missing configuration keys: ' + ', '.join(sorted(missing)))
        for name in ('camera_device', 'recordings_dir', 'state_dir', 'motion_binary', 'gdbus_binary'):
            if name in payload:
                if not isinstance(payload[name], str):
                    raise ValueError(f'{name} must be a path string')
                payload[name] = Path(payload[name]).expanduser().absolute()
        settings = cls(**payload)
        settings.validate()
        return settings

    def validate(self) -> None:
        if not self.camera_device.is_absolute() or not str(self.camera_device).startswith('/dev/'):
            raise ValueError('camera_device must be an absolute path under /dev/')
        for name in ('camera_device', 'recordings_dir', 'state_dir', 'motion_binary', 'gdbus_binary'):
            val = getattr(self, name)
            if not val.is_absolute() or any(c in str(val) for c in '\r\n\x00'):
                raise ValueError(f'Invalid {name} path')
        if not 160 <= self.width <= 3840 or not 120 <= self.height <= 2160:
            raise ValueError('Unsupported frame size')
        if not 1 <= self.fps <= 30 or not 1 <= self.motion_threshold <= 100000:
            raise ValueError('Invalid fps or threshold')
        if not 0.2 <= self.poll_seconds <= 10.0 or not 1 <= self.shutdown_seconds <= 30:
            raise ValueError('Invalid polling or shutdown interval')
        if self.recordings_dir == self.state_dir:
            raise ValueError('Recordings and state directories must differ')
