from .scrape_url import scrape_url
from .send_email import send_email

TOOL_MAP = {
    "scrape_url": scrape_url,
    "send_email": send_email,
    # Add other tools as needed
}

TOOL_REGISTRY = {
    "scrape_url": {
        "name": "Scrape URL",
        "inputs": ["url"],
        "description": "Fetches text from a web page.",
        "function": "scrape_url"
    },
    "summarize_text": {
        "name": "Summarize Text",
        "inputs": ["text"],
        "description": "Summarizes the input text using an LLM.",
        "function": "summarizer.summarize"
    },
    "send_email": {
        "name": "Send Email",
        "inputs": ["to", "subject", "body"],
        "description": "Sends an email using SMTP.",
        "function": "send_email"
    }
}
