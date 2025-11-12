import pytest
from spyne import Fault
from services.ScoringService import ScoringService

def test_calculate_credit_score_success():
    # client_id valide, pas de faillite
    result = ScoringService.calculate_credit_scrore(None, "client-123", 1000.0, 2, False)
    expected_score = int(round(1000.0 - 0.1*1000.0 - 50*2 - 0))
    assert result == expected_score

def test_calculate_credit_score_with_bankruptcy():
    result = ScoringService.calculate_credit_scrore(None, "client-123", 500.0, 1, True)
    expected_score = int(round(1000.0 - 0.1*500.0 - 50*1 - 200))
    assert result == expected_score

def test_calculate_credit_score_invalid_client_id_empty():
    with pytest.raises(Fault) as excinfo:
        ScoringService.calculate_credit_scrore(None, "", 1000.0, 1, False)
    assert "Client.clientIdEmpty" in str(excinfo.value)

def test_calculate_credit_score_invalid_client_id_pattern():
    with pytest.raises(Fault) as excinfo:
        ScoringService.calculate_credit_scrore(None, "invalid-456", 1000.0, 1, False)
    assert "Client.ValidationError" in str(excinfo.value)
    assert "invalide" in str(excinfo.value)

def test_calculate_credit_score_debt_not_numeric():
    with pytest.raises(Fault) as excinfo:
        ScoringService.calculate_credit_scrore(None, "client-123", "abc", 1, False)
    assert "Debt must be numeric" in str(excinfo.value)
