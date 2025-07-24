import requests
from bs4 import BeautifulSoup

def scrape_url(params: dict) -> str:
    url = params.get("url")
    if not url:
        raise ValueError("Missing 'url' parameter")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text.strip()[:3000]  # Limit to 3000 chars for now