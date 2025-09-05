from __future__ import annotations

import time
from threading import Lock


class TokenBucket:
    def __init__(self, rps: float = 0.5, burst: int = 1):
        self.capacity = max(1.0, float(burst))
        self.tokens = self.capacity
        self.rate = float(rps)
        self.timestamp = time.monotonic()
        self._lock = Lock()

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            delta = now - self.timestamp
            self.timestamp = now
            self.tokens = min(self.capacity, self.tokens + delta * self.rate)
            if self.tokens < 1.0:
                sleep_time = (1.0 - self.tokens) / self.rate if self.rate > 0 else 1.0
                time.sleep(sleep_time)
                self.tokens = 0.0
            else:
                self.tokens -= 1.0
