#  Discount Allocation System for Hospitals and Agents

##  Project Overview

This project implements a two-level **fair and configurable discount allocation system**:
1. **Hospital-Level Allocation** – Discounts are distributed among hospitals based on performance indicators.
2. **Agent-Level Allocation** – Each hospital's share is further divided among its sales agents using detailed performance metrics.

The system supports interactive input and is extensible through a configuration file (`config.json`) to adjust evaluation weights and discount limits.

---

##  Key Components

###  `allocator.py`
Allocates discounts to **agents** based on:
- Performance score
- Seniority
- Target achievement
- Client retention and satisfaction
- New client acquisition
- Upselling/Cross-selling
- Workload complexity

###  `red_health_allocation.py`
Full interactive program that:
- Collects inputs for hospitals and agents
- Allocates discounts in two stages (hospitals → agents)
- Provides justifications for each decision
- Outputs JSON summary and human-readable results

###  `config.json`
Customizable parameters:
- Weightages for hospital and agent features
- Discount boundaries
- Global kitty (total budget to distribute)

###  `test_cases.txt`
Includes unit test descriptions:
- Normal case
- Identical scores
- Edge case with rounding and limits

---

##  Approach

### Hospital Allocation:
- Normalize metrics (performance, revenue, customer rating, service standard)
- Compute weighted score
- Allocate discount proportionally
- Enforce min/max bounds

### Agent Allocation:
- Normalize individual agent metrics
- Score agents using a weighted sum
- Allocate hospital's kitty to agents proportionally
- Ensure fairness via boundary constraints

Each allocation includes a **textual justification** using raw input values.

---

##  Assumptions Made

- All input metrics are **non-negative** and fall within expected ranges.
- **Weight sums** do not exceed 1 for normalization purposes.
- Agents and hospitals receive at least the **minimum specified** discount.
- If all scores are equal, allocation is done **uniformly**.
- Interactive mode is used for realistic data entry and validation.

---

##  How to Run

> Requires Python 3.x

 ```bash
python red_health_allocation.py
```


### Option 1: Interactive Full Allocation (Hospitals + Agents)

```bash
python red_health_allocation.py
```

##  Test Cases

###  Normal Case (Multiple Hospitals and Agents)

**Input:**
- 3 Hospitals, each with 3 Agents
- Diverse performance metrics

**Expected Output:**
- Hospital-level allocation based on combined metrics
- Agent-level allocation proportionally from hospital share
- Final output includes summary and JSON structure

**Sample Output Excerpt:**
```
Agent H2_A1 → ₹106711.63
Justification: Agent H2_A1 has performance (90.0), retention (80.0%), satisfaction (70.0), upselling rate (80.0%), 55.0 months of experience, workload complexity (4.0).
...
Agent H3_A3 → ₹20146.55
Justification: Agent H3_A3 has performance (20.0), retention (39.0%), satisfaction (40.0), upselling rate (45.0%), 12.0 months of experience, workload complexity (2.0).
```

###  All-Same Scores Case

**Input:**
- All hospitals and agents have identical scores

**Expected Output:**
- Equal allocation among all hospitals
- Equal distribution to each agent within their hospital

###  Rounding Edge Case

**Input:**
- Values that push boundaries of rounding (e.g., 1 agent, 1 hospital, extreme scores)

**Expected Output:**
- Allocation properly rounded
- Does not exceed total kitty or violate min/max rules