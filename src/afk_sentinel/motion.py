"""Minimal, fail-closed Motion adapter. No TCP listener enabled."""
from __future__ import annotations
from pathlib import Path
import subprocess
from .config import Settings


def build_motion_config(cfg: Settings) -> str:
    cfg.validate()
    return '\n'.join([
        'daemon off',
        'setup_mode off',
        'log_level 5',
        f'video_device {cfg.camera_device}',
        f'width {cfg.width}',
        f'height {cfg.height}',
        f'framerate {cfg.fps}',
        f'threshold {cfg.motion_threshold}',
        'minimum_motion_frames 2',
        'pre_capture 3',
        'post_capture 10',
        'event_gap 5',
        'picture_output off',
        'movie_output on',
        'movie_codec mkv',
        'movie_max_time 30',
        'movie_quality 50',
        'movie_filename afk-sentinel-%Y%m%d-%H%M%S',
        f'target_dir {cfg.recordings_dir}',
        'webcontrol_port 0',
        'stream_port 0',
        'webcontrol_localhost on',
        'stream_localhost on',
        '',
    ])


class MotionRunner:
    def __init__(self, cfg: Settings, config_path: Path):
        self.cfg = cfg
        self.config_path = config_path
        self.proc: subprocess.Popen | None = None

    def is_running(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def start(self) -> None:
        if self.proc is not None:
            if self.proc.poll() is None:
                raise RuntimeError('Motion already running')
            raise RuntimeError(f'Motion exited unexpectedly: {self.proc.returncode}')
        self.proc = subprocess.Popen(
            [str(self.cfg.motion_binary), '-n', '-c', str(self.config_path)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def stop(self) -> int | None:
        if self.proc is None:
            return None
        proc, self.proc = self.proc, None
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=self.cfg.shutdown_seconds)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
                raise RuntimeError('Motion shutdown exceeded grace period')
        return proc.returncode
