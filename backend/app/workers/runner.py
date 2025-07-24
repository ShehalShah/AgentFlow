from app.workers.tools import scrape_url, summarize_text, send_email
from datetime import datetime
import re

from app.celery_app import celery
# from app.tools import TOOL_MAP
from app.database import SessionLocal
from app.models.workflow_run import WorkflowRun
from app.models.workflow import Workflow
TOOL_MAP = {
    "scrape_url": scrape_url,
    "summarize_text": summarize_text,
    "send_email": send_email
}


def resolve_param(value: str, context: dict) -> str:
    """Replace {{step_id.output}} with actual value from previous step outputs."""
    matches = re.findall(r"\{\{(.+?)\}\}", value)
    for match in matches:
        step_ref = match.strip().split(".")
        if len(step_ref) != 2:
            continue
        step_id, field = step_ref
        replacement = context.get(step_id, {}).get(field, "")
        value = value.replace(f"{{{{{match}}}}}", replacement)
    return value


@celery.task(name="app.workers.runner.run_workflow")
def run_workflow(workflow: dict, run_id: int):
    db = SessionLocal()

    try:
        run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
        if not run:
            raise Exception(f"WorkflowRun with id {run_id} not found")

        run.status = "running"
        run.started_at = datetime.utcnow()
        db.commit()

        context = {}
        logs = {}

        for step in workflow["steps"]:
            step_id = step["id"]
            tool_name = step["tool"]
            raw_params = step.get("params", {})
            resolved_params = {}

            for key, val in raw_params.items():
                if isinstance(val, str):
                    resolved_params[key] = resolve_param(val, context)
                else:
                    resolved_params[key] = val

            try:
                tool = TOOL_MAP[tool_name]
                result = tool(resolved_params)
                context[step_id] = {"output": result}
                logs[step_id] = {"status": "success", "output": result}
            except Exception as e:
                logs[step_id] = {"status": "failed", "error": str(e)}
                run.status = "failed"
                run.ended_at = datetime.utcnow()
                run.logs = logs
                db.commit()
                raise e

        run.status = "success"
        run.ended_at = datetime.utcnow()
        run.logs = logs
        db.commit()

    finally:
        db.close()

    return context