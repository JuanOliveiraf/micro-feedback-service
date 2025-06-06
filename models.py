from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class FeedbackSaida(BaseModel):
    id: int
    mentor_name: str
    mentoring_name: str
    scheduled_date: datetime
    mentoring_rating: Optional[int]

class FeedbackResponse(BaseModel):
    mentoring_id: int
    rating: int