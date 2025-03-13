def reg_patterns():
    patterns = {
        "tipo de taxa": r"tipo de taxa de juro:\s*([\S\s]+?)(?:\.|\n)",
        "montante e moeda": r"montante e moeda\s*(?:do\s*)?([\d\s\.,]+)\s*([a-zA-Z]{3}|€)",
        "duração do empréstimo": r"duração (?:do empréstimo|do)\s*:?\s*(\d+)\s*meses?",
        "primeira tan": r"(?:taxa de juro\s*\(tan\)|taxa de juro fixa):\s*([\d\s\.,]+)%",
        "segundo tan": r"tan será de:\s*([\d\s\.,]+)%",
        "terceira tan": r"(?:taxa de juro variável:\s*|durante o período de taxa variável:\s*)([\d\s\.,]+)%",
        "quarta tan": r"(?:a tan será de:\s*|a tan será de\s*)([\d\s\.,]+)%\,\s*resultante da soma",
        "número de prestações": r"número de prestações.*?(\d+)",
        "valor do imóvel": r"(?:valor do imóvel|valor presumido do|para efeitos da presente ficha)\s*€?\s*([\d.,]+)€?",
        "spread": r"spread (?:base )?de\s*([\d\s\.,]+)%",
        "mtic (base)": r"(?:(?:mtic \(base\)\s*€\s*)|(?:montante total a\s*))([\d\s\.,]+)",
        "mtic (base) 1": r"([\d\.,]+€)\s*de custo total do",
        "mtic (contratada)": r"mtic \(contratada\)\s*€\s*([\d\s\.,]+)",
        "taeg (base)": r"(?:taeg \(base\)|taeg aplicável\s*ao\s*|TAEG:|a taeg aplicávelao)\s*([\d\s\.,]+)%",
        "taeg (contratada)": r"(?:taeg \(contratada\)|TAEG c/ vendas associadas facultativas|taxa anual de encargos)\s*([\d\s\.,]+)%",
        "montante da prestação": r"montante da prestação(?: inicial)?:?\s*([\d\s\.,]+)\s*(EUR|€)",
        "index": r"euribor (3|6|12) meses"
    }

    return patterns