import pytest
from unittest.mock import patch, MagicMock
from spyne import Fault
from services.FinancialDataService import FinancialService
from helpers.types import FinancialsInfoType

# Exemple de client "mocké"
mock_financial_data =     {
        "client_id": "client-001",
        "income": 4000,
        "expenses": 3000
    }

def test_get_financial_info_success():
    # On mock Database.get_client_infos_by_name pour retourner un client valide
    with patch("services.FinancialDataService.Database.get_financial_info", return_value=mock_financial_data):
        result = FinancialService.get_financial_info(None, "client-001")
        assert isinstance(result, FinancialsInfoType)
        assert result.monthlyIncome == 4000
        assert result.monthlyExpenses == 3000



def test_get_financial_info_empty_client_id():
    with pytest.raises(Fault) as excinfo:
        FinancialService.get_financial_info(None, "")
    assert "Client.clientIdEmpty" in str(excinfo.value)
    
    
def test_get_financial_info_wrong_client_id():
    with pytest.raises(Fault) as excinfo:
        FinancialService.get_financial_info(None, "clien12t123")
    assert "Client.ValidationError" in str(excinfo.value)
    

def test_get_financial_info_not_found():
    # Mock pour renvoyer None si client non trouvé
    with patch("services.FinancialDataService.Database.get_financial_info", return_value=None):
        with pytest.raises(Fault) as excinfo:
            FinancialService.get_financial_info(None, "client-012")
        assert "Client.NotFound" in str(excinfo.value)

def test_get_financial_info_database_error():
    # Mock pour lever une exception
    with patch("services.FinancialDataService.Database.get_financial_info", side_effect=Exception("DB down")):
        with pytest.raises(Fault) as excinfo:
            FinancialService.get_financial_info(None, "client-012")
        assert "Server.DatabaseError" in str(excinfo.value)