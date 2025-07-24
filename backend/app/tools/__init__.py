from .scrape_url import scrape_url
from .send_email import send_email

TOOL_MAP = {
    "scrape_url": scrape_url,
    "send_email": send_email,
    # You can add more tools here: summarize_text, query_pdf, generate_image, etc.
}