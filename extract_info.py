import re
from patterns import reg_patterns

def extract_info(document):
    extracted_data = {}

    document = document.strip()

    patterns = reg_patterns()

    for key, pattern in patterns.items():
        match = re.search(pattern, document, re.IGNORECASE)
        if match:
            if key == "montante e moeda":
                extracted_data[key] = (match.group(1), match.group(2))
            elif key == "index":
                extracted_data[key] = f"Euribor {match.group(1)} meses"
            else:
                extracted_data[key] = match.group(1)
        else:
            extracted_data[key] = "not found"

    # Special handling for "mista" type in "tipo de taxa" field
    if extracted_data.get("tipo de taxa") == "mista":
        tan_matches = re.findall(r"taxa de juro \(tan\):\s*([\d.,]+)%", document, re.IGNORECASE)
        if len(tan_matches) == 2:
            extracted_data["primeira tan"] = tan_matches[0]
            extracted_data["segundo tan"] = tan_matches[1]

    mtic_base = extracted_data.get("mtic (base)", "").strip()
    mtic_base_1 = extracted_data.get("mtic (base) 1", "").strip()

    if not mtic_base or mtic_base == "not found":
        extracted_data["mtic (base)"] = mtic_base_1
    elif mtic_base_1 and mtic_base != mtic_base_1:
        extracted_data["mtic (base)"] = mtic_base_1  # Prioritize base 1 if they differ

    # Remove unwanted keys
    extracted_data.pop("mtic (base) 1", None)

    return extracted_data