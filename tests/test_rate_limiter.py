import unittest

from src.rate_limiter import RateLimiter


class FakeClock:
    """A clock that lets us control time during testing."""

    def __init__(self):
        self.current_time = 1000

    def __call__(self):
        return self.current_time

    def advance(self, seconds):
        self.current_time += seconds


class TestRateLimiter(unittest.TestCase):

    def setUp(self):
        self.clock = FakeClock()

        self.limiter = RateLimiter(
            limit=5,
            window_seconds=60,
            clock=self.clock,
        )

        # Replace the real clock with our test clock.
        self.limiter_clock = self.clock
        self.limiter._clock = self.clock

    def test_first_request_is_allowed(self):
        result = self.limiter.allow_request("client_A")

        self.assertTrue(result["allowed"])
        self.assertEqual(result["remaining"], 4)

    def test_request_below_limit_is_allowed(self):
        self.limiter.allow_request("client_A")

        result = self.limiter.allow_request("client_A")

        self.assertTrue(result["allowed"])
        self.assertEqual(result["remaining"], 3)

    def test_fifth_request_is_allowed(self):
        for _ in range(4):
            self.limiter.allow_request("client_A")

        result = self.limiter.allow_request("client_A")

        self.assertTrue(result["allowed"])
        self.assertEqual(result["remaining"], 0)

    def test_sixth_request_is_rejected(self):
        for _ in range(5):
            self.limiter.allow_request("client_A")

        result = self.limiter.allow_request("client_A")

        self.assertFalse(result["allowed"])
        self.assertEqual(result["remaining"], 0)

    def test_request_after_window_expires_is_allowed(self):
        for _ in range(5):
            self.limiter.allow_request("client_A")

        # Advance the test clock by 60 seconds.
        self.clock.advance(60)

        result = self.limiter.allow_request("client_A")

        self.assertTrue(result["allowed"])
        self.assertEqual(result["remaining"], 4)

    def test_two_clients_have_independent_limits(self):
        for _ in range(5):
            self.limiter.allow_request("client_A")

        result_a = self.limiter.allow_request("client_A")
        result_b = self.limiter.allow_request("client_B")

        self.assertFalse(result_a["allowed"])
        self.assertTrue(result_b["allowed"])
        self.assertEqual(result_b["remaining"], 4)


if __name__ == "__main__":
    unittest.main()