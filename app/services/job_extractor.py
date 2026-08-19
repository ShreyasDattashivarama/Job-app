from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup


def extract_from_url(url: str) -> str:
    """Best-effort public page extraction; callers must request pasted text on failure."""
    response = requests.get(url, timeout=15, headers={"User-Agent": "JobApplicationCopilot/0.1"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n", strip=True))
    if len(text) < 300:
        raise ValueError("The page did not contain a reliable job description.")
    return text

