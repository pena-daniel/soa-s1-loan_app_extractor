import logging
from helpers.server import APP_HOST, runService
from services.ServiceExtractor import SERVICE_APP_EXTRACTOR_PORT, SERVICE_APP_EXTRACTOR

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for InfoExtractor service
    runService("InfoExtractor", APP_HOST, SERVICE_APP_EXTRACTOR_PORT, SERVICE_APP_EXTRACTOR)