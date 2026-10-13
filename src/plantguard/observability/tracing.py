
from functools import wraps
from time import perf_counter

from langfuse import get_client

LOCAL_ONLY = False


def traced_node(node_name: str, node_function):
    """Trace node execution without letting telemetry failures mask results."""

    @wraps(node_function)
    def wrapper(state: dict, *args, **kwargs):
        started = perf_counter()

        def run_locally():
            try:
                return node_function(state, *args, **kwargs)
            finally:
                elapsed_ms = round((perf_counter() - started) * 1000, 2)
                print(f"[PlantGuard Trace] {node_name}: {elapsed_ms} ms")

        if LOCAL_ONLY:
            return run_locally()

        try:
            langfuse = get_client()
            observation = langfuse.start_as_current_observation(
                as_type="span",
                name=f"plantguard.{node_name}",
            )
            span = observation.__enter__()
        except Exception as exc:
            print(
                f"[PlantGuard Observability] Span unavailable for "
                f"{node_name}: {type(exc).__name__}"
            )
            return run_locally()

        node_error = None
        result = None

        try:
            result = node_function(state, *args, **kwargs)
        except BaseException as exc:
            node_error = exc

        elapsed_ms = round((perf_counter() - started) * 1000, 2)

        try:
            span.update(
                level="ERROR" if node_error else "DEFAULT",
                status_message=type(node_error).__name__ if node_error else None,
                metadata={
                    "node": node_name,
                    "outcome": "error" if node_error else "success",
                    "latency_ms": elapsed_ms,
                },
            )
        except Exception as exc:
            print(
                f"[PlantGuard Observability] Span update failed: "
                f"{type(exc).__name__}"
            )

        try:
            if node_error is not None:
                observation.__exit__(
                    type(node_error), node_error, node_error.__traceback__
                )
            else:
                observation.__exit__(None, None, None)
        except BaseException as exc:
            # Preserve an existing application error or LangGraph interrupt.
            if node_error is None:
                print(
                    f"[PlantGuard Observability] Span close failed: "
                    f"{type(exc).__name__}"
                )

        print(f"[PlantGuard Trace] {node_name}: {elapsed_ms} ms")

        if node_error is not None:
            raise node_error.with_traceback(node_error.__traceback__)

        return result

    return wrapper
