# runner.py - simplified version for guaranteed A4 HTML output
import json
import os
import subprocess
import sys

# -----------------------------
# CONFIGURATION
# -----------------------------
SYSTEM_NAME = "uk_homelessness_agent_system"
AGENTS_DIR = "agents"
TOOLS_DIR = "tools"
SCENARIOS_DIR = "evaluation"
OUTPUT_DIR = "logs"
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "summary_report.json")
PYTHON_EXEC = sys.executable

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# LOAD AGENT AND TOOL DEFINITIONS
# -----------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_all_definitions():
    agents = []
    tools = []

    for file in os.listdir(AGENTS_DIR):
        if file.endswith(".json"):
            agents.append(load_json(os.path.join(AGENTS_DIR, file)))

    for folder in os.listdir(TOOLS_DIR):
        tool_json = os.path.join(TOOLS_DIR, folder, "tool.json")
        handler_path = os.path.join(TOOLS_DIR, folder)
        if os.path.exists(tool_json):
            definitions = load_json(tool_json)
            definitions["code_path"] = handler_path
            tools.append(definitions)

    print(f"[INFO] Loaded {len(agents)} agents and {len(tools)} tools.\n")
    return agents, tools

# -----------------------------
# CREATE SYSTEM & SESSION
# -----------------------------
def create_system_and_session(agents, tools):
    agents_file = "temp_agents.json"
    tools_file = "temp_tools.json"
    with open(agents_file, "w", encoding="utf-8") as f:
        json.dump(agents, f)
    with open(tools_file, "w", encoding="utf-8") as f:
        json.dump(tools, f)

    try:
        subprocess.run([
            PYTHON_EXEC, "-m", "google.adk.cli.cli_create",
            "--system_name", SYSTEM_NAME,
            "--agents_file", agents_file,
            "--tools_file", tools_file
        ], check=False, text=True)

        subprocess.run([
            PYTHON_EXEC, "-m", "google.adk.cli.cli_deploy",
            "--system_name", SYSTEM_NAME
        ], check=False, text=True)

    finally:
        if os.path.exists(agents_file):
            os.remove(agents_file)
        if os.path.exists(tools_file):
            os.remove(tools_file)

# -----------------------------
# RUN SCENARIO
# -----------------------------
def run_scenario(user_input):
    result_eval = subprocess.run([
        PYTHON_EXEC, "-m", "google.adk.cli.cli_eval",
        "--system_name", SYSTEM_NAME,
        "--message", json.dumps(user_input)
    ], capture_output=True, text=True)

    try:
        response_json = json.loads(result_eval.stdout)
    except json.JSONDecodeError:
        response_json = {"raw_output": result_eval.stdout.strip()}

    return {
        "system_id": "single_system",
        "session_id": "single_session",
        "response": response_json
    }

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    agents, tools = load_all_definitions()
    create_system_and_session(agents, tools)

    scenario_files = [f for f in os.listdir(SCENARIOS_DIR) if f.endswith(".json")]
    if not scenario_files:
        print(f"[ERROR] No scenario JSON files found in {SCENARIOS_DIR}")
        exit(1)

    summary_report = []

    for scenario_file in scenario_files:
        scenario_path = os.path.join(SCENARIOS_DIR, scenario_file)
        print(f"\n=== RUNNING SCENARIO: {scenario_file} ===\n")

        scenario = load_json(scenario_path)
        user_input = scenario.get("user_input")
        if not user_input:
            print("[WARNING] 'user_input' not found, skipping scenario.")
            continue

        output = run_scenario(user_input)
        response = output.get("response", {})

        # --- Simplified A4 HTML output ---
        filename = os.path.join(OUTPUT_DIR, f"{scenario['scenario_name'].replace(' ','_')}.html")

        html_content = f"""
        <html>
        <head>
        <style>
        body {{ font-family: Arial; margin: 20px; }}
        h1 {{ color: #2E8B57; }}
        </style>
        </head>
        <body>
        <h1>Action Plan for {user_input.get('name')}</h1>
        <p>Risk Level: {response.get('risk_level', 'N/A')}</p>
        <p>Services: {', '.join([s['name'] for s in response.get('matched_services', [])])}</p>
        <p>Documents Required: {', '.join(response.get('documents_required', []))}</p>
        <p>Eligibility: {response.get('eligibility_assessment', 'N/A')}</p>
        </body>
        </html>
        """

        # Save HTML
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Update response for validation
        response["html_report"] = filename
        response["pdf_file_path"] = None
        response["summary_text"] = f"Plan generated for {user_input.get('name')}"
        response["mode"] = "html-only"
        output["response"] = response

        # Save scenario output
        output_file = os.path.join(
            OUTPUT_DIR, f"{os.path.splitext(scenario_file)[0]}_output.json"
        )
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

        # Prepare summary snippet
        response_text = ""
        for k, v in response.items():
            if isinstance(v, str):
                response_text += v + " "
            elif isinstance(v, dict):
                response_text += " ".join(str(vv) for vv in v.values()) + " "
        response_text = response_text.strip()[:200]

        summary_report.append({
            "scenario_file": scenario_file,
            "name": user_input.get("name"),
            "age": user_input.get("age"),
            "postcode": user_input.get("postcode"),
            "financial_status": user_input.get("financial_status"),
            "health_conditions": user_input.get("health_conditions"),
            "system_id": output["system_id"],
            "session_id": output["session_id"],
            "response_snippet": response_text
        })

        print(f"[INFO] Output saved to {output_file}")
        print(json.dumps(output, indent=2))

    # Save summary report
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2)

    print(f"\n=== ALL SCENARIOS COMPLETED ===")
    print(f"[INFO] Summary report saved to {SUMMARY_FILE}\n")
