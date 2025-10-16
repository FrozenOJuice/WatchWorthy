from pydantic import BaseModel, Field
from typing import List, Optional

class MovieMetadata(BaseModel):
    title: str
    movieIMDbRating: float
    totalRatingCount: int
    totalUserReviews: str
    totalCriticReviews: str
    metaScore: str
    movieGenres: List[str]
    directors: List[str]
    datePublished: str
    creators: List[str]
    mainStars: List[str]
    description: str
    duration: int


class Movie(BaseModel):
    id: str
    metadata: MovieMetadata


class MovieListResponse(BaseModel):
    movies: List[Movie]


# --- Reviews ---
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
    rating: Optional[int] = Field(None, ge=0, le=10)
