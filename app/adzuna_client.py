from typing import Optional

import httpx

from .config import settings
from .schemas import Job, SearchResponse


class AdzunaClient:
    """

    Thin wrapper around the Adzuna Job Search API.

    Designed so we can inject an httpx.AsyncClient in tests and mock responses.

        - Calls Adzuna with what, where, pagination.

        - Normalizes into Job + SearchResponse.

        - Lets you inject a mocked httpx.AsyncClient in tests.

    """

    def __init__(self, http_client: Optional[httpx.AsyncClient] = None) -> None:
        self._client = http_client

    def _build_url(self, page: int) -> str:
        # Example: https://api.adzuna.com/v1/api/jobs/us/search/1
        return (
            f"{settings.adzuna_base_url}/jobs/"
            f"{settings.adzuna_country}/search/{page}"
        )

    async def search_jobs(
        self,
        *,
        query: str,
        location: Optional[str],
        page: int = 1,
        per_page: int = 20,
    ) -> SearchResponse:
        """
        Call Adzuna and return a normalized SearchResponse.
        """
        close_client = False
        if self._client is None:
            self._client = httpx.AsyncClient()
            close_client = True

        url = self._build_url(page)

        params: dict[str, object] = {
            "app_id": settings.adzuna_app_id,
            "app_key": settings.adzuna_app_key,
            "what": query,
            "results_per_page": per_page,
            "content-type": "application/json",
        }
        if location:
            params["where"] = location

        try:
            response = await self._client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
        finally:
            if close_client and self._client is not None:
                await self._client.aclose()

        payload = response.json()

        raw_results = payload.get("results", [])
        total = payload.get("count", len(raw_results))

        jobs: list[Job] = []
        for item in raw_results:
            jobs.append(
                Job(
                    id=str(item.get("id")),
                    title=item.get("title"),
                    company=(item.get("company") or {}).get("display_name"),
                    location=(item.get("location") or {}).get("display_name"),
                    category=(item.get("category") or {}).get("label"),
                    created=item.get("created"),
                    description=item.get("description"),
                    redirect_url=item.get("redirect_url"),
                    salary_min=item.get("salary_min"),
                    salary_max=item.get("salary_max"),
                    salary_currency=item.get("salary_currency"),
                )
            )

        return SearchResponse(
            total=total,
            page=page,
            per_page=per_page,
            results=jobs,
        )
