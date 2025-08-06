import numpy as np

# Normalize a value between 0 and 1 using min-max normalization
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) if max_val > min_val else 0.0

# Main function to allocate discounts among agents based on weighted parameters
def allocate_discounts(input_data, config_data):
    agents = input_data['agents']                # List of sales agents with their attributes
    kitty = input_data['siteKitty']              # Total budget available for allocation
    weights = config_data['weights']             # Weight assigned to each agent parameter
    min_discount = config_data['minPerAgent']    # Minimum discount assignable to an agent
    max_discount = config_data['maxPerAgent']    # Maximum discount assignable to an agent

    # Extract all agent parameters (e.g., performanceScore, retention rate, etc.)
    param_keys = list(weights.keys())

    # Collect parameter values for all agents to calculate normalization statistics
    stats = {key: [agent.get(key, 0) for agent in agents] for key in param_keys}
    min_vals = {key: min(vals) for key, vals in stats.items()}  # Minimum values per parameter
    max_vals = {key: max(vals) for key, vals in stats.items()}  # Maximum values per parameter

    scores = []  # To store computed weighted scores for each agent

    # Calculate weighted normalized score for each agent
    for agent in agents:
        score = 0
        for key in param_keys:
            val = agent.get(key, 0)                              # Get agent's value for the parameter
            norm_val = normalize(val, min_vals[key], max_vals[key])  # Normalize the value
            score += norm_val * weights[key]                    # Multiply with weight and add to score
        scores.append(score)

    total_score = sum(scores)  # Sum of all agent scores to compute proportions
    allocations = []           # Final result list with allocation and justification per agent

    # Assign discounts based on proportional score
    for agent, score in zip(agents, scores):
        proportion = score / total_score if total_score > 0 else 1 / len(agents)  # Prevent division by zero
        raw_discount = round(proportion * kitty, 2)  # Calculate raw discount amount
        assigned = max(min_discount, min(max_discount, raw_discount))  # Clamp within min/max range

        # Create a detailed justification for this allocation
        justification = (
            f"Agent {agent['id']} has performance ({agent.get('performanceScore', 'N/A')}), "
            f"client retention ({agent.get('customerRetentionRate', 'N/A')}%), "
            f"satisfaction ({agent.get('clientSatisfactionScore', 'N/A')}), "
            f"upselling rate ({agent.get('upsellingCrossSellingRate', 'N/A')}%), "
            f"{agent.get('seniorityMonths', 'N/A')} months of experience, "
            f"workload complexity ({agent.get('workloadComplexity', 'N/A')})."
        )

        # Add allocation result
        allocations.append({
            'id': agent['id'],
            'assignedDiscount': round(assigned, 2),
            'justification': justification
        })

    # Return dictionary of allocations
    return {'allocations': allocations}
