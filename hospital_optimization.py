#  Hospital Resource Optimizer (Console Version)
# Author: Your Name

from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import pandas as pd

# Step 1: Define the hospital data
departments = ["ER", "ICU", "GeneralWard"]
demand = {"ER": 40, "ICU": 12, "GeneralWard": 55}

# Step 2: Available resources
total_nurses = 25
total_beds = 80

# Step 3: Create the optimization problem
model = LpProblem(name="hospital-resource-optimizer", sense=LpMaximize)

# Step 4: Define decision variables
nurses = {d: LpVariable(name=f"nurses_{d}", lowBound=0) for d in departments}
beds = {d: LpVariable(name=f"beds_{d}", lowBound=0) for d in departments}

# Step 5: Objective function (maximize resource utilization)
model += lpSum([nurses[d] + beds[d] for d in departments])

# Step 6: Constraints
model += lpSum([nurses[d] for d in departments]) <= total_nurses, "NurseLimit"
model += lpSum([beds[d] for d in departments]) <= total_beds, "BedLimit"

# Each department can't exceed its demand
for d in departments:
    model += beds[d] <= demand[d], f"BedDemand_{d}"

# Step 7: Solve
model.solve()

# Step 8: Display results
results = []
for d in departments:
    unmet = demand[d] - beds[d].value()
    results.append({
        "Department": d,
        "Demand": demand[d],
        "Nurses": int(nurses[d].value()),
        "Beds": int(beds[d].value()),
        "Unmet Demand": max(0, unmet)
    })

df = pd.DataFrame(results)
print("\n Hospital Resource Optimization Results\n")
print(df.to_string(index=False))

print("\nTotal Nurses Used:", sum([nurses[d].value() for d in departments]))
print("Total Beds Used:", sum([beds[d].value() for d in departments]))

