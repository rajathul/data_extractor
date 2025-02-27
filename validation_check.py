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
        "crédito hipotecário",
        "empréstimo para compra de habitação",
        "empréstimo com garantia hipotecária",
        "crédito para aquisição de habitação própria"
    ]
    return any(lt in document for lt in loan_types)


def is_document_expired(document):
    match = re.search(r"As informações adiante apresentadas permanecem válidas até (\d{2}/\d{2}/\d{4})", document)
    if match:
        validity_date = datetime.strptime(match.group(1), "%d/%m/%Y")
        return validity_date < datetime.today()
    return False