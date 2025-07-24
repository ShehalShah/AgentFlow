from backend.app.database import Base, engine
from backend.app.models import Workflow, WorkflowRun

Base.metadata.create_all(bind=engine)
