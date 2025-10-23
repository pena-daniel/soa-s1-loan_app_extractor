import logging
from helpers.server import APP_HOST, runService
from services.ExplanantionService import EXPLANATION_APP_PORT, EXPLANATION_APP

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for InfoExtractor service
    runService("ExplanationService", APP_HOST, EXPLANATION_APP_PORT, EXPLANATION_APP)