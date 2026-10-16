import os

from src.plantguard.m2.agent import MaintenanceAgent


def main():
    model = os.environ.get("PLANTGUARD_LLM_MODEL") or "groq/openai/gpt-oss-20b"
    api_key = os.environ.get("PLANTGUARD_LLM_API_KEY") or os.environ.get(
        "GROQ_API_KEY"
    )
    if not api_key:
        raise RuntimeError(
            "Set GROQ_API_KEY (or PLANTGUARD_LLM_API_KEY) in the environment."
        )

    agent = MaintenanceAgent(model=model, api_key=api_key)

    user_request = """
    Investigate maintenance requirements for asset VPW-CNC-MILL-03.

    Check:
    1. Recent sensor history for this asset.
    2. Spare-part inventory for part number VPW-P-00003.
    3. Technician availability for technician VPW-T-001 on 2026-08-12.

    Also calculate the downtime cost assuming:
    - 4 hours of downtime
    - 15000 INR per hour

    Report the tool results clearly.

    Do not invent engineering limits, fault diagnoses,
    part requirements, or technician assignments.
    """

    result = agent.run(user_request)

    print("\nAgent response:")
    print(result)


if __name__ == "__main__":
    main()
