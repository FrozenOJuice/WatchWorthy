from pydantic import BaseModel, Field
from typing import List, Optional

class Review(BaseModel):
    date: str
    user: str
    usefulness_vote: Optional[int]
    total_votes: Optional[int]
    rating: Optional[float]
    title: str
    review: str

class ReviewListResponse(BaseModel):
    reviews: List[Review]

class ReviewCreate(BaseModel):
    review_title: str
    review_text: str
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)