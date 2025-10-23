from helpers.server import APP_HOST
import json
import logging
from spyne import Application, rpc, ServiceBase, Unicode,Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from helpers.Database import Database
from helpers.types import ClientIdentity

class ClientIdentityService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=ClientIdentity)
    def get_client_identity(ctx, clientName, clientEmail):
        if not clientName or clientName.strip() == "":
            raise Fault(faultcode="Client.clientNameEmpty", faultstring="The clientName is not set or is empty.")
        try:
            logging.info(f"GetClientinformations called for {clientEmail} - {clientName}")
            client = Database.get_client_infos_by_name(clientName)
            if not client:
                raise Fault(faultcode="Client.NotFound", faultstring=f"No client found with name {clientName}.")
            return ClientIdentity(clientId=client['clientId'], address=client['address'])
        except Exception as e:
            logging.error(f"Error in get_client_identity service method: {e}")
            raise Fault(faultcode="Server.DatabaseError", faultstring=str(e))
    
    
# App configuration
application_clid = Application(
    [ClientIdentityService], 
    tns='spyne.clientinfos',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

SERVICE_APP_CLIENT_INFO = WsgiApplication(application_clid)
SERVICE_APP_CLIENT_INFO_PORT = 8000
SERVICE_APP_CLIENT_INFO_URL = f'http://{APP_HOST}:{SERVICE_APP_CLIENT_INFO_PORT}/'