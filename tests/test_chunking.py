from app.chunking import build_chunks, normalize_speaker_turns
def test_speaker_turns():
    turns = normalize_speaker_turns("Alice: Hello\nBob: Hi there")
    assert len(turns) == 2
def test_chunks():
    chunks = build_chunks("Alice: Hello\nBob: Hi\nCarol: Bye", 30, 5)
    assert chunks[0].index == 1
