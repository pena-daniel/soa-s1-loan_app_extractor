from helpers.server import APP_HOST
import json
import logging
from spyne import Application, rpc, ServiceBase, Unicode,Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from helpers.Database import Database
from helpers.types import CreditHistoryType
from helpers.helper import validate_client_id
        
class CreditBureauService(ServiceBase):
    @rpc(Unicode, _returns=CreditHistoryType)
    def get_client_credit_history(ctx, clientId):
        try:
            if not clientId or clientId.strip() == "":
                raise Fault(faultcode="Client.clientIdEmpty", faultstring="The clientId is not set or is empty.")
            
            if validate_client_id(clientId) is not None:
                raise Fault(faultcode="Client.ValidationError", faultstring=f"clientId '{clientId}' invalide. Pattern attendu: client-\\d{{3}}")
            
            logging.info(f"GetClientCreditHistory called for {clientId}")
            credit_history = Database.get_credit_info(clientId)
            
            if not credit_history:
                raise Fault(faultcode="Client.NotFound", faultstring=f"No credit history found for clientId {clientId}.")
            
            return CreditHistoryType(debt=credit_history['debt'], latePayments=credit_history['late'], hasBankruptcy=credit_history['bankruptcy'])
        except Exception as e:
            logging.error(f"Error in GetClientCreditHistory service method: {e}")
            raise Fault(faultcode="Server.DatabaseError", faultstring=str(e))
    

# App configuration for Credit Bureau Service
application_credit_bureau = Application(
    [CreditBureauService],
    tns='spyne.creditbureau',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)
CREDIT_BUREAU_APP_CLIENT = WsgiApplication(application_credit_bureau)
CREDIT_BUREAU_APP_PORT = 8006
CREDIT_BUREAU_APP_CLIENT_URL = f'http://{APP_HOST}:{CREDIT_BUREAU_APP_PORT}/'