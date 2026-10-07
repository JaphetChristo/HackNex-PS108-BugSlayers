from typing import Optional, List
from pydantic import BaseModel


class AnalysisPlan(BaseModel):
    task: str
    required_columns: List[str]
    operations: List[str]


class AgentResponse(BaseModel):
    can_answer: bool
    reason: str
    analysis_plan: Optional[AnalysisPlan]
    python_code: Optional[str]
    result_type: Optional[str]