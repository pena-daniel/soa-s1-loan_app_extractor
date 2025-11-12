import pytest
from unittest.mock import patch, MagicMock
from spyne import Fault
from services.CreditService import CreditBureauService
from helpers.types import CreditHistoryType

# Exemple de client "mocké"
mock_financial_data = {
        "client_id": "client-001",
        "debt": 5000,
        "late": 2,
        "bankruptcy": False
}

def test_get_client_credit_history_success():
    # On mock Database.get_client_infos_by_name pour retourner un client valide
    with patch("services.CreditService.Database.get_credit_info", return_value=mock_financial_data):
        result = CreditBureauService.get_client_credit_history(None, "client-001")
        assert isinstance(result, CreditHistoryType)
        assert result.debt == 5000
        assert result.latePayments == 2
        assert result.hasBankruptcy == False



def test_get_client_credit_history_empty_client_id():
    with pytest.raises(Fault) as excinfo:
        CreditBureauService.get_client_credit_history(None, "")
    assert "Client.clientIdEmpty" in str(excinfo.value)
    
    
def test_get_client_credit_history_wrong_client_id():
    with pytest.raises(Fault) as excinfo:
        CreditBureauService.get_client_credit_history(None, "clien12t123")
    assert "Client.ValidationError" in str(excinfo.value)
    

def test_get_client_credit_history_not_found():
    # Mock pour renvoyer None si client non trouvé
    with patch("services.CreditService.Database.get_credit_info", return_value=None):
        with pytest.raises(Fault) as excinfo:
            CreditBureauService.get_client_credit_history(None, "client-012")
        assert "Client.NotFound" in str(excinfo.value)

def test_get_client_credit_history_database_error():
    # Mock pour lever une exception
    with patch("services.CreditService.Database.get_credit_info", side_effect=Exception("DB down")):
        with pytest.raises(Fault) as excinfo:
            CreditBureauService.get_client_credit_history(None, "client-012")
        assert "Server.DatabaseError" in str(excinfo.value)