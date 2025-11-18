from fastapi import FastAPI, Depends, Query

from app.adzuna_client import AdzunaClient

from .config import settings  # import the Settings instance
from .schemas import SearchResponse

app = FastAPI(
    title="Adzuna Job Search API",
    description="Backend service that wraps the Adzuna Job Search API",
    version="0.1.0",
)


def get_adzuna_client() -> AdzunaClient:
    return AdzunaClient()


@app.get("/")
def read_root():
    return {"message": "Adzuna Job Search API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "adzuna_job_search",
        "adzuna_configured": bool(settings.adzuna_app_id and settings.adzuna_app_key),
    }


@app.get("/search", response_model=SearchResponse)
async def search_jobs(
    q: str = Query(..., description="Free-text job query (Adzuna 'what')"),
    location: str | None = Query(
        None,
        description="Location filter (Adzuna 'where', e.g. 'Austin, TX')",
    ),
    page: int = Query(
        1,
        ge=1,
        description="Results page, 1-indexed per Adzuna API",
    ),
    per_page: int = Query(
        20,
        ge=1,
        le=50,
        description="Results per page (max 50 for Adzuna free tier)",
    ),
    client: AdzunaClient = Depends(get_adzuna_client),
) -> SearchResponse:
    """
    Proxy search to Adzuna and return normalized jobs.
    """
    return await client.search_jobs(
        query=q,
        location=location,
        page=page,
        per_page=per_page,
    )
