
import os
from pathlib import Path

from fastmcp import Client

from src.plantguard.m6.permissions import scoped


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MCP_SERVER_PATH = PROJECT_ROOT / "src/plantguard/m6/mcp_server.py"


def _mcp_config() -> dict:
    return {
        "mcpServers": {
            "plantguard": {
                "command": os.environ.get(
                    "PYTHON", str(PROJECT_ROOT / ".venv/bin/python")
                ),
                "args": [str(MCP_SERVER_PATH)],
            }
        }
    }


async def _lookup_inventory(part_number: str) -> dict:
    """Look up a spare part through the PlantGuard MCP server."""
    async with Client(_mcp_config()) as client:
        result = await client.call_tool(
            "inventory_lookup",
            {"part_number": part_number},
        )

        if getattr(result, "is_error", False):
            raise RuntimeError("MCP inventory lookup failed")

        data = result.structured_content
        if data is None:
            raise RuntimeError("Inventory tool returned no structured data")

        return data


async def _create_mock_order(
    part_number: str,
    quantity: int,
    approval_reference: str,
) -> dict:
    """Request a simulated purchase order through MCP."""
    async with Client(_mcp_config()) as client:
        result = await client.call_tool(
            "create_mock_purchase_order",
            {
                "part_number": part_number,
                "quantity": quantity,
                "approval_reference": approval_reference,
            },
        )

        if getattr(result, "is_error", False):
            raise RuntimeError("MCP mock order creation failed")

        data = result.structured_content
        if data is None:
            raise RuntimeError("Mock order tool returned no structured data")

        return data


@scoped("procurement")
async def procurement_agent(state: dict) -> dict:
    """
    Check inventory and optionally request a simulated purchase order.

    An order is not requested by default. A supplied approval reference
    is required for the mock-order path, but is not independently verified
    against a trusted approval system.
    """
    part_number = state.get("part_number")

    if not isinstance(part_number, str) or not part_number.strip():
        return {
            "procurement_result": {
                "status": "not_requested",
                "message": "No part number was supplied.",
            },
            "audit_log": [
                "procurement: skipped; no part number supplied"
            ],
        }

    part_number = part_number.strip()

    # Inventory lookup never places an order.
    try:
        inventory = await _lookup_inventory(part_number)
    except Exception as exc:
        return {
            "procurement_result": {
                "status": "error",
                "part_number": part_number,
                "message": f"Inventory lookup failed: {type(exc).__name__}",
                "purchase_authorized": False,
            },
            "audit_log": ["procurement: MCP inventory lookup failed"],
            "error": "Procurement inventory lookup failed.",
        }

    result = {
        "status": "success",
        "part_number": part_number,
        "inventory": inventory,
        "purchase_authorized": False,
    }

    # Preserve read-only behavior unless a mock order is explicitly requested.
    if state.get("create_mock_order") is not True:
        result["message"] = "Inventory checked; no order requested."
        return {
            "procurement_result": result,
            "audit_log": [
                f"procurement: inventory lookup completed for {part_number}"
            ],
        }

    approval_reference = state.get("procurement_approval_reference")
    if (
        not isinstance(approval_reference, str)
        or not approval_reference.strip()
    ):
        result.update({
            "status": "approval_required",
            "message": "A procurement approval reference is required.",
        })
        return {
            "procurement_result": result,
            "audit_log": [
                "procurement: mock order not created; approval reference missing"
            ],
        }

    quantity = state.get("order_quantity", 1)
    if (
        not isinstance(quantity, int)
        or isinstance(quantity, bool)
        or quantity < 1
    ):
        result.update({
            "status": "invalid_quantity",
            "message": "Order quantity must be a positive integer.",
        })
        return {
            "procurement_result": result,
            "audit_log": ["procurement: invalid mock order quantity"],
        }

    # Request a simulated order; never execute a real purchase.
    try:
        order = await _create_mock_order(
            part_number=part_number,
            quantity=quantity,
            approval_reference=approval_reference.strip(),
        )
    except Exception as exc:
        result.update({
            "status": "error",
            "message": f"Mock order failed: {type(exc).__name__}",
        })
        return {
            "procurement_result": result,
            "audit_log": ["procurement: mock order creation failed"],
            "error": "Mock order creation failed.",
        }

    result["mock_order"] = order
    result["status"] = (
        "mock_order_created"
        if order.get("created") is True
        else "order_not_created"
    )
    result["purchase_authorized"] = False

    return {
        "procurement_result": result,
        "audit_log": [
            f"procurement: mock order request processed for {part_number}"
        ],
    }
