import re
from spyne import Fault

CLIENT_ID_PATTERN = re.compile(r"^client-\d{3}$")

def validate_client_id(clientId):
    if not CLIENT_ID_PATTERN.match(clientId):
        raise Fault(faultcode="Client.ValidationError", faultstring=f"clientId '{clientId}' invalide. Pattern attendu: client-\\d{{3}}")