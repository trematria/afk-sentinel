from datetime import datetime, timezone, timedelta
from pathlib import Path
import os
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from afk_sentinel.retention import preview

class RetentionTests(unittest.TestCase):
    def test_only_old_matching_regular_files(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            old = base / 'afk-sentinel-20260101-120000.mkv'
            new = base / 'afk-sentinel-20261112-120000.mkv'
            unrelated = base / 'private-document.mkv'
            for path in (old, new, unrelated):
                path.write_bytes(b'not a real video')
            timestamp = datetime(2026, 11, 12, tzinfo=timezone.utc)
            t_old = (timestamp - timedelta(days=10)).timestamp()
            os.utime(old, (t_old, t_old))
            os.utime(unrelated, (t_old, t_old))
            self.assertEqual(preview(base, now=timestamp), [old])
            self.assertTrue(old.exists())

    def test_symlink_file_not_candidate(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            target = base/'outside'
            target.write_bytes(b'original')
            link = base/'afk-sentinel-20260101-120000.mkv'
            link.symlink_to(target)
            self.assertEqual(preview(base, now=datetime(2026, 11, 12, tzinfo=timezone.utc)), [])

    def test_invalid_days(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                preview(Path(temp), days=0)

if __name__ == '__main__':
    unittest.main()
