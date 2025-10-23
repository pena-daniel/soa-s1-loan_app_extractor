import logging
from helpers.server import APP_HOST, runService
from services.LoanAppService import LOAN_EXPENSE_APP_PORT, LOAN_EXPENSE_APP_EXTRACTOR

# global logging configuration
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Serveur WSGI for loan expense analyzer
    runService("LoanExpenseAnalyzer", APP_HOST, LOAN_EXPENSE_APP_PORT, LOAN_EXPENSE_APP_EXTRACTOR)