import requests
import os
from app.tools.registry import TOOL_REGISTRY
from dotenv import load_dotenv
load_dotenv()

import os
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable not set!")
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

tool_descriptions = "\n".join([
    f"{tool_id} ({tool_info['name']}): {tool_info['description']}" for tool_id, tool_info in TOOL_REGISTRY.items()
])


SYSTEM_PROMPT = f"""
You are a workflow planner AI.
Given a user's natural language intent, decide the sequence of tasks (tools) to achieve it.
Given a user instruction, choose and order tools to form a workflow.
    Each tool has a name and description. Choose from only these tools:

{{tool_descriptions}}

Return steps in the format:
[
  {{"id": "step_1", "tool": "scrape_url", "params": {{"url": "..."}}}},
  {{"id": "step_2", "tool": "summarize_text", "params": {{"text": "{{step_1.output}}"}}}},
  ...
]
""".replace("{tool_descriptions}", tool_descriptions)

def generate_steps_from_intent(intent: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Optional headers for OpenRouter ranking (customize as needed)
        # "HTTP-Referer": "http://localhost:8000",  # or your deployed site
        # "X-Title": "AgentFlow Backend"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Intent: {intent}"},
        ],
        "temperature": 0.7
    }
    import json
    response = requests.post(OPENROUTER_URL, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except Exception as e:
        print("Failed to parse steps:", e)
        return []