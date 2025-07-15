from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.workflow_run import WorkflowRun
from ..schemas.workflow_run import WorkflowRunSchema
from typing import List

router = APIRouter()

@router.get("/runs/", response_model=List[WorkflowRunSchema])
def list_runs(db: Session = Depends(get_db)):
    return db.query(WorkflowRun).all()

@router.get("/runs/{run_id}", response_model=WorkflowRunSchema)
def get_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
