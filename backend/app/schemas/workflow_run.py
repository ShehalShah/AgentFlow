from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class WorkflowRunSchema(BaseModel):
    id: int
    workflow_id: int
    task_id: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime]
    logs: Optional[Dict[str, Any]]

    class Config:
        orm_mode = True
