from app.schemas import Decision, ActionItem, RiskFlag
def test_schemas():
    assert Decision(decision="Launch", speaker="Alice").speaker == "Alice"
    assert ActionItem(action="Send report").deadline is None
    assert RiskFlag(risk="Delay", severity="high").severity == "high"
