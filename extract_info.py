import re

def extract_info(document):
    extracted_data = {}

    patterns = {
        "tipo de taxa": r"Tipo de taxa de juro:\s*(.*?)(?=\.|\n)",
        "montante e moeda": r"Montante e moeda do\s*empréstimo a conceder:\s*([\d\s\.,]+)\s*([a-zA-Z]{3})",
        "duração do empréstimo": r"Duração do empréstimo:\s*(\d+\s*meses)",
        "primeira tan": r"TAN\s*(?:\(base\)|contratada)?\s?:?\s*([\d\.,]+)",
        "segundo tan": r"(?:Em resultado da contratação facultativa dos produtos e serviços financeiros descritos na Secção \"8. Obrigações adicionais\", a TAN será de:|A TAN será de):?\s*([\d\.,]+)",
        "terceira tan": r"(?:A TAN será de|a tan será de):?\s*([\d\.,]+)",
        "quarta tan": r"a TAN será de:\s*([\d\.,]+)%,\s*resultante da soma",
        "número de prestações": r"Número de prestações:\s*(\d+)",
        "valor do imóvel": r"Valor do imóvel\s*:\s*([\d\.,]+)\s*EUR",
        "spread": r"spread\s*(?:base)?\s*de\s*([\d\.,]+)",
        "mtic (base)": r"MTIC \(base\)\s*:\s*([\d\.,]+)",
        "mtic (contratada)": r"MTIC \(contratada\)\s*:\s*([\d\.,]+)",
        "taeg (base)": r"TAEG \(base\)\s*:\s*([\d\.,]+)",
        "taeg (contratada)": r"TAEG \(contratada\)\s*:\s*([\d\.,]+)",
        "montante da prestação": r"Montante da prestação\s*inicial:\s*([\d\.,]+)\s*EUR",
        "index": r"indexante:\s*(.*?)"
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