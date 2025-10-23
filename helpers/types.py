from spyne import Integer, Unicode, ComplexModel, Enum, Decimal, Boolean
from enum import Enum as PyEnum

# form of possible extraction text types
TypeOfExtraction = PyEnum("TypeOfExtraction", ["line", "block"])

ClientId = Unicode(12, pattern="client-\d{3}", type_name="ClientId")  # type globale pour l'identifiant client

NonNegativeDecimal = Decimal(min_inclusive=0, context=None)
NonNegativeInteger = Integer(min_inclusive=0)

    
class CreditInfos(ComplexModel):
    clientId = ClientId
    debt = NonNegativeDecimal
    late = Boolean
    bankruptcy = Boolean

class FinanceInfos(ComplexModel):
    clientId = ClientId
    income = NonNegativeDecimal
    expense = NonNegativeDecimal

class UserInfos(ComplexModel):
    clientId = ClientId
    name = Unicode
    adresse = Unicode
    

class ClientIdentity(ComplexModel):
    clientId = ClientId
    address = Unicode

class Financials(ComplexModel):
    monthlyIncome = SpyneDecimal
    monthlyExpenses = SpyneDecimal

class CreditHistory(ComplexModel):
    debt = SpyneDecimal
    latePayments = Integer
    hasBankruptcy = Boolean

class CreditScoreType(ComplexModel):
    score = Integer

class Explanations(ComplexModel):
    creditScoreExplanation = Unicode
    incomeVsExpensesExplanation = Unicode
    creditHistoryExplanation = Unicode

class SolvencyReport(ComplexModel):
    name = Unicode
    identity = ClientIdentity
    financials = Financials
    creditHistory = CreditHistory
    creditScore = Integer
    solvencyStatus = Unicode
    explanations = Explanations
    
SolvencyStatusType = Enum('SOLVENT','NOT_SOLVENT', type_name='SolvencyStatus')