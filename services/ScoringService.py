
from helpers.server import APP_HOST
import json
import logging
from spyne import Application, rpc, ServiceBase, Unicode,Fault, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from helpers.Database import Database
from helpers.types import NonNegativeDecimal, NonNegativeInteger
from helpers.helper import validate_client_id


class ScoringService(ServiceBase):
    @rpc(Unicode, NonNegativeDecimal, NonNegativeInteger, Boolean, _returns=NonNegativeInteger)
    def calculate_credit_scrore(ctx, client_id, debt, late, hasBankruptcy):
        try:
            d = float(debt)
        except:
            raise Fault(faultcode="Client.ValidationError", faultstring="Debt must be numeric")
        
        try:
            if not client_id or client_id.strip() == "":
                raise Fault(faultcode="Client.clientIdEmpty", faultstring="The client_id is not set or is empty.")
            
            if validate_client_id(client_id) is not None:
                raise Fault(faultcode="Client.ValidationError", faultstring=f"client_id '{client_id}' invalide. Pattern attendu: client-\\d{{3}}")
            
            score_float = 1000.0 - 0.1 * d - 50.0 * int(late) - (200.0 if bool(hasBankruptcy) else 0.0)
            score_int = int(round(score_float))
            
            return score_int
            
        except Exception as e:
            logging.error(f"Error in calculate_credit_scrore service method: {e}")
            raise Fault(faultcode="Server.ValidationError", faultstring=str(e))
        
# Configuration de l'application Spyne
scoring_app = Application(
    [ScoringService],
    tns="services.ScoringService",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

SCORING_APP = WsgiApplication(scoring_app)
SCORING_APP_PORT = 8006
SCORING_APP_CLIENT_URL = f'http://{APP_HOST}:{SCORING_APP_PORT}/'
