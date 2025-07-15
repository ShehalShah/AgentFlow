from pydantic import BaseModel
from typing import Dict, List, Union, Optional

class Step(BaseModel):
    id: str
    tool: str
    params: Dict[str, Union[str, float, int, bool]]

class WorkflowCreate(BaseModel):
    name: str
    created_by: str
    trigger: Optional[str] = None
    steps: List[Step]

class WorkflowSchema(WorkflowCreate):
    id: int
