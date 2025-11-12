import pytest
import json
from spyne import Fault
from services.ServiceExtractor import ContentBlockExtractor, ContentLineExtractor, RequestInfoReader, InfoExtractor, TypeOfExtraction

# Exemple de texte structuré (ligne clé:valeur)
line_content = """client_name: John Doe
email: john@example.com
loan_amount: 5000
loan_times: 5
adresse: 12 rue de Paris, 75000 Paris
description: Appartement lumineux"""

# Exemple de texte bloc (non structuré)
block_content = """Je m'appelle John Doe, client-123
email: john@example.com
Je réside actuellement au 12 rue de Paris, 75000 Paris.
Je souhaite un prêt de 5 000 euros pour une durée de 5 ans.
Appartement lumineux située dans le centre de Paris.
Cordialement, John Doe
Tel: +33 6 12 34 56 78"""

def test_content_line_extractor():
    result = ContentLineExtractor.extract_info(line_content)
    assert result["client_name"] == "John Doe"
    assert result["email"] == "john@example.com"
    assert int(result["loan_amount"]) == 5000
    assert int(result["loan_times"]) == 5
    assert "Appartement lumineux" in result["description"]

def test_content_block_extractor():
    result = ContentBlockExtractor.extract_info(block_content)
    assert result["client_name"] == "John Doe"
    assert result["client_id"] == "client-123"
    assert result["email"] == "john@example.com"
    assert result["adresse"] == "centre de Paris" or "12 rue de Paris" or "le centre de paris" in result["adresse"]
    assert result["loan_amount"] == 5000
    assert result["loan_times"] == 5
    assert "Appartement lumineux" in result["description"]
    assert result["phone_numer"] == "+33 6 12 34 56 78"

def test_request_info_reader_line():
    result = RequestInfoReader.extract_info(TypeOfExtraction.line, line_content)
    assert result["client_name"] == "John Doe"

def test_request_info_reader_block():
    result = RequestInfoReader.extract_info(TypeOfExtraction.block, block_content)
    assert result["client_name"] == "John Doe"

def test_info_extractor_service(monkeypatch):
    # Mock RequestInfoReader.extract_info pour contrôler le retour
    monkeypatch.setattr(
        "services.ServiceExtractor.RequestInfoReader.extract_info",
        lambda type, content: {"mocked": True}
    )
    result = InfoExtractor.extract_info(None, "any content")
    parsed = json.loads(result)
    assert parsed["mocked"] is True

def test_info_extractor_empty_content():
    with pytest.raises(Fault) as excinfo:
        InfoExtractor.extract_info(None, "")
    assert "Client.ContentEmpty" in str(excinfo.value)
