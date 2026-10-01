from app.ingestion import normalize_text
def test_normalize_text():
    assert normalize_text(" A   B\n\n\n C ") == "A B\n\n C"
