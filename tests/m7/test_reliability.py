from plantguard.observability.reliability import (
    CircuitBreaker,
    CircuitOpenError,
    CircuitState,
    resilient_call,
    retry_with_backoff,
    with_fallback,
)


def test_retry_succeeds_after_transient_failures():
    attempts = 0
    delays = []

    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("temporary failure")
        return "success"

    result = retry_with_backoff(
        operation,
        max_attempts=3,
        base_delay=0.5,
        sleep=delays.append,
    )

    assert result == "success"
    assert attempts == 3
    assert delays == [0.5, 1.0]


def test_retry_raises_after_max_attempts():
    attempts = 0
    delays = []

    def operation():
        nonlocal attempts
        attempts += 1
        raise ConnectionError("service unavailable")

    try:
        retry_with_backoff(
            operation,
            max_attempts=3,
            base_delay=0.5,
            sleep=delays.append,
        )
        assert False, "Expected ConnectionError"
    except ConnectionError:
        pass

    assert attempts == 3
    assert delays == [0.5, 1.0]


def test_fallback_is_used_when_primary_fails():
    fallback_calls = []

    result = with_fallback(
        lambda: (_ for _ in ()).throw(TimeoutError("timed out")),
        lambda: fallback_calls.append("used") or {"status": "fallback"},
    )

    assert result == {"status": "fallback"}
    assert fallback_calls == ["used"]


def test_circuit_opens_after_failure_threshold():
    circuit = CircuitBreaker(failure_threshold=2, reset_timeout=10)

    for _ in range(2):
        try:
            circuit.call(
                lambda: (_ for _ in ()).throw(ConnectionError("offline"))
            )
        except ConnectionError:
            pass

    assert circuit.state == CircuitState.OPEN

    try:
        circuit.call(lambda: "should not run")
        assert False, "Expected CircuitOpenError"
    except CircuitOpenError:
        pass


def test_circuit_recovers_after_successful_half_open_trial():
    now = [100.0]
    circuit = CircuitBreaker(
        failure_threshold=1,
        reset_timeout=10,
        clock=lambda: now[0],
    )

    try:
        circuit.call(
            lambda: (_ for _ in ()).throw(ConnectionError("offline"))
        )
    except ConnectionError:
        pass

    assert circuit.state == CircuitState.OPEN

    now[0] += 11
    assert circuit.call(lambda: "recovered") == "recovered"
    assert circuit.state == CircuitState.CLOSED


def test_resilient_call_uses_fallback_after_retries():
    attempts = 0
    delays = []
    fallback_calls = []
    circuit = CircuitBreaker(failure_threshold=3)

    def operation():
        nonlocal attempts
        attempts += 1
        raise ConnectionError("service unavailable")

    result = resilient_call(
        operation,
        lambda: fallback_calls.append("used")
        or {
            "status": "evidence_unavailable",
            "human_review_required": True,
        },
        circuit=circuit,
        max_attempts=3,
        base_delay=0.5,
        sleep=delays.append,
    )

    assert result == {
        "status": "evidence_unavailable",
        "human_review_required": True,
    }
    assert attempts == 3
    assert delays == [0.5, 1.0]
    assert fallback_calls == ["used"]
    assert circuit.state == CircuitState.OPEN
