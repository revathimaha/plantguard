from unittest.mock import patch

import pytest

from plantguard.observability.tracing import traced_node


def test_node_runs_when_langfuse_client_initialization_fails():
    calls = []

    def node(state):
        calls.append(state)
        return {"status": "ok"}

    with patch(
        "plantguard.observability.tracing.get_client",
        side_effect=RuntimeError("telemetry unavailable"),
    ):
        result = traced_node("test_node", node)({"value": 1})

    assert result == {"status": "ok"}
    assert calls == [{"value": 1}]


def test_node_exception_is_propagated():
    def node(state):
        raise ValueError("application failure")

    with patch(
        "plantguard.observability.tracing.get_client",
        side_effect=RuntimeError("telemetry unavailable"),
    ):
        with pytest.raises(ValueError, match="application failure"):
            traced_node("test_node", node)({})


    
def test_node_runs_once_when_span_creation_fails():
    calls = []

    def node(state):
        calls.append(state)
        return {"status": "ok"}

    with patch(
        "plantguard.observability.tracing.get_client"
    ) as get_client:
        get_client.return_value.start_as_current_observation.side_effect = (
            RuntimeError("span unavailable")
        )

        result = traced_node("test_node", node)({"value": 1})

    assert result == {"status": "ok"}
    assert calls == [{"value": 1}]


def test_node_result_survives_span_close_failure():
    calls = []

    class FakeSpan:
        def update(self, **kwargs):
            pass

    class FakeObservation:
        def __enter__(self):
            return FakeSpan()

        def __exit__(self, exc_type, exc, tb):
            raise RuntimeError("export context failed")

    def node(state):
        calls.append(state)
        return {"status": "ok"}

    with patch(
        "plantguard.observability.tracing.get_client"
    ) as get_client:
        get_client.return_value.start_as_current_observation.return_value = (
            FakeObservation()
        )

        result = traced_node("test_node", node)({"value": 1})

    assert result == {"status": "ok"}
    assert calls == [{"value": 1}]
