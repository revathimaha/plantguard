from plantguard.m3.maintenance_history import (
    MaintenanceHistory,
)


def main():

    history = MaintenanceHistory(
        work_orders_path=(
            "data/plantguard/mock_api/work_orders.json"
        ),
        work_order_details_path=(
            "data/plantguard/mock_api/work_order_details.json"
        ),
    )

    records = history.get_asset_history(
        "VPW-CNC-MILL-03"
    )

    print(f"Found {len(records)} maintenance records")

    for record in records[:5]:
        print(record)


if __name__ == "__main__":
    main()