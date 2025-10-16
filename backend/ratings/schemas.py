from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from backend.movies.schemas import Movie

class RatingCreate(BaseModel):
    rating: float = Field(..., ge=0.0, le=10.0, description="Rating from 0.0 to 10.0")

class UserRatingResponse(BaseModel):
    movie: Movie
    user_rating: float

class UserRatingsResponse(BaseModel):
    ratings: List[UserRatingResponse]

class AverageRatingResponse(BaseModel):
    movie_id: str
    average_rating: Optional[float]
    total_ratings: int

class MovieRatingsResponse(BaseModel):
    movie_id: str
    ratings: Dict[str, float]  # user_id -> rating