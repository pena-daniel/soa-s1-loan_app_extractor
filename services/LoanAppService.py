import logging
import json
from spyne import Application, rpc, ServiceBase, Unicode,Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from helpers.server import APP_HOST
from services.ServiceExtractor import SERVICE_APP_EXTRACTOR_URL
from services.ClientInfos import SERVICE_APP_CLIENT_INFO_URL
from zeep import Client
from zeep.helpers import serialize_object

# Service Web principal for loan expense analysis
class LoanExpenseAnalyzer(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def analyze_loan_expense(ctx, content):
        try:
            if not content or content.strip() == "":
                raise Fault(faultcode="Client.ContentEmpty", faultstring="The content is not set or is empty.")
            # extract information from api call locahost:8000/extract_info
            info_extractor_client = Client(f"{SERVICE_APP_EXTRACTOR_URL}?wsdl")
            extracted_infos = info_extractor_client.service.extract_info(content)
            
            # check if i have a returned value
            if not extracted_infos:
                raise Fault(faultcode="Server.NullResponse", faultstring="No information could be extracted from the provided content.")
        
            extracted_infos = json.loads(extracted_infos)
            
            logging.info("Infos extracted for loan expense analysis")
            
            # get client informations
            client_info_service = Client(f"{SERVICE_APP_CLIENT_INFO_URL}?wsdl")
            clients_infos = client_info_service.service.get_client_identity(extracted_infos.get("client_name"), extracted_infos.get("email"))
            
            # check if i have a returned value
            if not clients_infos:
                raise Fault(faultcode="Server.NullResponse", faultstring="No client information found for the extracted client name.")
            
            clients_infos = serialize_object(clients_infos)
            
            logging.info("Client informations retrieved for loan expense analysis")
            
            # get financial informations
            finance_info_service = Client(f"{SERVICE_APP_CLIENT_INFO_URL}?wsdl")
            financial_infos = finance_info_service.service.get_financial_info(clients_infos.get("clientId"))      
            financial_info = serialize_object(financial_infos)
            
            
            # get credit history
            credit_info_service = Client(f"{SERVICE_APP_CLIENT_INFO_URL}?wsdl")
            credit_history = credit_info_service.service.get_client_credit_history(clients_infos.get("clientId"))
            credit_info = serialize_object(credit_history)
            
            # analyze loan expense based on extracted info
            results = {
                "client_id": clients_infos.get("clientId"),
                "name": extracted_infos.get("client_name"),
                "finances_history": financial_info,
                "credit_history": credit_info
            }
            
            return json.dumps(clients_infos+financial_info, ensure_ascii=False, indent=2)
        
        except ConnectionError as ce:
            raise Fault(faultcode="Server.ConnectionError",
                        faultstring=f"We can't reach the server {ce}.")
        
        except Exception as e:
            logging.error(f"Error in analyze_loan_expense service method: {e}")
            raise Fault(faultcode="Server", faultstring=str(e))
        
        
# App configuration for loan expense analyzer
application_loan_expense = Application(
    [LoanExpenseAnalyzer],
    tns='spyne.loanexpenseanalyzer',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

LOAN_EXPENSE_APP_EXTRACTOR = WsgiApplication(application_loan_expense)
LOAN_EXPENSE_APP_PORT = 8001
SERVICE_APP_LOAN_URL = f'http://{APP_HOST}:{LOAN_EXPENSE_APP_PORT}/'