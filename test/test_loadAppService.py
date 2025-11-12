import pytest
from unittest.mock import patch, MagicMock
from spyne import Fault
from services.LoanAppService import LoanExpenseAnalyzer
import json

# Données simulées
mock_extracted_info = {
    "client_name": "John Doe",
    "email": "john@example.com"
}

mock_client_info = {
    "clientId": "client-123",
    "address": "12 rue de Paris"
}

mock_financial_info = {
    "monthlyIncome": 5000,
    "monthlyExpenses": 2000
}

mock_credit_info = {
    "debt": 1000,
    "latePayments": 1,
    "hasBankruptcy": False
}

mock_score = 750

mock_solvency_info = "solvent"

mock_explanation = {
    "creditScoreExplanation": "Credit score of 750 is considered excellent.",
    "incomeVsExpensesExplanation": "Your income exceeds your expenses.",
    "creditHistoryExplanation": "No late payments and no bankruptcy."
}

def test_analyze_loan_expense_success():
    with patch("services.LoanAppService.Client") as MockClient:
        # Mock service calls
        extractor_mock = MockClient.return_value.service
        extractor_mock.extract_info.return_value = json.dumps(mock_extracted_info)

        client_mock = MockClient.return_value.service
        client_mock.get_client_identity.return_value = mock_client_info

        finance_mock = MockClient.return_value.service
        finance_mock.get_financial_info.return_value = mock_financial_info

        credit_mock = MockClient.return_value.service
        credit_mock.get_client_credit_history.return_value = mock_credit_info

        scoring_mock = MockClient.return_value.service
        scoring_mock.calculate_credit_scrore.return_value = mock_score

        solvency_mock = MockClient.return_value.service
        solvency_mock.calculate_solvacy.return_value = mock_solvency_info

        explanation_mock = MockClient.return_value.service
        explanation_mock.get_explaination.return_value = mock_explanation

        result = LoanExpenseAnalyzer.analyze_loan_expense(None, "Some content")

        assert result.name == "John Doe"
        assert result.identity["clientId"] == "client-123"
        assert result.financials["monthlyIncome"] == 5000
        assert result.creditHistory["score"] == mock_score
        assert result.solvencyStatus == mock_solvency_info
        assert result.explanations["creditScoreExplanation"] == mock_explanation["creditScoreExplanation"]

def test_analyze_loan_expense_empty_content():
    with pytest.raises(Fault) as excinfo:
        LoanExpenseAnalyzer.analyze_loan_expense(None, "  ")
    assert "Client.ContentEmpty" in str(excinfo.value)

def test_analyze_loan_expense_extraction_null():
    with patch("services.LoanAppService.Client") as MockClient:
        extractor_mock = MockClient.return_value.service
        extractor_mock.extract_info.return_value = None

        with pytest.raises(Fault) as excinfo:
            LoanExpenseAnalyzer.analyze_loan_expense(None, "Some content")
        assert "Server.NullResponse" in str(excinfo.value)
