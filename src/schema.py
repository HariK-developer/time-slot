from pydantic import BaseModel, Field


class DateAvailability(BaseModel):
    user_id: list
    date_range: list[str] = Field(..., min_length=2, max_length=2)
    time_zone: str

    class Config:
        extra = "forbid"
