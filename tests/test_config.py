import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from afk_sentinel.config import Settings
from afk_sentinel.motion import build_motion_config

class ConfigTests(unittest.TestCase):
    def make(self, fields=None):
        config = {'camera_device':'/dev/video0', 'recordings_dir':'~/Videos/AFK', 'state_dir':'~/.local/state/afk-dev'}
        config.update(fields or {})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'settings.json'
            path.write_text(json.dumps(config))
            return Settings.from_file(path)

    def test_valid(self):
        self.assertTrue(self.make().recordings_dir.is_absolute())

    def test_unknown_field_rejected(self):
        with self.assertRaises(ValueError):
            self.make({'email_password':'secret'})

    def test_non_device_rejected(self):
        with self.assertRaises(ValueError):
            self.make({'camera_device':'/home/user/video0'})

    def test_resolution_rejected(self):
        with self.assertRaises(ValueError):
            self.make({'width': 99999})

    def test_local_only_ports(self):
        conf = build_motion_config(self.make())
        self.assertIn('webcontrol_port 0\n', conf)
        self.assertIn('stream_port 0\n', conf)
        self.assertIn('daemon off\n', conf)

if __name__ == '__main__':
    unittest.main()
