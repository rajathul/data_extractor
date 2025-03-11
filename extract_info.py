import re

def extract_info(document):
    extracted_data = {}

    document = document.strip()

    patterns = {
        "tipo de taxa": r"tipo de taxa de juro:\s*([\w\s]+?)(?:\.|\n)",
        "montante e moeda": r"montante e moeda\s*(?:do\s*)?([\d\s\.,]+)\s*([a-zA-Z]{3}|€)",
        "duração do empréstimo": r"duração (?:do empréstimo|do)\s*(\d+)\s*meses?",
        "primeira tan": r"(?:taxa de juro\s*\(tan\)|taxa de juro fixa):\s*([\d\s\.,]+)%",
        "segundo tan": r"tan será de:\s*([\d\s\.,]+)%",
        "terceira tan": r"(?:taxa de juro variável:\s*|durante o período de taxa variável:\s*)([\d\s\.,]+)%",
        "quarta tan": r"(?:a tan será de:\s*|a tan será de\s*)([\d\s\.,]+)%\,\s*resultante da soma",
        "número de prestações": r"número de prestações.*?(\d+)",
        "valor do imóvel": r"valor do imóvel\s*(?:€\s*|:\s*)([\d\s\.,]+)\s*€?",
        "spread": r"spread (?:base )?de\s*([\d\s\.,]+)%",
        "mtic (base)": r"(?:(?:mtic \(base\)\s*€\s*)|(?:montante total a\s*))([\d\s\.,]+)",
        "mtic (base) 1": r"([\d\.,]+€)\s*de custo total do",
        "mtic (contratada)": r"mtic \(contratada\)\s*€\s*([\d\s\.,]+)",
        "taeg (base)": r"(?:taeg \(base\)|taeg aplicável\s*ao\s*|TAEG:|a taeg aplicávelao)\s*([\d\s\.,]+)%",
        "taeg (contratada)": r"(?:taeg \(contratada\)|TAEG c/ vendas associadas facultativas|taxa anual de encargos)\s*([\d\s\.,]+)%",
        "montante da prestação": r"montante da prestação(?: inicial)?:?\s*([\d\s\.,]+)\s*(EUR|€)",
        "index": r"euribor (3|6|12) meses"
    }

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