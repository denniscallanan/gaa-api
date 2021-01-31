import unittest
from src.api.retry import retry

NON_RETRY_ATTEMPTS = 1


class TestImporterClient(unittest.TestCase):

    def setUp(self):
        self.attempts = 0

    @retry(exceptions=(KeyError,), initial_wait_seconds=0)
    def function_to_try_one(self):
        self.attempts += 1
        if self.attempts <= 2:
            raise KeyError

    @retry(exceptions=(KeyError,), initial_wait_seconds=0)
    def function_to_try_two(self):
        self.attempts += 1
        raise KeyError

    @retry(exceptions=(ValueError,), initial_wait_seconds=0)
    def function_to_try_three(self):
        self.attempts += 1
        raise KeyError

    def test_retry(self):
        self.attempts = 0
        self.assertEqual(self.attempts, 0)
        self.function_to_try_one()
        self.assertEqual(self.attempts, 2 + NON_RETRY_ATTEMPTS)
        self.attempts = 0
        self.assertRaises(KeyError, self.function_to_try_two)
        self.assertEqual(self.attempts, 3 + NON_RETRY_ATTEMPTS)
        self.attempts = 0
        self.assertRaises(KeyError, self.function_to_try_three)
        self.assertEqual(self.attempts, NON_RETRY_ATTEMPTS)
