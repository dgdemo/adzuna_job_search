from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, Field


class Job(BaseModel):
    id: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    created: datetime
    description: Optional[str] = None
    url: HttpUrl = Field(alias="redirect_url")
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: Optional[str] = None

    class Config:
        populate_by_name = True


class SearchResponse(BaseModel):
    total: int
    page: int
    per_page: int
    results: List[Job]
