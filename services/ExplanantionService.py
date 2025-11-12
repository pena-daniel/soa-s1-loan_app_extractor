from helpers.server import APP_HOST
import json
import logging
from spyne import Application, rpc, ServiceBase, Unicode,Fault, Integer, Decimal, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from helpers.Database import Database
from helpers.types import SolvencyStatusType,NonNegativeDecimal, NonNegativeInteger, ExplanationsType
from helpers.helper import validate_client_id

class ExplanationService(ServiceBase):
    @rpc(Decimal, NonNegativeInteger, NonNegativeDecimal, NonNegativeDecimal, NonNegativeDecimal, Boolean, _returns=ExplanationsType)
    def get_explaination(ctx, score, income, expence, debt, late, hasBankruptcy):
        
        try:
            income = float(income)
            expenses = float(expence)
            sc = int(score)
            debt = float(debt)
            late = float(late)
            hasBankruptcy = bool(hasBankruptcy)
        except Exception as e:
            print(f"Error parsing numeric inputs: {e}")
            raise Fault(faultcode="Client.ValidationError", faultstring="Invalid numeric inputs for decision")
        
        try:
            if income < 0 or expenses < 0 or debt < 0:
                raise Fault(faultcode="Client.ValidationError", faultstring="Numeric inputs must be >= 0")
            
            # simple explanation logic
            cs = "excellent" if sc >= 800 else ("acceptable" if sc >= 650 else "poor")
            creditScoreExplanation = f"Credit score of {sc} is considered {cs}."
            # incomes and expense explanation for the report
            in_explanation = "your income exceeds your expenses." if income > expenses else "your expenses exceed your income."
            incomeVsExpensesExplanation = f"{in_explanation} Income = {income}, Expenses = {expenses}."
            
            # credit history explanation
            cr_explanantion = "no late payments and no bankruptcy." if (late == 0 and not hasBankruptcy) else \
                             ("some late payments but no bankruptcy." if (late > 0 and not hasBankruptcy) else \
                                "a history of bankruptcy." )
                             
            creditHistoryExplanation = f"{cr_explanantion} Debt = {debt}, Late Payments = {late}, Bankruptcy = {hasBankruptcy}."
            
            return ExplanationsType(
                creditScoreExplanation=creditScoreExplanation,
                incomeVsExpensesExplanation=incomeVsExpensesExplanation,
                creditHistoryExplanation=creditHistoryExplanation
            )
        except Exception as e:
            logging.error(f"Error in Explain service method: {e}")
            raise Fault(faultcode="Server.ValidationError", faultstring=str(e))
    
# Configuration de l'application Spyne
explanation_app = Application(
    [ExplanationService],
    tns="services.ExplanationService",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

EXPLANATION_APP = WsgiApplication(explanation_app)
EXPLANATION_APP_PORT = 8002
EXPLANATION_APP_CLIENT_URL = f'http://{APP_HOST}:{EXPLANATION_APP_PORT}/'