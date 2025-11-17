# scripts/run_all_tabs.py
import os
import time
import csv
import argparse
import sys
import json

# Ensure we can import from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from typing import List, Dict, Union
from dotenv import load_dotenv
from adzuna_client.api import fetch_jobs
from adzuna_client.sheets_integration import publish_to_google_sheets

load_dotenv(dotenv_path=".env")

BASIC_COLUMNS = (
    "Title",
    "Company",
    "Location",
    "URL",
    "Matched Keywords",
    "Description Snippet",
)


def write_csv(rows: List[Dict], out_path: str) -> None:
    headers = [
        "id",
        "title",
        "company",
        "location",
        "created",
        "redirect_url",
        "description",
        "salary_min",
        "salary_max",
        "contract_time",
        "category",
        "via",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        if rows:
            w.writerows(rows)


def load_cfg():
    cfg_path = os.path.join("config", "tabs.json")
    if not os.path.exists(cfg_path):
        return None
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_list(v: Union[str, List[str]]) -> List[str]:
    return v if isinstance(v, list) else [v]


def dedupe_rows(rows: List[Dict]) -> List[Dict]:
    seen = set()
    out = []
    for r in rows:
        key = (
            r.get("id")
            or r.get("redirect_url")
            or (r.get("title"), r.get("company"), r.get("location"))
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def run_tab(
    tab: str,
    queries: List[str],
    days: int,
    per_page: int,
    max_pages: int,
    country: str,
    sheet: bool,
    sleep: float,
):
    print(
        f"[run] tab={tab} queries={queries} days={days} per_page={per_page} pages={max_pages}"
    )
    all_rows: List[Dict] = []
    for q in queries:
        rows = list(
            fetch_jobs(
                country=country,
                what=q,
                where="",
                days=days,
                results_per_page=per_page,
                max_pages=max_pages,
            )
        )
        print(f"[run] tab={tab} subquery='{q}' fetched={len(rows)}")
        all_rows.extend(rows)
        time.sleep(sleep)
    all_rows = dedupe_rows(all_rows)
    print(f"[run] tab={tab} total_after_dedupe={len(all_rows)}")

    out_csv = f"{tab}.csv"
    write_csv(all_rows, out_csv)
    print(f"[run] tab={tab} wrote CSV -> {out_csv}")

    if sheet:
        # Build keyword list for the Matched Keywords column (tokens across all queries)
        tokens: List[str] = []
        for q in queries:
            tokens.extend([t for t in q.replace('"', "").split() if t.strip()])
        publish_to_google_sheets(
            all_rows, worksheet_title=tab, keywords=tokens, columns=BASIC_COLUMNS
        )
        print(f"[run] tab={tab} published to Google Sheets")


def main():
    ap = argparse.ArgumentParser(
        description="Refresh tabs and CSVs (reads config/tabs.json if present)."
    )
    ap.add_argument("--days", type=int, default=7, help="Max age of listings")
    ap.add_argument("--per-page", type=int, default=50, help="Results per page")
    ap.add_argument("--max-pages", type=int, default=2, help="Pages to fetch")
    ap.add_argument("--country", default="us", help="Adzuna country code")
    ap.add_argument(
        "--sleep", type=float, default=0.4, help="Seconds between subqueries/tabs"
    )
    ap.add_argument(
        "--no-sheet", action="store_true", help="Skip Google Sheets publishing"
    )
    ap.add_argument(
        "--only", help="Run a single tab name (must exist in config or defaults)"
    )
    args = ap.parse_args()

    # Default queries (now lists)
    tabs: Dict[str, Union[str, List[str]]] = {
        "terraform": ["terraform", "terraform aws", "terraform gcp", "terraform azure"],
        "appsec": [
            '"application security"',
            "appsec",
            '"application security engineer"',
            "devsecops application security",
            "sast dast code scanning",
            'threat modeling "secure sdlc"',
        ],
        "cloudsec": [
            '"cloud security"',
            '"cloud security engineer"',
            "iam aws security",
            "kubernetes security",
            "cnapp cspm cwpp",
        ],
    }
    defaults = dict(
        days=args.days,
        per_page=args.per_page,
        max_pages=args.max_pages,
        country=args.country,
        sleep=args.sleep,
    )

    cfg = load_cfg()
    if cfg:
        if "tabs" in cfg and isinstance(cfg["tabs"], dict):
            tabs = cfg["tabs"]
        if "defaults" in cfg and isinstance(cfg["defaults"], dict):
            defaults.update({k: v for k, v in cfg["defaults"].items() if k in defaults})

    if args.only:
        if args.only not in tabs:
            raise SystemExit(
                f"--only '{args.only}' not found in tabs: {', '.join(tabs.keys())}"
            )
        tabs = {args.only: tabs[args.only]}

    for tab, q in tabs.items():
        queries = ensure_list(q)
        run_tab(
            tab=tab,
            queries=queries,
            days=defaults["days"],
            per_page=defaults["per_page"],
            max_pages=defaults["max_pages"],
            country=defaults["country"],
            sheet=not args.no_sheet,
            sleep=defaults["sleep"],
        )


if __name__ == "__main__":
    main()
