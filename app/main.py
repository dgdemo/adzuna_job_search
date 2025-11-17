from fastapi import FastAPI

from .config import settings  # 👈 import the Settings instance

app = FastAPI(
    title="Adzuna Job Search API",
    description="Backend service that wraps the Adzuna Job Search API",
    version="0.1.0",
)


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


# testing comment
