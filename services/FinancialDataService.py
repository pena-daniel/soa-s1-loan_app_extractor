from helpers.server import APP_HOST
import json
import logging
from spyne import Application, rpc, ServiceBase, Unicode,Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from helpers.Database import Database
from helpers.types import FinancialsInfoType
from helpers.helper import validate_client_id

class FinancialService(ServiceBase):
    @rpc(Unicode, _returns=FinancialsInfoType)
    def get_financial_info(ctx, clientId):
        if not clientId or clientId.strip() == "":
            raise Fault(faultcode="Client.clientIdEmpty", faultstring="The clientId is not set or is empty.")
        
        if validate_client_id(clientId) is not None:
            raise Fault(faultcode="Client.ValidationError", faultstring=f"clientId '{clientId}' invalide. Pattern attendu: client-\\d{{3}}")
        
        try:
            logging.info(f"Get called for {clientId}")
            fi_infos = Database.get_financial_info(clientId)
            if not fi_infos:
                raise Fault(faultcode="Client.NotFound", faultstring=f"No financial info found for clientId {clientId}.")
            return FinancialsInfoType(monthlyIncome=fi_infos['income'], monthlyExpenses=fi_infos['expenses'])
        except Exception as e:
            logging.error(f"Error in get_financial_info service method: {e}")
            raise Fault(faultcode="Server.DatabaseError", faultstring=str(e))
    
    
# App configuration
application_fid = Application(
    [FinancialService], 
    tns='spyne.financialdata',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

FINANCE_APP_CLIENT_INFO = WsgiApplication(application_fid)
FINANCE_APP_PORT = 8005
FINANCE_APP_CLIENT_INFO_URL = f'http://{APP_HOST}:{FINANCE_APP_PORT}/'