from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from backend.movies import schemas
from backend.movies import utils as movie_utils
from backend.authentication.security import get_current_user
from backend.authentication import utils as auth_utils

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=schemas.MovieListResponse)
def get_movies(
    genre: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    sort_by: Optional[str] = Query(None, enum=["rating", "date"]),
    order: Optional[str] = Query("asc", enum=["asc", "desc"])
):
    movies = movie_utils.load_movies()

    if genre:
        movies = [m for m in movies if genre in m["metadata"]["movieGenres"]]
    if min_rating is not None:
        movies = [m for m in movies if m["metadata"]["movieIMDbRating"] >= min_rating]
    if max_rating is not None:
        movies = [m for m in movies if m["metadata"]["movieIMDbRating"] <= max_rating]

    if sort_by == "rating":
        movies.sort(key=lambda m: m["metadata"]["movieIMDbRating"], reverse=(order == "desc"))
    elif sort_by == "date":
        movies.sort(key=lambda m: m["metadata"]["datePublished"], reverse=(order == "desc"))

    return {"movies": movies}

@router.get("/{movie_id}", response_model=schemas.Movie)
@movie_utils.movie_exists
def get_movie(movie_id: str, movie: dict):
    return movie

@router.post("/{movie_id}/watch-later")
@movie_utils.movie_exists
def add_to_watch_later(
    movie_id: str,
    movie: dict,
    current_user=Depends(get_current_user)
):
    """Add movie to user's watch later list"""
    users = auth_utils.load_users()
    user = next((u for u in users if u['user_id'] == current_user.user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "watch_later" not in user:
        user["watch_later"] = []
    
    if movie_id in user["watch_later"]:
        raise HTTPException(status_code=400, detail="Movie already in watch later list")
    
    user["watch_later"].append(movie_id)
    auth_utils.save_users(users)
    
    return {"message": "Movie added to watch later", "movie_id": movie_id}

@router.delete("/{movie_id}/watch-later")
@movie_utils.movie_exists
def remove_from_watch_later(
    movie_id: str,
    movie: dict,
    current_user=Depends(get_current_user)
):
    """Remove movie from user's watch later list"""
    users = auth_utils.load_users()
    user = next((u for u in users if u['user_id'] == current_user.user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "watch_later" not in user or movie_id not in user["watch_later"]:
        raise HTTPException(status_code=400, detail="Movie not in watch later list")
    
    user["watch_later"].remove(movie_id)
    auth_utils.save_users(users)
    
    return {"message": "Movie removed from watch later", "movie_id": movie_id}

@router.get("/user/watch-later", response_model=schemas.WatchLaterResponse)
def get_watch_later(current_user=Depends(get_current_user)):
    """Get user's watch later list with movie details"""
    users = auth_utils.load_users()
    user = next((u for u in users if u['user_id'] == current_user.user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    watch_later_movies = []
    all_movies = movie_utils.load_movies()
    
    for movie_id in user.get("watch_later", []):
        movie = next((m for m in all_movies if m["id"] == movie_id), None)
        if movie:
            watch_later_movies.append(movie)
    
    return {"watch_later": watch_later_movies}