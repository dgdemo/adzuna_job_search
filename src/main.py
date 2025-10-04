import csv, argparse
from typing import List, Dict
from dotenv import load_dotenv
from adzuna_client.api import fetch_jobs

# Ensure .env loads even when invoked from shells/heredocs
load_dotenv(dotenv_path=".env")

def write_csv(rows: List[Dict], out_path: str) -> None:
    headers = ["id","title","company","location","created","redirect_url",
               "description","salary_min","salary_max","contract_time","category","via"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        if rows:
            w.writerows(rows)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--what", default="")
    p.add_argument("--where", default="")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--per-page", type=int, default=5)
    p.add_argument("--max-pages", type=int, default=1)
    p.add_argument("--country", default="us")
    p.add_argument("--out", default="results.csv")
    p.add_argument("--sheet", action="store_true")
    p.add_argument("--sheet-tab", default=None)
    p.add_argument("--columns-basic", action="store_true")
    args = p.parse_args()

    print("[main] start", dict(what=args.what, days=args.days, per=args.per_page, pages=args.max_pages, sheet=args.sheet, tab=args.sheet_tab))
    rows = list(fetch_jobs(
        country=args.country,
        what=args.what,
        where=args.where,
        days=args.days,
        results_per_page=args.per_page,
        max_pages=args.max_pages,
    ))
    print(f"[main] fetched {len(rows)} rows")
    write_csv(rows, args.out)
    print(f"[main] wrote CSV -> {args.out}")

    if args.sheet:
        from adzuna_client.sheets_integration import publish_to_google_sheets
        if args.columns_basic:
            columns = ("Title","Company","Location","URL","Matched Keywords","Description Snippet")
            keywords = [tok.strip() for tok in args.what.split() if tok.strip()]
            publish_to_google_sheets(rows, worksheet_title=args.sheet_tab or "jobs",
                                     keywords=keywords, columns=columns)
        else:
            publish_to_google_sheets(rows)
        print(f"[main] published to Sheets tab '{args.sheet_tab or 'jobs'}'")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback; traceback.print_exc()
