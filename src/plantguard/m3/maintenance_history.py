import json
from pathlib import Path


class MaintenanceHistory:

    def __init__(
        self,
        work_orders_path: str,
        work_order_details_path: str,
    ):
        self.work_orders_path = Path(work_orders_path)
        self.work_order_details_path = Path(
            work_order_details_path
        )

    def load_history(self) -> list[dict]:
        with self.work_orders_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            work_orders = json.load(f)

        with self.work_order_details_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            details = json.load(f)

        details_by_id = {
            item["work_order_id"]: item
            for item in details
        }

        history = []

        for work_order in work_orders:
            work_order_id = work_order["work_order_id"]

            record = {
                **work_order,
                **details_by_id.get(work_order_id, {}),
            }

            history.append(record)

        return history

    def get_asset_history(
        self,
        asset_tag: str,
    ) -> list[dict]:

        history = self.load_history()

        return [
            record
            for record in history
            if record["asset_tag"] == asset_tag
        ]