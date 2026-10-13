from plantguard.m2.agent import MaintenanceAgent


def main():
    agent = MaintenanceAgent(
        model="groq/openai/gpt-oss-20b",
        api_key="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",
    )
    result = agent.run(
        """
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
    )

    print("\nAgent response:")
    print(result)


if __name__ == "__main__":
    main()