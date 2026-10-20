import time


class RateLimiter:

    def __init__(self, limit=5, window_seconds=60, clock=None):
        self.limit = limit
        self.window_seconds = window_seconds

        # Use the real clock unless a test clock is provided.
        self.clock = clock if clock is not None else time.monotonic

        self.clients = {}

    def allow_request(self, client_id):
        current_time = self.clock()

        if client_id not in self.clients:
            self.clients[client_id] = {
                "window_start": current_time,
                "count": 0
            }

        client = self.clients[client_id]

        elapsed_time = current_time - client["window_start"]

        if elapsed_time >= self.window_seconds:
            client["window_start"] = current_time
            client["count"] = 0

        if client["count"] >= self.limit:
            remaining_time = (
                self.window_seconds
                - (current_time - client["window_start"])
            )

            return {
                "allowed": False,
                "limit": self.limit,
                "remaining": 0,
                "retry_after": max(0, int(remaining_time + 0.999))
            }

        client["count"] += 1

        return {
            "allowed": True,
            "limit": self.limit,
            "remaining": self.limit - client["count"],
            "retry_after": 0
        }