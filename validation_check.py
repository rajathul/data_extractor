import re
from datetime import datetime


def is_valid_document(document):
    document_type = determine_document_type(document)

    if not contains_loan_type(document):
        return False, document_type, "It is not a housing loan document. No fields extracted."

    if is_document_expired(document):
        return False, document_type, "The document has expired. No fields extracted."

    return True, document_type, "The document is valid."


def determine_document_type(document):
    return "Simulation" if "fine de simulação" in document else "Not simulation"


def contains_loan_type(document):
    loan_types = [
        "crédito à habitação",
        "Crédito habitação",
        "crédito hipotecário",
        "empréstimo para compra de habitação",
        "empréstimo com garantia hipotecária",
        "crédito para aquisição de habitação própria"
    ]
    return any(lt in document for lt in loan_types)


month_map = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}


def is_document_expired(document):
    match = re.search(
        r"as informações adiante apresentadas permanecem válidas até (\d{1,2})(?:/(\d{2})/| de (\w+) de )(\d{4})",
        document)

    if match:
        day, month_numeric, month_word, year = match.groups()
        month = month_numeric if month_numeric else month_map.get(month_word.lower())

        if month:
            validity_date = datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
            return validity_date < datetime.today()

    return False