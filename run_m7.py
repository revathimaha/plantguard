import src.plantguard.observability.tracing as tracing
from src.plantguard.observability.reliability import (
    CircuitBreaker,
    CircuitOpenError,
    resilient_call,
    retry_with_backoff,
    with_fallback,
)

tracing.LOCAL_ONLY = True


def demo_tracing():
    def healthy_node(state):
        return {"status": "ok", "asset": state["asset"]}

    traced = tracing.traced_node("healthy_node", healthy_node)
    result = traced({"asset": "VPW-CNC-MILL-03"})
    print("Traced node result:", result)


def demo_retry():
    attempts = {"count": 0}

    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise TimeoutError("transient sensor-feed timeout")
        return "sensor feed recovered"

    result = retry_with_backoff(flaky, max_attempts=3, sleep=lambda _: None)
    print(f"Retry succeeded after {attempts['count']} attempts:", result)


def demo_fallback():
    def unavailable():
        raise ConnectionError("ERP unavailable")

    result = with_fallback(
        unavailable,
        lambda: "fallback: queued for human review",
    )
    print("Fallback result:", result)


def demo_circuit_breaker():
    breaker = CircuitBreaker(failure_threshold=2, reset_timeout=30.0)

    def always_down():
        raise ConnectionError("ERP down")

    for attempt in range(3):
        try:
            breaker.call(always_down)
        except ConnectionError:
            print(f"Attempt {attempt + 1}: failure recorded ({breaker.state.value})")
        except CircuitOpenError:
            print(f"Attempt {attempt + 1}: rejected, circuit open")


def demo_resilient_call():
    breaker = CircuitBreaker(failure_threshold=3, reset_timeout=30.0)

    def unavailable():
        raise TimeoutError("inventory service timeout")

    result = resilient_call(
        unavailable,
        lambda: "fallback: safe default threshold applied",
        circuit=breaker,
        max_attempts=3,
        sleep=lambda _: None,
    )
    print("Resilient call result:", result)


def main():
    print("== M7 tracing ==")
    demo_tracing()
    print("\n== M7 reliability: retry ==")
    demo_retry()
    print("\n== M7 reliability: fallback ==")
    demo_fallback()
    print("\n== M7 reliability: circuit breaker ==")
    demo_circuit_breaker()
    print("\n== M7 reliability: resilient_call ==")
    demo_resilient_call()


if __name__ == "__main__":
    main()
