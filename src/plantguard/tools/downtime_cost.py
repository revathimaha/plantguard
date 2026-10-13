def calculate_downtime_cost(
    downtime_hours: float,
    cost_per_hour: float,
) -> float:
    """Calculate the estimated cost of equipment downtime."""

    return downtime_hours * cost_per_hour