import csv
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "uk_services.csv")

def lookup_services(query: str):
    print("[TOOL] uk_services_lookup called with:", query)
    results = []
    query_lower = query.lower()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                query_lower in row["name"].lower()
                or query_lower in row["type"].lower()
                or query_lower in row["region"].lower()
                or (row["postcode"] and query_lower in row["postcode"].lower())
            ):
                results.append(row)

    return {"results": results}


# MCP entrypoint
def main(function: str, args: dict):
    if function == "lookup_services":
        return lookup_services(args["query"])
    else:
        return {"error": "Function not found"}

