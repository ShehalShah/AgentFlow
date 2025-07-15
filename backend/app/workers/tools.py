import time

def scrape_url(params):
    url = params["url"]
    time.sleep(1)  # Simulate work
    return f"Scraped content from {url}"

def summarize_text(params):
    text = params["text"]
    return f"Summary of: {text}"

def send_email(params):
    # just simulate
    to = params["to"]
    subject = params["subject"]
    body = params["body"]
    print(f"Email sent to {to}: {subject} - {body}")
    return "Email sent"
