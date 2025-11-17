# src/adzuna_client/sheets_integration.py
import os
from typing import List, Dict, Iterable


def _open_sheet():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    service_json = os.getenv("GSPREAD_SERVICE_ACCOUNT_JSON")
    sheet_name = os.getenv("GSPREAD_SHEET_NAME", "Adzuna Jobs")
    if not service_json:
        raise RuntimeError(
            "GSPREAD_SERVICE_ACCOUNT_JSON not set. Add it to .env or disable --sheet."
        )

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(service_json, scope)
    client = gspread.authorize(creds)

    try:
        return client.open(sheet_name)
    except Exception:
        return client.create(sheet_name)


def _ensure_worksheet(sh, title: str):
    try:
        ws = sh.worksheet(title)
        ws.clear()
        return ws
    except Exception:
        return sh.add_worksheet(title=title, rows="2000", cols="30")


def _truncate(text: str, max_len: int = 300) -> str:
    if not text:
        return ""
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def _match_keywords(row: Dict, keywords: Iterable[str]) -> str:
    if not keywords:
        return ""
    blob = " ".join(
        [str(row.get("title", "")), str(row.get("description", ""))]
    ).lower()
    hits = sorted({kw for kw in keywords if kw and kw.lower() in blob})
    return ", ".join(hits)


RAW_HEADERS = [
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


def publish_to_google_sheets(
    rows: List[Dict],
    worksheet_title: str | None = None,
    keywords: Iterable[str] = (),
    columns: Iterable[str] | None = None,
) -> None:
    """
    Backward-compatible publisher:
      - If worksheet_title is None and columns is None:
          writes RAW_HEADERS to tab 'jobs' (old behavior)
      - Else:
          writes shaped columns to the specified tab
    """
    sh = _open_sheet()

    # Old behavior: default to 'jobs' and raw columns
    if worksheet_title is None and columns is None:
        ws = _ensure_worksheet(sh, "jobs")
        values = [RAW_HEADERS]
        for r in rows:
            values.append([r.get(h, "") for h in RAW_HEADERS])
        if len(values) == 1:
            values.append([""] * len(RAW_HEADERS))
        ws.update("A1", values)
        return

    # New behavior: shaped columns to a named tab
    ws = _ensure_worksheet(sh, worksheet_title or "jobs")
    shaped_cols = list(columns or RAW_HEADERS)
    values = [shaped_cols]

    for r in rows:
        row_out = []
        for col in shaped_cols:
            if col == "Title":
                row_out.append(r.get("title", ""))
            elif col == "Company":
                row_out.append(r.get("company", ""))
            elif col == "Location":
                row_out.append(r.get("location", ""))
            elif col == "URL":
                row_out.append(r.get("redirect_url", ""))
            elif col == "Matched Keywords":
                row_out.append(_match_keywords(r, keywords))
            elif col == "Description Snippet":
                row_out.append(_truncate(r.get("description", ""), 350))
            elif col == "Created":
                row_out.append(r.get("created", ""))
            elif col == "Category":
                row_out.append(r.get("category", ""))
            else:
                # fall back to raw field by key name if provided
                row_out.append(r.get(col, ""))
        values.append(row_out)

    if len(values) == 1:
        values.append([""] * len(shaped_cols))
    ws.update("A1", values)
