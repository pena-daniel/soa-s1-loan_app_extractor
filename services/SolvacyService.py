
from helpers.server import APP_HOST
import json
import logging
from spyne import Application, rpc, ServiceBase, Unicode,Fault, Integer, Decimal, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from helpers.Database import Database
from helpers.types import SolvencyStatusType,NonNegativeDecimal, NonNegativeInteger
from helpers.helper import validate_client_id


class SolvacyService(ServiceBase):
    @rpc(Unicode, NonNegativeDecimal, NonNegativeDecimal, NonNegativeInteger, _returns=SolvencyStatusType)
    def calculate_solvacy(ctx, client_id, income, expence, score):
        
        try:
            income = float(income)
            expenses = float(expence)
            sc = int(score)
        except Exception as e:
            print(f"Error parsing numeric inputs: {e}")
            raise Fault(faultcode="Client.ValidationError", faultstring="Invalid numeric inputs for decision")
    
        try:
            if not client_id or client_id.strip() == "":
                raise Fault(faultcode="Client.clientIdEmpty", faultstring="The client_id is not set or is empty.")
            
            if validate_client_id(client_id) is not None:
                raise Fault(faultcode="Client.ValidationError", faultstring=f"client_id '{client_id}' invalide. Pattern attendu: client-\\d{{3}}")
            
            if income < 0 or expenses < 0:
                raise Fault(faultcode="Client.ValidationError", faultstring="Income and expenses must be >= 0")
            status = "solvent" if (sc >= 700 and income > expenses) else "not_solvent"
            
            return SolvencyStatusType.SOLVENT if status == "solvent" else SolvencyStatusType.NOT_SOLVENT
            
        except Exception as e:
            logging.error(f"Error in calculate_solvacy service method: {e}")
            raise Fault(faultcode="Server.ValidationError", faultstring=str(e))
        
# Configuration de l'application Spyne
solvacy_app = Application(
    [SolvacyService],
    tns="services.SolvacyService",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

SOLVACY_APP = WsgiApplication(solvacy_app)
SOLVACY_APP_PORT = 8007
SOLVACY_APP_CLIENT_URL = f'http://{APP_HOST}:{SOLVACY_APP_PORT}/'
