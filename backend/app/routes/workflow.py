from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.workflow import WorkflowSchema, WorkflowCreate
from ..models.workflow import Workflow
from ..database import get_db  
from app.workers.runner import run_workflow

router = APIRouter()

from ..schemas.workflow import WorkflowSchema, WorkflowCreate

@router.post("/workflows/", response_model=WorkflowSchema)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    # Convert Step objects to plain dictionaries
    step_dicts = [step.dict() for step in workflow.steps]

    db_workflow = Workflow(
        name=workflow.name,
        created_by=workflow.created_by,
        trigger=workflow.trigger,
        steps=step_dicts  # now it's plain JSON serializable
    )

    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@router.get("/workflows/{workflow_id}", response_model=WorkflowSchema)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    wf = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return wf

@router.get("/workflows/", response_model=list[WorkflowSchema])
def list_workflows(db: Session = Depends(get_db)):
    return db.query(Workflow).all()

from ..models.workflow_run import WorkflowRun
from datetime import datetime

@router.post("/workflows/{workflow_id}/run")
def run_saved_workflow(workflow_id: int, db: Session = Depends(get_db)):
    wf = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Create a new run entry
    run = WorkflowRun(
        workflow_id=wf.id,
        status="pending",
        started_at=datetime.utcnow()
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    # Trigger the Celery task and update task_id
    task = run_workflow.delay(wf.as_dict(), run.id)

    run.task_id = task.id
    db.commit()

    return {"run_id": run.id, "task_id": task.id}


