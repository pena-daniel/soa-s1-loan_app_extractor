import logging
from helpers.server import APP_HOST, runService
from services.SolvacyService import SOLVACY_APP, SOLVACY_APP_PORT

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for SolvacyService service
    runService("SolvacyService", APP_HOST, SOLVACY_APP_PORT, SOLVACY_APP)