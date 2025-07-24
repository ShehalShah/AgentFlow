import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(params):
    to = params.get("to")
    subject = params.get("subject", "")
    body = params.get("body", "")
    from_email = os.environ.get("SENDGRID_FROM_EMAIL")
    api_key = os.environ.get("SENDGRID_API_KEY")

    if not (to and body and from_email and api_key):
        return "ERROR: Missing required email parameters or SendGrid credentials."

    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            return "Email sent successfully"
        else:
            return f"ERROR: SendGrid returned status {response.status_code}: {response.body}"
    except Exception as e:
        return f"ERROR: {e}"