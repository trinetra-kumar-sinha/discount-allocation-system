import json

# Prompt the user for high-level input values
num_hospitals = int(input("Enter number of hospitals: "))
global_kitty = float(input("Enter total discount kitty amount (₹): "))

# Default weights for hospital-level evaluation criteria
hospital_weights = {
    "performanceScore": 0.3,
    "revenue": 0.3,
    "customerRating": 0.2,
    "serviceStandard": 0.2
}

# Default weights for agent-level evaluation criteria
agent_weights = {
    "performanceScore": 0.2,
    "seniorityMonths": 0.1,
    "targetAchievedPercent": 0.15,
    "activeClients": 0.1,
    "customerRetentionRate": 0.1,
    "newClientAcquisition": 0.1,
    "clientSatisfactionScore": 0.1,
    "upsellingCrossSellingRate": 0.1,
    "workloadComplexity": 0.05
}

# Discount boundaries for hospitals and agents
min_hospital_discount = float(input("Enter minimum discount per hospital (₹): "))
max_hospital_discount = float(input("Enter maximum discount per hospital (₹): "))
min_agent_discount = float(input("Enter minimum discount per agent (₹): "))
max_agent_discount = float(input("Enter maximum discount per agent (₹): "))


# Utility to normalize values (between 0 and 1)
def normalize(val, max_val):
    return val / max_val if max_val != 0 else 0

# Calculate a weighted score using a data dictionary and associated weights
def compute_score(data, weights):
    return sum(data[k] * weights[k] for k in weights)

# Generate a textual justification string for an agent's discount allocation
def justify(agent):
    r = agent["raw"]
    return (
        f"Agent {agent['id']} has performance ({r['performanceScore']}), "
        f"retention ({r['customerRetentionRate']}%), satisfaction ({r['clientSatisfactionScore']}), "
        f"upselling rate ({r['upsellingCrossSellingRate']}%), {r['seniorityMonths']} months of experience, "
        f"workload complexity ({r['workloadComplexity']})."
    )

# Input data for each agent
def collect_agent_input(agent_id):
    print(f"\nEnter details for Agent {agent_id}:")
    performanceScore = float(input("  Performance Score (0–100): "))
    seniorityMonths = float(input("  Seniority in Months: "))
    targetAchievedPercent = float(input("  Target Achieved (%): "))
    activeClients = float(input("  Active Clients: "))
    customerRetentionRate = float(input("  Customer Retention Rate (%): "))
    newClientAcquisition = float(input("  New Clients Acquired: "))
    clientSatisfactionScore = float(input("  Client Satisfaction (0–100): "))
    upsellingCrossSellingRate = float(input("  Upselling/Cross-selling Rate (%): "))
    workloadComplexity = float(input("  Workload Complexity (1–5): "))

    # Return agent dictionary with normalized and raw values
    return {
        "id": str(agent_id),
        "performanceScore": normalize(performanceScore, 100),
        "seniorityMonths": normalize(seniorityMonths, 60),
        "targetAchievedPercent": normalize(targetAchievedPercent, 100),
        "activeClients": normalize(activeClients, 100),
        "customerRetentionRate": normalize(customerRetentionRate, 100),
        "newClientAcquisition": normalize(newClientAcquisition, 50),
        "clientSatisfactionScore": normalize(clientSatisfactionScore, 100),
        "upsellingCrossSellingRate": normalize(upsellingCrossSellingRate, 100),
        "workloadComplexity": normalize(workloadComplexity, 5),
        "raw": {
            "performanceScore": performanceScore,
            "seniorityMonths": seniorityMonths,
            "targetAchievedPercent": targetAchievedPercent,
            "activeClients": activeClients,
            "customerRetentionRate": customerRetentionRate,
            "newClientAcquisition": newClientAcquisition,
            "clientSatisfactionScore": clientSatisfactionScore,
            "upsellingCrossSellingRate": upsellingCrossSellingRate,
            "workloadComplexity": workloadComplexity
        }
    }

# Input data for each hospital
def collect_hospital_input(hospital_id):
    print(f"\nEnter details for Hospital {hospital_id}:")
    performanceScore = float(input("  Performance Score (0–100): "))
    revenue = float(input("  Revenue in Lakhs: "))
    customerRating = float(input("  Customer Rating (0–5): "))
    serviceStandard = float(input("  Service Standard (0–5): "))

    # Return hospital dictionary with normalized and raw values
    return {
        "id": f"H{hospital_id}",
        "performanceScore": normalize(performanceScore, 100),
        "revenue": normalize(revenue, 1000),
        "customerRating": normalize(customerRating, 5),
        "serviceStandard": normalize(serviceStandard, 5),
        "raw": {
            "performanceScore": performanceScore,
            "revenue": revenue,
            "customerRating": customerRating,
            "serviceStandard": serviceStandard
        },
        "agents": []
    }

