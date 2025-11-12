import pytest
from spyne import Fault
from services.ExplanantionService import ExplanationService
from helpers.types import ExplanationsType

def test_get_explanation_excellent_score():
    result = ExplanationService.get_explaination(None, 850, 5000, 2000, 1000, 0, False)
    assert isinstance(result, ExplanationsType)
    assert "excellent" in result.creditScoreExplanation
    assert "your income exceeds your expenses" in result.incomeVsExpensesExplanation
    assert "no late payments and no bankruptcy" in result.creditHistoryExplanation

def test_get_explanation_acceptable_score_with_late():
    result = ExplanationService.get_explaination(None, 700, 3000, 3500, 2000, 2, False)
    assert "acceptable" in result.creditScoreExplanation
    assert "your expenses exceed your income" in result.incomeVsExpensesExplanation
    assert "some late payments but no bankruptcy" in result.creditHistoryExplanation

def test_get_explanation_poor_score_with_bankruptcy():
    result = ExplanationService.get_explaination(None, 600, 2500, 2000, 3000, 1, True)
    assert "poor" in result.creditScoreExplanation
    assert "your income exceeds your expenses" in result.incomeVsExpensesExplanation
    assert "a history of bankruptcy" in result.creditHistoryExplanation

def test_get_explanation_negative_values():
    with pytest.raises(Fault) as excinfo:
        ExplanationService.get_explaination(None, 700, -3000, 2000, 1000, 0, False)
    assert "Numeric inputs must be >= 0" in str(excinfo.value)

def test_get_explanation_invalid_numeric_inputs():
    with pytest.raises(Fault) as excinfo:
        ExplanationService.get_explaination(None, "abc", 2000, 1500, 1000, 0, False)
    assert "Invalid numeric inputs for decision" in str(excinfo.value)
