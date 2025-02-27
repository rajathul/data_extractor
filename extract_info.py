import re

def extract_info(document):
    extracted_data = {}

    patterns = {
        "tipo de taxa": r"tipo de taxa de juro:\s*([\w\s]+?)(?:\.|\n)",
        "montante e moeda": r"montante e moeda do\s*([\d\s\.,]+)\s*([a-zA-Z]{3})",
        "duração do empréstimo": r"duração do empréstimo:\s*(\d+\s*meses)",
        "primeira tan": r"(?:taxa de juro\s*\(tan\)|taxa de juro fixa):\s*([\d\.,]+)%",
        "segundo tan": r"tan será de:\s*([\d\.,]+)%",
        "terceira tan": r"taxa de juro variável:\s*([\d\.,]+)%",
        "quarta tan": r"a tan será de:\s*([\d\.,]+)%,\s*resultante da soma",
        "número de prestações": r"número de prestações.*?(\d+)",
        "valor do imóvel": r"valor do imóvel\s*(?:€\s*|:\s*)([\d\.,]+)\s*€?",
        "spread": r"spread (?:base )?de\s*([\d\.,]+)%",
        "mtic (base)": r"(?:mtic \(base\)\s*€\s*|montante total a\s*)([\d\.,]+)",
        "mtic (contratada)": r"mtic \(contratada\)\s*€\s*([\d\.,]+)",
        "taeg (base)": r"taeg \(base\)\s*([\d\.,]+)%",
        "taeg (contratada)": r"taeg \(contratada\)\s*([\d\.,]+)%",
        "montante da prestação": r"montante da prestação\s*([\d\.,]+)\s*EUR",
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

    return extracted_data