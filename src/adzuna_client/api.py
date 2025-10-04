import os, time, requests
from typing import Dict, Generator
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load .env explicitly (works in heredoc, VS Code, etc.)
load_dotenv(dotenv_path=".env")

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs"

class AdzunaError(Exception): ...

def _check_creds():
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise AdzunaError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env")

def fetch_jobs(
    country: str = "us",
    what: str = "",
    where: str = "",
    days: int = 7,
    results_per_page: int = 50,
    max_pages: int = 1,
    sleep_secs: float = 0.4,
) -> Generator[Dict, None, None]:
    _check_creds()
    session = requests.Session()
    for page in range(1, max_pages + 1):
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": what or "",
            "where": where or "",
            "results_per_page": results_per_page,
            "content-type": "application/json",
            "max_days_old": days,
        }
        url = f"{BASE_URL}/{country}/search/{page}?{urlencode(params)}"
        print(f"[adzuna] GET {url}")  # DEBUG
        resp = session.get(url, timeout=30)
        print(f"[adzuna] HTTP {resp.status_code}")  # DEBUG

        if resp.status_code in (401, 403):
            raise AdzunaError(f"Auth error {resp.status_code}. Check APP_ID/KEY.")
        if resp.status_code == 404:
            raise AdzunaError("404 endpoint/country")
        if resp.status_code >= 400:
            raise AdzunaError(f"HTTP {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        results = data.get("results", []) or []
        print(f"[adzuna] page {page} results: {len(results)}")  # DEBUG
        if not results:
            return
        for r in results:
            yield {
                "id": r.get("id"),
                "title": r.get("title"),
                "company": (r.get("company") or {}).get("display_name"),
                "location": (r.get("location") or {}).get("display_name"),
                "created": r.get("created"),
                "redirect_url": r.get("redirect_url"),
                "description": r.get("description"),
                "salary_min": r.get("salary_min"),
                "salary_max": r.get("salary_max"),
                "contract_time": r.get("contract_time"),
                "category": (r.get("category") or {}).get("label"),
                "via": r.get("adref"),
            }
        time.sleep(sleep_secs)
