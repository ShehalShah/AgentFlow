from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import workflow
from app.routes import workflow_run

# Import models to ensure they are registered with SQLAlchemy
from .models import Workflow, WorkflowRun

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow.router)
app.include_router(workflow_run.router)

# @app.get("/")
# def root():
#     return {"msg": "AgentFlow backend running!"}

# celery -A app.celery_app.celery worker --loglevel=info -Q workflows
# uvicorn app.main:app --reload
