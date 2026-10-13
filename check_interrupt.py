
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from typing import TypedDict


class State(TypedDict, total=False):
    status: str


def approval_node(state: State) -> dict:
    decision = interrupt({"message": "Approve this test?"})
    return {
        "status": "approved" if decision.get("approved") else "rejected"
    }


builder = StateGraph(State)
builder.add_node("approval", approval_node)
builder.add_edge(START, "approval")
builder.add_edge("approval", END)

graph = builder.compile(checkpointer=MemorySaver())

result = graph.invoke(
    {"status": "pending"},
    config={"configurable": {"thread_id": "interrupt-test"}},
)

print("Result:", result)
print("Interrupt present:", bool(result.get("__interrupt__")))
