import re

POSTCODE_MAP = {
    "SW1A 1AA": (51.5010, -0.1416),
    "N1 9QZ": (51.5340, -0.1050),
    "N17 6AA": (51.5941, -0.0691)
}

def postcode_to_geo(postcode: str):
    postcode = postcode.upper().strip()
    postcode = re.sub(r"\s+", " ", postcode)
    return {
        "postcode": postcode,
        "lat": POSTCODE_MAP.get(postcode, None),
        "lon": POSTCODE_MAP.get(postcode, None)
    }

def main(function: str, args: dict):
    if function == "postcode_to_geo":
        return postcode_to_geo(args["postcode"])
    else:
        return {"error": "Function not found"}
