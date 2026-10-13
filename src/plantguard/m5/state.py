from typing import TypedDict, Annotated
from operator import add


class PlantGuardState(TypedDict):
    event: dict
    root_cause_evidence: list[dict]
    recommendation: str
    safety_critical: bool
    route: str
    status: str
    approval_status: str
    approver_note: str
    audit_log: Annotated[list[str], add]
    rag_answer: str
    rag_sources: list[dict]
    error: str