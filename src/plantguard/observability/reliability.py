
import time
from collections.abc import Callable
from typing import TypeVar



T = TypeVar("T")


def retry_with_backoff(
    operation: Callable[[], T],
    *,
    max_attempts: int = 3,
    base_delay: float = 0.5,
    retryable_exceptions: tuple[type[Exception], ...] = (TimeoutError, ConnectionError),
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Retry transient failures with bounded exponential backoff."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if base_delay < 0:
        raise ValueError("base_delay cannot be negative")

    for attempt in range(max_attempts):
        try:
            return operation()
        except retryable_exceptions:
            if attempt == max_attempts - 1:
                raise
            sleep(base_delay * (2 ** attempt))

    raise RuntimeError("Unreachable retry state")



def with_fallback(
    operation: Callable[[], T],
    fallback: Callable[[], T],
    *,
    retryable_exceptions: tuple[type[Exception], ...] = (
        TimeoutError,
        ConnectionError,
    ),
) -> T:
    """Return a fallback result for configured transient failures."""

    try:
        return operation()
    except retryable_exceptions:
        return fallback()




from enum import Enum
from threading import Lock
from time import monotonic
from typing import Any


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(RuntimeError):
    """Raised when a circuit breaker rejects a call."""


class CircuitBreaker:
    """A small, thread-safe circuit breaker for synchronous operations."""

    def __init__(
        self,
        *,
        failure_threshold: int = 3,
        reset_timeout: float = 30.0,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be at least 1")
        if reset_timeout < 0:
            raise ValueError("reset_timeout cannot be negative")

        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self._clock = clock
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at: float | None = None
        self._half_open_trial = False
        self._lock = Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            return self._state

    def call(
        self,
        operation: Callable[[], T],
        *,
        retryable_exceptions: tuple[type[Exception], ...] = (
            TimeoutError,
            ConnectionError,
        ),
    ) -> T:
        with self._lock:
            if self._state == CircuitState.OPEN:
                elapsed = self._clock() - (self._opened_at or 0.0)

                if elapsed < self.reset_timeout:
                    raise CircuitOpenError("Circuit is open")

                self._state = CircuitState.HALF_OPEN
                self._half_open_trial = False

            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_trial:
                    raise CircuitOpenError(
                        "Half-open trial already in progress"
                    )
                self._half_open_trial = True

        try:
            result = operation()
        except retryable_exceptions:
            with self._lock:
                self._failures += 1
                if (
                    self._state == CircuitState.HALF_OPEN
                    or self._failures >= self.failure_threshold
                ):
                    self._state = CircuitState.OPEN
                    self._opened_at = self._clock()
                self._half_open_trial = False
            raise
        except Exception:
            with self._lock:
                self._half_open_trial = False
            raise
        else:
            with self._lock:
                self._failures = 0
                self._state = CircuitState.CLOSED
                self._opened_at = None
                self._half_open_trial = False
            return result





def resilient_call(
    operation: Callable[[], T],
    fallback: Callable[[], T],
    *,
    circuit: CircuitBreaker,
    max_attempts: int = 3,
    base_delay: float = 0.5,
    sleep: Callable[[float], None] = time.sleep,
    retryable_exceptions: tuple[type[Exception], ...] = (
        TimeoutError,
        ConnectionError,
    ),
) -> T:
    """Combine circuit breaking, bounded retries, and fallback."""

    def protected_operation() -> T:
        return retry_with_backoff(
            lambda: circuit.call(
                operation,
                retryable_exceptions=retryable_exceptions,
            ),
            max_attempts=max_attempts,
            base_delay=base_delay,
            sleep=sleep,
            retryable_exceptions=retryable_exceptions,
        )

    return with_fallback(
        protected_operation,
        fallback,
        retryable_exceptions=retryable_exceptions,
    )

