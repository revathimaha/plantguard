from plantguard.tools.sensor_history import get_sensor_history
from plantguard.tools.downtime_cost import calculate_downtime_cost
from plantguard.tools.inventory import check_spare_parts
from plantguard.tools.technician_schedule import get_technician_schedule
import json
from litellm import completion

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_sensor_history",
            "description": (
                "Retrieve recent sensor telemetry for a specific asset."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "asset_tag": {
                        "type": "string",
                        "description": "Asset tag of the machine.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of recent records to return.",
                    },
                },
                "required": ["asset_tag"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_downtime_cost",
            "description": (
                "Calculate the financial cost of equipment downtime."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "downtime_hours": {
                        "type": "number",
                        "description": "Number of hours of downtime.",
                    },
                    "cost_per_hour": {
                        "type": "number",
                        "description": "Cost of downtime per hour.",
                    },
                },
                "required": [
                    "downtime_hours",
                    "cost_per_hour",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_spare_parts",
            "description": (
                "Check inventory information for a spare part."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "part_number": {
                        "type": "string",
                        "description": "Spare-part number to look up.",
                    },
                },
                "required": ["part_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_technician_schedule",
            "description": (
                "Retrieve technician availability from the technician calendar."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "technician_id": {
                        "type": "string",
                        "description": "Technician identifier.",
                    },
                    "date": {
                        "type": "string",
                        "description": "Optional date in YYYY-MM-DD format.",
                    },
                },
                "required": ["technician_id"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "get_sensor_history": get_sensor_history,
    "calculate_downtime_cost": calculate_downtime_cost,
    "check_spare_parts": check_spare_parts,
    "get_technician_schedule": get_technician_schedule,
}


class MaintenanceAgent:

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def run(self, user_request: str):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a plant maintenance assistant. "
                    "Use the available tools when operational data "
                    "is required. Do not invent tool results. "
                    "Do not claim that sensor values are normal, abnormal, "
                    "safe, or within engineering limits unless those limits "
                    "are explicitly provided by a tool or the input data. "
                    "Do not infer causes from sensor trends unless supported "
                    "by the available data."
                ),
            },
            {
                "role": "user",
                "content": user_request,
            },
        ]

        while True:

            response = completion(
                model=self.model,
                api_key=self.api_key,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )

            message = response.choices[0].message

            # No tool requested → final answer
            if not message.tool_calls:
                return message.content

            # Add the assistant's tool request to the conversation
            messages.append(message)

            # Execute requested tools
            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name
                arguments = json.loads(
                    tool_call.function.arguments
                )

                tool_function = TOOL_FUNCTIONS[tool_name]

                result = tool_function(**arguments)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )