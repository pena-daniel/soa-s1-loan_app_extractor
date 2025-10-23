import logging
from helpers.server import APP_HOST, runService
from services.ClientInfos import SERVICE_APP_CLIENT_INFO_PORT, SERVICE_APP_CLIENT_INFO

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for get client informations service
    runService("ClientInfoApp", APP_HOST, SERVICE_APP_CLIENT_INFO_PORT, SERVICE_APP_CLIENT_INFO)
