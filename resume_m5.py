import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from src.plantguard.m5.graph import build_graph


DB_PATH = "plantguard_m5.sqlite"
THREAD_ID = "m5-40ee2b7b-2027-420d-975d-363aaf700594"


def main():
    # This represents a NEW process after restart.
    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False,
    )

    saver = SqliteSaver(conn)
    saver.setup()

    # Rebuild the graph from code.
    workflow = build_graph()
    graph = workflow.compile(checkpointer=saver)

    config = {
        "configurable": {
            "thread_id": THREAD_ID,
        }
    }

    # Recover the persisted state.
    snapshot = graph.get_state(config)

    print("=== RECOVERED CHECKPOINT ===")
    print("thread_id:", THREAD_ID)
    print("next:", snapshot.next)
    print("status:", snapshot.values.get("status"))
    print("route:", snapshot.values.get("route"))
    print(
        "safety_critical:",
        snapshot.values.get("safety_critical"),
    )

    # Resume the paused human approval.
    final = graph.invoke(
        Command(
            resume={
                "action": "rejected",
                "note": "Rejected during safety review.",
            }
        ),
        config,
    )

    print("\n=== AFTER RESUME ===")
    print("status:", final.get("status"))
    print(
        "approval_status:",
        final.get("approval_status"),
    )
    print(
        "approver_note:",
        final.get("approver_note"),
    )

    final_snapshot = graph.get_state(config)

    print("\n=== FINAL CHECKPOINT ===")
    print("next:", final_snapshot.next)


if __name__ == "__main__":
    main()