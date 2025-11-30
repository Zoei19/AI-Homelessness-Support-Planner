import json
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
LOG_DIR = "logs"
EVAL_DIR = "evaluation"
EXPECTED_FILE = os.path.join(EVAL_DIR, "expected_outputs.md")

# -----------------------------
# LOAD EXPECTED OUTPUTS (simplified for matching)
# -----------------------------
EXPECTED = {
    "High Risk Rough Sleeping in London": {
        "A1": "High Risk",
        "A2_services": ["St Mungo’s Emergency Shelter", "Glass Door Winter Night Shelter", "Outreach teams"],
        "A3_docs": ["ID documents", "GP letter"],
        "A4_mode": "HTML"
    },
    "Domestic Abuse Refuge Case": {
        "A1": "Domestic Abuse",
        "A2_services": ["Women's Aid Refuge"],
        "A3_docs": ["Refuge documentation"],
        "A4_mode": "HTML"
    },
    "Family with Children Facing Eviction": {
        "A1": "Children Priority",
        "A2_services": ["Manchester Homelessness Hub"],
        "A3_docs": ["Prevention duty context"],
        "A4_mode": "HTML"
    }
}

# -----------------------------
# VALIDATION LOGIC
# -----------------------------
def validate_scenario(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    scenario_name = os.path.basename(log_file).replace("_output.json", "").replace("_", " ")
    response = data.get("response", {})

    result = {}
    # A1 validation
    risk_level = response.get("risk_level") or response.get("A1_risk_level")
    expected_risk = EXPECTED.get(scenario_name, {}).get("A1")
    result["A1_pass"] = risk_level == expected_risk

    # A2 validation
    matched_services = response.get("matched_services", []) or response.get("A2_services", [])
    expected_services = EXPECTED.get(scenario_name, {}).get("A2_services", [])
    service_names = [s.get("name") for s in matched_services]
    result["A2_pass"] = all(s in service_names for s in expected_services)

    # A3 validation
    documents = response.get("documents_required", []) or response.get("A3_docs", [])
    expected_docs = EXPECTED.get(scenario_name, {}).get("A3_docs", [])
    result["A3_pass"] = all(d in documents for d in expected_docs)

    # A4 validation
    mode = response.get("mode") or response.get("A4_mode")
    result["A4_pass"] = mode is not None  # just check HTML/PDF generated

    return scenario_name, result

# -----------------------------
# MAIN EXECUTION
# -----------------------------
summary_results = {}
for file in os.listdir(LOG_DIR):
    if file.endswith("_output.json"):
        scenario_name, result = validate_scenario(os.path.join(LOG_DIR, file))
        summary_results[scenario_name] = result

# Print results
print("\n=== VALIDATION RESULTS ===")
for scenario, res in summary_results.items():
    print(f"\nScenario: {scenario}")
    for agent, passed in res.items():
        print(f"  {agent}: {passed}")

# Optional: save summary JSON
with open(os.path.join(LOG_DIR, "validation_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary_results, f, indent=2)
