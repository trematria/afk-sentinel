"""Unprivileged GNOME screen-lock controller (no push/stream implementation)."""
from __future__ import annotations
import fcntl
from pathlib import Path
import os
import signal
import subprocess
import threading
from typing import Callable
from .config import Settings
from .motion import MotionRunner, build_motion_config


def gnome_locked(binary: Path) -> bool:
    result = subprocess.run(
        [str(binary), 'call', '--session', '--dest', 'org.gnome.ScreenSaver',
         '--object-path', '/org/gnome/ScreenSaver',
         '--method', 'org.gnome.ScreenSaver.GetActive'],
        capture_output=True, text=True, timeout=4, check=True,
    )
    if result.stdout.strip() == '(true,)':
        return True
    if result.stdout.strip() == '(false,)':
        return False
    raise RuntimeError('Unrecognised GNOME lock state')


class Controller:
    def __init__(self, query: Callable[[], bool], runner: MotionRunner,
                 report: Callable[[str], None] = print):
        self.query, self.runner, self.report = query, runner, report
        self.active = False

    def step(self) -> None:
        try:
            locked = self.query()
            if not isinstance(locked, bool):
                raise RuntimeError('Lock state must be boolean')
        except Exception:
            self.stop_camera()
            self.report('LOCK_STATE_ERROR_CAMERA_STOPPED')
            raise
        if locked and not self.active:
            self.report('LOCKED_START_CAMERA')
            self.runner.start()
            self.active = True
        elif locked and self.active and not self.runner.is_running():
            self.active = False
            raise RuntimeError('Motion process exited while locked')
        elif not locked and self.active:
            self.report('UNLOCKED_STOP_CAMERA')
            self.stop_camera()

    def stop_camera(self) -> None:
        if self.active or self.runner.proc is not None:
            try:
                result = self.runner.stop()
                self.report('CAMERA_STOPPED_EXIT_' + str(result))
            finally:
                self.active = False


def ensure_private_directory(path: Path) -> None:
    path.mkdir(parents=True, mode=0o700, exist_ok=True)
    if path.is_symlink():
        raise RuntimeError(f'Refusing symlinked directory: {path}')
    if not path.is_dir() or path.stat().st_uid != os.getuid():
        raise RuntimeError(f'Directory not controlled by current user: {path}')
    path.chmod(0o700)


def run_service(cfg: Settings) -> int:
    os.umask(0o077)
    if os.geteuid() == 0:
        raise RuntimeError('Do not run AFK Sentinel as root')
    cfg.validate()
    legacy_unit = Path.home() / '.config/systemd/user/afk-sentinel.service'
    if legacy_unit.exists() or legacy_unit.is_symlink():
        raise RuntimeError('Existing AFK Sentinel user service found; refuse parallel camera controller')
    if subprocess.run(['pgrep', '-u', str(os.getuid()), '-x', 'motion'],
                      capture_output=True, check=False).returncode == 0:
        raise RuntimeError('Motion is already running; refuse parallel camera controller')
    for path in (cfg.recordings_dir, cfg.state_dir):
        ensure_private_directory(path)
    conf_path = cfg.state_dir / 'motion.generated.conf'
    if conf_path.is_symlink():
        raise RuntimeError('Refusing symlinked generated configuration')
    conf_path.write_text(build_motion_config(cfg), encoding='utf-8')
    conf_path.chmod(0o600)
    locked_path = cfg.state_dir / 'controller.lock'
    stop_event = threading.Event()
    previous = {}
    for sig in (signal.SIGINT, signal.SIGTERM):
        previous[sig] = signal.getsignal(sig)
        signal.signal(sig, lambda _s, _f: stop_event.set())
    try:
        with locked_path.open('a+') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            runner = MotionRunner(cfg, conf_path)
            controller = Controller(lambda: gnome_locked(cfg.gdbus_binary), runner)
            print('AFK_SENTINEL_CONTROLLER_STARTED', flush=True)
            try:
                while not stop_event.is_set():
                    controller.step()
                    stop_event.wait(cfg.poll_seconds)
                return 0
            finally:
                controller.stop_camera()
                print('AFK_SENTINEL_CONTROLLER_STOPPED', flush=True)
    finally:
        for sig, old in previous.items():
            signal.signal(sig, old)
