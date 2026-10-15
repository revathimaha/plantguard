from operator import add
from typing import Annotated, Any, TypedDict


class PlantGuardTeamState(TypedDict, total=False):
    event: dict
    plan: list[str]
    findings: Annotated[list[dict], add]
    recommendation: dict[str, Any] | str
    procurement_result: dict
    safety_review: dict
    approval_required: bool
    approval_status: str
    revision_count: int
    status: str
    next_agent: str
    error: str
    audit_log: Annotated[list[str], add]
    recommendation_review: dict
    refusal: dict[str, Any]