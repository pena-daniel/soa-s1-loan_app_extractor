import pytest
from unittest.mock import patch, MagicMock
from spyne import Fault
from services.ClientInfos import ClientIdentityService
from helpers.types import ClientIdentity

# Exemple de client "mocké"
mock_client_data = {
    "client_id": "client-123",
    "adresse": "12 rue de Paris, 75000 Paris"
}

def test_get_client_identity_success():
    # On mock Database.get_client_infos_by_name pour retourner un client valide
    with patch("services.ClientInfos.Database.get_client_infos_by_name", return_value=mock_client_data):
        result = ClientIdentityService.get_client_identity(None, "John Doe", "john@example.com")
        assert isinstance(result, ClientIdentity)
        assert result.clientId == "client-123"
        assert result.address == "12 rue de Paris, 75000 Paris"

def test_get_client_identity_empty_name():
    with pytest.raises(Fault) as excinfo:
        ClientIdentityService.get_client_identity(None, "", "john@example.com")
    assert "Client.clientNameEmpty" in str(excinfo.value)

def test_get_client_identity_not_found():
    # Mock pour renvoyer None si client non trouvé
    with patch("services.ClientInfos.Database.get_client_infos_by_name", return_value=None):
        with pytest.raises(Fault) as excinfo:
            ClientIdentityService.get_client_identity(None, "Unknown", "unknown@example.com")
        assert "Client.NotFound" in str(excinfo.value)

def test_get_client_identity_database_error():
    # Mock pour lever une exception
    with patch("services.ClientInfos.Database.get_client_infos_by_name", side_effect=Exception("DB down")):
        with pytest.raises(Fault) as excinfo:
            ClientIdentityService.get_client_identity(None, "John Doe", "john@example.com")
        assert "Server.DatabaseError" in str(excinfo.value)