# Ask user to enter custom weights or use predefined ones
def get_custom_weights(default_weights, entity_name):
    choice = input(f"\nDo you want to fill weightage of {entity_name} parameters?\n"
                   f"  1. Yes\n"
                   f"  2. Go with predefined weightage\n"
                   f"Enter choice (1/2): ")

    if choice.strip() == '1':
        print(f"\nEnter custom weights for {entity_name} parameters (total should be 1.0):")
        custom_weights = {}
        total = 0.0
        for param in default_weights:
            while True:
                try:
                    val = float(input(f"  Weight for '{param}': "))
                    if 0 <= val <= 1:
                        custom_weights[param] = val
                        total += val
                        break
                    else:
                        print("    Please enter a value between 0 and 1.")
                except:
                    print("    Invalid input. Please enter a numeric value.")
        if round(total, 2) != 1.0:
            print(f"\n⚠️ Total weight entered = {total} ≠ 1.0 → Reverting to default weights.\n")
            return default_weights
        return custom_weights
    else:
        print(f"✅ Using predefined weightage for {entity_name}.")
        return default_weights

# Main execution flow
def main():
    global hospital_weights, agent_weights

    # Allow weight customization
    hospital_weights = get_custom_weights(hospital_weights, "hospital")
    agent_weights = get_custom_weights(agent_weights, "agent")

    print(f"\n💰 Total Kitty Available: ₹{global_kitty}")

    hospitals = []
    hospital_scores = []

    # Step 1: Collect hospital data and calculate scores
    for i in range(1, num_hospitals + 1):
        hospital = collect_hospital_input(i)
        hospitals.append(hospital)
        hospital_scores.append(compute_score(hospital, hospital_weights))

    total_hospital_score = sum(hospital_scores)

    # Step 2: Allocate kitty to hospitals based on performance
    for i, hospital in enumerate(hospitals):
        share = hospital_scores[i] / total_hospital_score if total_hospital_score else 0
        raw_discount = share * global_kitty
        hospital_kitty = max(min_hospital_discount, min(max_hospital_discount, round(raw_discount, 2)))
        hospital["allocated_kitty"] = hospital_kitty

        print(f"\n🏥 Hospital {hospital['id']} allocated ₹{hospital_kitty} based on performance.")

        # Step 3: Input and store agents for each hospital
        num_agents = int(input(f"  Enter number of agents in Hospital {hospital['id']}: "))
        for j in range(1, num_agents + 1):
            agent = collect_agent_input(f"{hospital['id']}_A{j}")
            hospital["agents"].append(agent)

    # Step 4: Allocate hospital kitty to agents based on agent scores
    final_allocations = []
    for hospital in hospitals:
        agents = hospital["agents"]
        if not agents:
            continue

        agent_scores = [compute_score(agent, agent_weights) for agent in agents]
        total_agent_score = sum(agent_scores)

        for agent, score in zip(agents, agent_scores):
            share = score / total_agent_score if total_agent_score else 0
            raw_discount = share * hospital["allocated_kitty"]
            assigned = max(min_agent_discount, min(max_agent_discount, round(raw_discount, 2)))

            alloc = {
                "id": agent["id"],
                "assignedDiscount": assigned,
                "hospitalId": hospital["id"],
                "justification": justify(agent)
            }

            final_allocations.append(alloc)

            print(f"\nAgent {alloc['id']} (Hospital {alloc['hospitalId']}) → ₹{alloc['assignedDiscount']}")
            print(f"Justification: {alloc['justification']}")

    # Step 5: Print final JSON output and textual summary
    output = {
        "summary": f"Total kitty ₹{global_kitty} distributed to hospitals and their agents.",
        "allocations": final_allocations
    }

    print("\n\nJSON OUTPUT:")
    print(json.dumps(output, indent=2))

    print("\nSUMMARY:\n")
    print(f"Total kitty ₹{global_kitty} distributed to hospitals and their agents:\n")
    for alloc in final_allocations:
        print(f"Agent {alloc['id']} → ₹{alloc['assignedDiscount']}")
        print(f"Justification: {alloc['justification']}\n")


# Entry point
if __name__ == "__main__":
    main()
