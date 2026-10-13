import os
import sqlite3
import uuid

from langgraph.checkpoint.sqlite import SqliteSaver

from src.plantguard.m5.graph import build_graph
from langgraph.types import Command


DB_PATH = "plantguard_m5.sqlite"
THREAD_ID = os.getenv(
    "M5_THREAD_ID",
    f"m5-{uuid.uuid4()}",
)

def main():
    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False,
    )

    saver = SqliteSaver(conn)
    saver.setup()

    workflow = build_graph()
    graph = workflow.compile(checkpointer=saver)

    config = {
        "configurable": {
            "thread_id": THREAD_ID,
        }
    }

    initial_state = {
        "event": {
            "event_id": "M5-001",
            "source": "test",
            "asset_tag": "CNC-MILL-03",
            "raw_text": "Electrical maintenance required on energized equipment",
            # "raw_text": "Routine inspection required for CNC-MILL-03",
        },
        "root_cause_evidence": [],
        "rag_answer": "",
        "rag_sources": [],
        "recommendation": "",
        "safety_critical": False,
        "route": "",
        "status": "",
        "approval_status": "",
        "approver_note": "",
        "audit_log": [],
        "error": "",
    }

    result = graph.invoke(
        initial_state,
        config,
    )

    print("\n=== M5 WORKFLOW RESULT ===")
    print("status:", result.get("status"))
    print("route:", result.get("route"))
    print("safety_critical:", result.get("safety_critical"))
    print("recommendation:", result.get("recommendation"))
    print("rag_sources:", result.get("rag_sources"))
    print("audit_log:", result.get("audit_log"))

    snapshot = graph.get_state(config)

    print("\n=== CHECKPOINT ===")
    print("next:", snapshot.next)
    print("thread_id:", THREAD_ID)
    print("database:", DB_PATH)

    # print("\n=== RESUMING WITH HUMAN APPROVAL ===")

    # final = graph.invoke(
    #     Command(
    #         resume={
    #             "action": "approved",
    #             "note": "Approved after safety review.",
    #         }
    #     ),
    #     config,
    # )

    # print("\n=== FINAL RESULT ===")
    # print("status:", final.get("status"))
    # print("approval_status:", final.get("approval_status"))
    # print("approver_note:", final.get("approver_note"))
    # print("audit_log:", final.get("audit_log"))

    # final_snapshot = graph.get_state(config)

    # print("\n=== FINAL CHECKPOINT ===")
    # print("next:", final_snapshot.next)


if __name__ == "__main__":
    main()