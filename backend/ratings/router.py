from fastapi import APIRouter, HTTPException, Depends
from backend.ratings import schemas
from backend.ratings import utils as ratings_utils
from backend.movies import utils as movies_utils
from backend.authentication.security import get_current_user
from backend.authentication import utils as auth_utils

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/{movie_id}")
@movies_utils.movie_exists
def rate_movie(
    movie_id: str,
    rating_data: schemas.RatingCreate,
    current_user=Depends(get_current_user)
):
    """Rate a movie (separate from review)"""
    ratings_utils.set_user_rating(current_user.user_id, movie_id, rating_data.rating)
    
    return {
        "message": "Movie rated successfully", 
        "movie_id": movie_id, 
        "rating": rating_data.rating
    }

@router.delete("/{movie_id}")
@movies_utils.movie_exists
def remove_rating(
    movie_id: str,
    movie: dict,
    current_user=Depends(get_current_user)
):
    """Remove user's rating for a movie"""
    success = ratings_utils.delete_user_rating(current_user.user_id, movie_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    return {"message": "Rating removed successfully", "movie_id": movie_id}

@router.get("/user", response_model=schemas.UserRatingsResponse)
def get_user_ratings(current_user=Depends(get_current_user)):
    """Get all movies rated by user with details"""
    user_ratings = ratings_utils.get_user_ratings(current_user.user_id)
    all_movies = movies_utils.load_movies()
    
    rated_movies = []
    for movie_id, rating in user_ratings.items():
        movie = next((m for m in all_movies if m["id"] == movie_id), None)
        if movie:
            rated_movies.append({
                "movie": movie,
                "user_rating": rating
            })
    
    return {"ratings": rated_movies}

@router.get("/{movie_id}/average", response_model=schemas.AverageRatingResponse)
@movies_utils.movie_exists
def get_movie_average_rating(movie_id: str):
    """Get average rating for a movie"""
    avg_rating = ratings_utils.get_average_rating(movie_id)
    movie_ratings = ratings_utils.get_movie_ratings(movie_id)
    
    return {
        "movie_id": movie_id,
        "average_rating": avg_rating,
        "total_ratings": len(movie_ratings)
    }

@router.get("/{movie_id}/user")
@movies_utils.movie_exists
def get_user_rating_for_movie(
    movie_id: str,
    movie: dict,
    current_user=Depends(get_current_user)
):
    """Get current user's rating for a specific movie"""
    user_ratings = ratings_utils.get_user_ratings(current_user.user_id)
    user_rating = user_ratings.get(movie_id)
    
    return {
        "movie_id": movie_id,
        "user_rating": user_rating
    }