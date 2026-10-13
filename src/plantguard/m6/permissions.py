from functools import wraps
import inspect


AGENT_SCOPES = {
    "intake": {"event", "plan", "findings", "audit_log", "error"},
    "researcher": {"findings", "audit_log", "error"},
    "maintenance": {"recommendation", "findings", "audit_log", "error"},
    "procurement": {"procurement_result", "findings", "audit_log", "error"},
    "manual_rag": {"findings", "audit_log", "error"},
    "safety_reviewer": {
        "safety_review",
        "approval_required",
        "findings",
        "audit_log",
        "error",
    },
    "recommendation_reviewer": {
    "recommendation_review",
    "findings",
    "audit_log",
    "error",
},
}


def validate_agent_update(agent_name: str, update: dict) -> dict:
    """Reject updates to fields outside an agent's write permissions."""
    if agent_name not in AGENT_SCOPES:
        raise ValueError(f"Unknown agent: {agent_name}")

    if not isinstance(update, dict):
        raise TypeError("Agent update must be a dictionary")

    forbidden = set(update) - AGENT_SCOPES[agent_name]
    if forbidden:
        raise PermissionError(
            f"{agent_name} cannot update fields: {sorted(forbidden)}"
        )

    return update


def scoped(agent_name: str):
    """Enforce an agent's allowed output fields."""
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                return validate_agent_update(agent_name, result)
            return async_wrapper

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return validate_agent_update(agent_name, result)

        return wrapper
    return decorator


def scoped_state(agent_name: str, state: dict) -> dict:
    """Return a copy of state containing only fields allowed for this agent."""
    if agent_name not in AGENT_SCOPES:
        raise ValueError(f"Unknown agent: {agent_name}")

    allowed = AGENT_SCOPES[agent_name]
    return {
        key: value
        for key, value in state.items()
        if key in allowed
    }
