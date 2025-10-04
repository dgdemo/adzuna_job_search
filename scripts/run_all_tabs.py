import os, time, csv, argparse, sys, json
# Ensure we can import from src/
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from typing import List, Dict
from dotenv import load_dotenv
from adzuna_client.api import fetch_jobs
from adzuna_client.sheets_integration import publish_to_google_sheets

load_dotenv(dotenv_path=".env")

BASIC_COLUMNS = ("Title","Company","Location","URL","Matched Keywords","Description Snippet")

def write_csv(rows: List[Dict], out_path: str) -> None:
    headers = ["id","title","company","location","created","redirect_url",
               "description","salary_min","salary_max","contract_time","category","via"]
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

def run_tab(tab: str, query: str, days: int, per_page: int, max_pages: int, country: str, sheet: bool, sleep: float):
    print(f"[run] tab={tab} query='{query}' days={days} per_page={per_page} pages={max_pages}")
    rows = list(fetch_jobs(
        country=country, what=query, where="", days=days,
        results_per_page=per_page, max_pages=max_pages
    ))
    print(f"[run] tab={tab} fetched={len(rows)}")
    out_csv = f"{tab}.csv"
    write_csv(rows, out_csv)
    print(f"[run] tab={tab} wrote CSV -> {out_csv}")

    if sheet:
        keywords = [k for k in query.split() if k.strip()]
        publish_to_google_sheets(rows, worksheet_title=tab, keywords=keywords, columns=BASIC_COLUMNS)
        print(f"[run] tab={tab} published to Google Sheets")
    time.sleep(sleep)

def main():
    ap = argparse.ArgumentParser(description="Refresh tabs and CSVs (reads config/tabs.json if present).")
    ap.add_argument("--days", type=int, default=7, help="Max age of listings")
    ap.add_argument("--per-page", type=int, default=50, help="Results per page")
    ap.add_argument("--max-pages", type=int, default=2, help="Pages to fetch")
    ap.add_argument("--country", default="us", help="Adzuna country code")
    ap.add_argument("--sleep", type=float, default=0.4, help="Seconds between tabs")
    ap.add_argument("--no-sheet", action="store_true", help="Skip Google Sheets publishing")
    ap.add_argument("--only", help="Run a single tab name (must exist in config or defaults)")
    args = ap.parse_args()

    cfg = load_cfg()
    tabs = {"terraform":"terraform","appsec":"application security appsec code scanning static analysis threat modeling","cloudsec":"cloud security aws gcp azure iam"}
    defaults = dict(days=args.days, per_page=args.per_page, max_pages=args.max_pages, country=args.country, sleep=args.sleep)

    if cfg:
        if "tabs" in cfg and isinstance(cfg["tabs"], dict):
            tabs = cfg["tabs"]
        if "defaults" in cfg and isinstance(cfg["defaults"], dict):
            defaults.update({k:v for k,v in cfg["defaults"].items() if k in defaults})

    if args.only:
        if args.only not in tabs:
            raise SystemExit(f"--only '{args.only}' not found in tabs: {', '.join(tabs.keys())}")
        tabs = {args.only: tabs[args.only]}

    for tab, query in tabs.items():
        run_tab(
            tab=tab,
            query=query,
            days=defaults["days"],
            per_page=defaults["per_page"],
            max_pages=defaults["max_pages"],
            country=defaults["country"],
            sheet=not args.no_sheet,
            sleep=defaults["sleep"],
        )

if __name__ == "__main__":
    main()
