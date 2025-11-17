from typing import Any


from app.config import settings


class AdzunaClient:
    def __init__(self) -> None:
        self.base_url = settings.adzuna_base_url
        self.app_id = settings.adzuna_app_id
        self.app_key = settings.adzuna_app_key

    async def search_jobs(
        self,
        coountry: str,
        query: str,
        page: int = 1,
        results_per_page: int = 20,
    ) -> dict[str, Any]:
        # actual implementation will come in next steps.
        raise NotImplementedError("AdzunaClient.search_jobs is not yet implemented.")
