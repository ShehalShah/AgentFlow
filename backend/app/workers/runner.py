from app.celery_app import celery
from app.database import SessionLocal
from app.workers.tools import scrape_url, summarize_text, send_email
from app.models import WorkflowRun, Workflow
from datetime import datetime

TOOL_MAP = {
    "scrape_url": scrape_url,
    "summarize_text": summarize_text,
    "send_email": send_email
}

@celery.task(name="app.workers.runner.run_workflow")
def run_workflow(workflow, run_id):
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

        try:
            for step in workflow["steps"]:
                resolved_params = {}
                for key, value in step["params"].items():
                    if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                        ref = value.strip("{{}}").split(".")[0]
                        resolved_params[key] = context.get(ref, {}).get("output", "")
                    else:
                        resolved_params[key] = value

                tool = TOOL_MAP[step["tool"]]
                result = tool(resolved_params)
                context[step["id"]] = {"output": result}
                logs[step["id"]] = {"status": "success", "output": result}

            run.status = "success"
            run.ended_at = datetime.utcnow()
            run.logs = logs
        except Exception as e:
            run.status = "failed"
            run.ended_at = datetime.utcnow()
            logs["error"] = str(e)
            run.logs = logs
            raise e

        db.commit()
    finally:
        db.close()

    return context
