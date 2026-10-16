import asyncio

import pytest

from src.plantguard.observability.reliability import (
    CircuitBreaker,
    CircuitState,
    resilient_async_call,
    retry_async_with_backoff,
)


async def _no_sleep(_delay):
    return None


@pytest.mark.asyncio
async def test_transient_sensor_failure_recovers_via_retry():
    attempts = {"count": 0}

    async def flaky_lookup():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ConnectionError("transient MCP sensor-feed failure")
        return {"count": 5, "records": []}

    result = await retry_async_with_backoff(
        flaky_lookup,
        max_attempts=3,
        sleep=_no_sleep,
    )

    assert result == {"count": 5, "records": []}
    assert attempts["count"] == 3


@pytest.mark.asyncio
async def test_permanent_failure_opens_circuit_and_falls_back():
    breaker = CircuitBreaker(failure_threshold=2, reset_timeout=30.0)

    async def always_down():
        raise ConnectionError("ERP/sensor service permanently down")

    async def fallback():
        return {"fallback": True, "degraded": "safe default"}

    for _ in range(2):
        result = await resilient_async_call(
            always_down,
            fallback,
            circuit=breaker,
            max_attempts=2,
            sleep=_no_sleep,
        )
        assert result["fallback"] is True

    assert breaker.state == CircuitState.OPEN

    rejected = await resilient_async_call(
        always_down,
        fallback,
        circuit=breaker,
        max_attempts=2,
        sleep=_no_sleep,
    )
    assert rejected["fallback"] is True


@pytest.mark.asyncio
async def test_success_keeps_circuit_closed():
    breaker = CircuitBreaker(failure_threshold=2, reset_timeout=30.0)

    async def healthy():
        return {"count": 10}

    async def fallback():
        return {"fallback": True}

    result = await resilient_async_call(
        healthy,
        fallback,
        circuit=breaker,
        max_attempts=3,
        sleep=_no_sleep,
    )

    assert result == {"count": 10}
    assert breaker.state == CircuitState.CLOSED


if __name__ == "__main__":
    asyncio.run(test_transient_sensor_failure_recovers_via_retry())
    asyncio.run(test_permanent_failure_opens_circuit_and_falls_back())
    asyncio.run(test_success_keeps_circuit_closed())
    print("All injected-failure integration checks passed.")
