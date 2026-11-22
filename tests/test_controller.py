import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from afk_sentinel.controller import Controller


class FakeRunner:
    def __init__(self):
        self.started = 0
        self.stopped = 0
        self.running = False
        self.proc = None

    def start(self):
        self.started += 1
        self.running = True
        self.proc = object()

    def is_running(self):
        return self.running

    def stop(self):
        self.stopped += 1
        self.running = False
        self.proc = None
        return 0


class ControllerTests(unittest.TestCase):
    def test_unlocked_does_not_start_camera(self):
        runner = FakeRunner()
        Controller(lambda: False, runner).step()
        self.assertEqual(runner.started, 0)

    def test_lock_starts_and_unlock_stops(self):
        state = [True]
        runner = FakeRunner()
        c = Controller(lambda: state[0], runner)
        c.step()
        state[0] = False
        c.step()
        self.assertEqual((runner.started, runner.stopped), (1, 1))

    def test_repeated_lock_does_not_duplicate(self):
        runner = FakeRunner()
        c = Controller(lambda: True, runner)
        c.step(); c.step(); c.step()
        self.assertEqual(runner.started, 1)

    def test_query_failure_stops_active_camera(self):
        state = [True]
        runner = FakeRunner()
        def query():
            if state[0] is None:
                raise TimeoutError('D-Bus unavailable')
            return state[0]
        c = Controller(query, runner)
        c.step()
        state[0] = None
        with self.assertRaises(TimeoutError):
            c.step()
        self.assertFalse(c.active)
        self.assertEqual(runner.stopped, 1)

    def test_unknown_query_result_stops_camera(self):
        state = [True]
        runner = FakeRunner()
        c = Controller(lambda: state[0], runner)
        c.step()
        state[0] = 'not locked'
        with self.assertRaises(RuntimeError):
            c.step()
        self.assertEqual(runner.stopped, 1)

    def test_unexpected_camera_exit_fails(self):
        runner = FakeRunner()
        c = Controller(lambda: True, runner)
        c.step()
        runner.running = False
        with self.assertRaises(RuntimeError):
            c.step()

    def test_stop_is_idempotent(self):
        runner = FakeRunner()
        c = Controller(lambda: True, runner)
        c.step(); c.stop_camera(); c.stop_camera()
        self.assertEqual(runner.stopped, 1)

if __name__ == '__main__':
    unittest.main()
