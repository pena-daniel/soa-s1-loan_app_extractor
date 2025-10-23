import re
from spyne import Fault

CLIENT_ID_PATTERN = re.compile(r"^client-\d{3}$")

def validate_client_id(client_id: str):
    if not CLIENT_ID_PATTERN.match(client_id):
        raise Fault(faultcode="Client.ValidationError", faultstring=f"clientId '{client_id}' invalide. Pattern attendu: client-\\d{{3}}")