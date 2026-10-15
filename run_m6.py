import json
import os

from src.plantguard.m6.graph import build_graph


def main():
    api_key = os.environ.get("PLANTGUARD_LLM_API_KEY") or os.environ.get(
        "GROQ_API_KEY"
    )
    if not api_key:
        raise RuntimeError(
            "Set GROQ_API_KEY (or PLANTGUARD_LLM_API_KEY) in the environment."
        )

    graph = build_graph()

    event = {
        "event_id": "M6-DEMO-001",
        "asset_tag": "VPW-CNC-MILL-03",
        "raw_text": (
            "Spindle vibration has been climbing over the last two shifts "
            "on the CNC mill. What maintenance action is recommended?"
        ),
        "readings": {},
    }

    result = graph.invoke(
        {"event": event},
        config={
            "configurable": {"thread_id": "m6-demo-001"},
            "recursion_limit": 30,
        },
    )

    print("\nMulti-agent team result:")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
