from celery import Celery

celery_app = Celery(
    "agentflow",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "app.workers.runner.run_workflow": {"queue": "workflows"},
}

# Import models to ensure they are registered with SQLAlchemy
from app.models import Workflow, WorkflowRun

# Import tasks to ensure they are registered with Celery
import app.workers.runner
