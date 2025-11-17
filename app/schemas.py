from pydantic import BaseModel


class JobListing(BaseModel):
    id: str
    title: str
    company: str | None = None
    location: str | None = None
    created: str | None = None
    redirect_url: str | None = None
