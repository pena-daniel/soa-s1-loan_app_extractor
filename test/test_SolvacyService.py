import pytest
from spyne import Fault
from services.SolvacyService import SolvacyService
from helpers.types import SolvencyStatusType

def test_calculate_solvacy_solvent():
    result = SolvacyService.calculate_solvacy(None, "client-123", 5000, 2000, 750)
    assert result == SolvencyStatusType.SOLVENT

def test_calculate_solvacy_not_solvent_low_score():
    result = SolvacyService.calculate_solvacy(None, "client-123", 5000, 2000, 650)
    assert result == SolvencyStatusType.NOT_SOLVENT

def test_calculate_solvacy_not_solvent_expenses_higher():
    result = SolvacyService.calculate_solvacy(None, "client-123", 2000, 3000, 800)
    assert result == SolvencyStatusType.NOT_SOLVENT

def test_calculate_solvacy_empty_client_id():
    with pytest.raises(Fault) as excinfo:
        SolvacyService.calculate_solvacy(None, "", 5000, 2000, 750)
    assert "Client.clientIdEmpty" in str(excinfo.value)

def test_calculate_solvacy_invalid_client_id():
    with pytest.raises(Fault) as excinfo:
        SolvacyService.calculate_solvacy(None, "invalid-456", 5000, 2000, 750)
    assert "Client.ValidationError" in str(excinfo.value)
    assert "invalide" in str(excinfo.value)

def test_calculate_solvacy_negative_values():
    with pytest.raises(Fault) as excinfo:
        SolvacyService.calculate_solvacy(None, "client-123", -5000, 2000, 750)
    assert "Income and expenses must be >= 0" in str(excinfo.value)

def test_calculate_solvacy_invalid_numeric_inputs():
    with pytest.raises(Fault) as excinfo:
        SolvacyService.calculate_solvacy(None, "client-123", "abc", 2000, 750)
    assert "Invalid numeric inputs for decision" in str(excinfo.value)
