from typing import Literal
from pydantic import BaseModel, Field

class Decision(BaseModel):
    decision: str
    speaker: str
    evidence: str = ""

class ActionItem(BaseModel):
    action: str
    owner: str | None = None
    deadline: str | None = None
    evidence: str = ""

class RiskFlag(BaseModel):
    risk: str
    severity: Literal["low", "medium", "high", "critical"]
    owner: str | None = None
    evidence: str = ""

class TopicCluster(BaseModel):
    topic: str
    description: str
    speakers: list[str] = Field(default_factory=list)

class StructuredExtraction(BaseModel):
    decisions: list[Decision] = Field(default_factory=list)
    actions: list[ActionItem] = Field(default_factory=list)
    risks: list[RiskFlag] = Field(default_factory=list)
    topics: list[TopicCluster] = Field(default_factory=list)
