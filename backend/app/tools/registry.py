TOOL_REGISTRY = {
    "scrape_url": {
        "name": "Scrape URL",
        "inputs": ["url"],
        "description": "Fetches text from a web page.",
        "function": "scraper.scrape"
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
        "function": "emailer.send"
    }
}
