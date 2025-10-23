import logging
from helpers.server import APP_HOST, runService
from services.ScoringService import SCORING_APP, SCORING_APP_PORT

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for InfoExtractor service
    runService("ScoreService", APP_HOST, SCORING_APP_PORT, SCORING_APP)