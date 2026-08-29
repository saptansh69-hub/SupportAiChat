"""
Pulls live product & pricing info so the bot never answers from stale,
hardcoded text. Two modes:

1. WEBSITE_API_URL set -> hits your backend's JSON endpoints directly.
   This is the recommended path since you already run a Python backend.
2. Only WEBSITE_URL set -> scrapes the page's visible text as a fallback.

Either way, results are cached in memory for CONTEXT_REFRESH_SECONDS so
you're not hammering your own site on every single chat message.
"""

import time
import requests
from bs4 import BeautifulSoup

import config

_cache = {"text": "", "fetched_at": 0}


def _fetch_from_api() -> str:
    parts = []
    for endpoint in ("/products", "/pricing"):
        try:
            resp = requests.get(config.WEBSITE_API_URL.rstrip("/") + endpoint, timeout=10)
            resp.raise_for_status()
            parts.append(f"{endpoint}: {resp.json()}")
        except Exception as e:
            parts.append(f"{endpoint}: (unavailable - {e})")
    return "\n".join(parts)


def _fetch_from_website() -> str:
    resp = requests.get(config.WEBSITE_URL, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = " ".join(soup.get_text(separator=" ").split())
    return text[:6000]  # keep prompt context reasonable


def get_product_context() -> str:
    """Returns cached (or freshly fetched) product/pricing text for the LLM prompt."""
    now = time.time()
    if now - _cache["fetched_at"] < config.CONTEXT_REFRESH_SECONDS and _cache["text"]:
        return _cache["text"]

    try:
        if config.WEBSITE_API_URL:
            text = _fetch_from_api()
        elif config.WEBSITE_URL:
            text = _fetch_from_website()
        else:
            text = "(No WEBSITE_URL or WEBSITE_API_URL configured yet.)"
    except Exception as e:
        text = _cache["text"] or f"(Failed to fetch product info: {e})"

    _cache["text"] = text
    _cache["fetched_at"] = now
    return text
