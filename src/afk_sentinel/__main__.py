"""Command line entry point. Explicit --run opt-in required to use camera."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
from .config import Settings
from .controller import run_service
from .motion import build_motion_config
from .retention import preview


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='TRELAB AFK Sentinel developer alpha')
    parser.add_argument('--config', type=Path, required=True, help='Local JSON configuration')
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--check', action='store_true', help='Validate only; no camera access')
    actions.add_argument('--render-motion', action='store_true', help='Display proposed Motion configuration')
    actions.add_argument('--retention-preview', action='store_true', help='List files older than 7 days; do not delete')
    actions.add_argument('--run', action='store_true', help='Run local camera controller')
    parser.add_argument('--ack-camera-use', action='store_true', help='Required with --run')
    args = parser.parse_args(argv)
    try:
        cfg = Settings.from_file(args.config)
        if args.check:
            print('CONFIG_VALID_NO_CAMERA_ACCESS')
        elif args.render_motion:
            print(build_motion_config(cfg))
        elif args.retention_preview:
            files = preview(cfg.recordings_dir)
            print(f'RETENTION_PREVIEW_ONLY: {len(files)} candidate(s)')
            for item in files:
                print(item.name)
        elif args.run:
            if not args.ack_camera_use:
                parser.error('--run requires --ack-camera-use')
            return run_service(cfg)
    except (ValueError, OSError, RuntimeError) as exc:
        print('AFK_SENTINEL_STOP: ' + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
