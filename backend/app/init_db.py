from .database import Base, engine
from .models import Workflow, WorkflowRun

Base.metadata.create_all(bind=engine)
