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

class WatchLaterResponse(BaseModel):
    watch_later: List[Movie]