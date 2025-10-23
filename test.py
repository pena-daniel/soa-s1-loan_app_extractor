from services.ServiceExtractor import SERVICE_APP_EXTRACTOR_URL
from services.ClientInfos import SERVICE_APP_CLIENT_INFO_URL
from services.LoanAppService import SERVICE_APP_LOAN_URL
from zeep import Client
from helpers import api

client = Client(f"{SERVICE_APP_LOAN_URL}?wsdl")
result = client.service.analyze_loan_expense("""
client_name: John Doe
adresse: 123 Rue de la Liberté, 75001 Paris, France
email: john.doe@email.com
phone_numer: +33 123 456 789
loan_amount: 200000 EUR
loan_times: 20 ans
description: Maison à deux étages avec jardin, située dans un quartier résidentiel calme.
""")
print(result)

# client = Client(f"{SERVICE_APP_CLIENT_INFO_URL}?wsdl")
# result = client.service.get_client_identity("John Doe")
# print(result)