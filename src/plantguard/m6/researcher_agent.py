import os
from pathlib import Path

from fastmcp import Client

from src.plantguard.m6.permissions import scoped

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MCP_SERVER_PATH = PROJECT_ROOT / "src/plantguard/m6/mcp_server.py"


async def _collect_evidence(asset_tag: str, limit: int = 10) -> dict:
    """Retrieve sensor history and safety policy through MCP."""

    async with Client({
        "mcpServers": {
            "plantguard": {
                "command": os.environ.get(
                    "PYTHON", str(PROJECT_ROOT / ".venv/bin/python")
                ),
                "args": [str(MCP_SERVER_PATH)],
            }
        }
    }) as client:
        result = await client.call_tool(
            "sensor_history_lookup",
            {"asset_tag": asset_tag, "limit": limit},
        )

        if getattr(result, "is_error", False):
            raise RuntimeError(
                f"sensor_history_lookup failed: {result}"
            )            

        sensor_data = result.structured_content
        if sensor_data is None:
            raise RuntimeError("Missing structured sensor-history response")

        policy_contents = await client.read_resource(
            "plantguard://policy/safety"
        )
        policy_text = "\n".join(
            item.text for item in policy_contents
            if hasattr(item, "text")
        )

        return {
            "sensor_history": sensor_data,
            "safety_policy": policy_text,
        }


@scoped("researcher")
async def researcher_agent(state: dict) -> dict:
    """Collect evidence without making safety or approval decisions."""

    event = state.get("event")
    if not isinstance(event, dict):
        return {
            "findings": [{
                "agent": "researcher",
                "status": "error",
                "message": "Missing maintenance event.",
            }],
            "audit_log": ["researcher: missing maintenance event"],
        }

    asset_tag = event.get("asset_tag")
    if not isinstance(asset_tag, str) or not asset_tag.strip():
        return {
            "findings": [{
                "agent": "researcher",
                "status": "error",
                "message": "Missing asset_tag.",
            }],
            "audit_log": ["researcher: missing asset tag"],
        }

    try:
        evidence = await _collect_evidence(asset_tag)
    except Exception as exc:
        print(f"Researcher MCP error: {type(exc).__name__}: {exc}")
        return {
            "findings": [{
                "agent": "researcher",
                "status": "error",
                "message": f"Evidence retrieval failed: {type(exc).__name__}",
            }],
            "audit_log": [
                f"researcher: MCP retrieval failed for {asset_tag}"
            ],
            "error": "Researcher evidence retrieval failed.",
        }

    sensor_data = evidence["sensor_history"]

    return {
        "findings": [{
            "agent": "researcher",
            "status": "success",
            "asset_tag": asset_tag,
            "sensor_history": sensor_data,
            "safety_policy": evidence["safety_policy"],
        }],
        "audit_log": [
            f"researcher: retrieved {sensor_data.get('count', 0)} "
            f"sensor records for {asset_tag}"
        ],
    }
