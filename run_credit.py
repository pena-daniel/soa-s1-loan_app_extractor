import logging
from helpers.server import APP_HOST, runService
from services.CreditService import CREDIT_BUREAU_APP_PORT, CREDIT_BUREAU_APP_CLIENT

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for InfoExtractor service
    runService("CreditInfo", APP_HOST, CREDIT_BUREAU_APP_PORT, CREDIT_BUREAU_APP_CLIENT)