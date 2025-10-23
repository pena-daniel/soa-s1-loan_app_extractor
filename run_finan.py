import logging
from helpers.server import APP_HOST, runService
from services.FinancialDataService import FINANCE_APP_PORT, FINANCE_APP_CLIENT_INFO

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for InfoExtractor service
    runService("InfoExtractor", APP_HOST, FINANCE_APP_PORT, FINANCE_APP_CLIENT_INFO)