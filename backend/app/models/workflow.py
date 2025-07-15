from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_by = Column(String)  # user ID or email
    trigger = Column(String)     # cron string or natural lang
    steps = Column(JSON)  
    runs = relationship("WorkflowRun", back_populates="workflow")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by,
            "trigger": self.trigger,
            "steps": self.steps
        }

