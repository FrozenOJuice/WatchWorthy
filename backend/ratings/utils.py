import json
import os
from typing import Dict, List, Optional
from pathlib import Path

RATINGS_FILE = Path("backend/data/ratings.json")

def load_ratings() -> Dict[str, Dict[str, float]]:
    """Load all user ratings: {user_id: {movie_id: rating}}"""
    if not RATINGS_FILE.exists():
        return {}
    
    with open(RATINGS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_ratings(ratings: Dict[str, Dict[str, float]]) -> None:
    RATINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RATINGS_FILE, "w") as f:
        json.dump(ratings, f, indent=4)

def get_user_ratings(user_id: str) -> Dict[str, float]:
    """Get all ratings for a specific user"""
    ratings = load_ratings()
    return ratings.get(user_id, {})

def get_movie_ratings(movie_id: str) -> Dict[str, float]:
    """Get all ratings for a specific movie"""
    all_ratings = load_ratings()
    movie_ratings = {}
    
    for user_id, user_ratings in all_ratings.items():
        if movie_id in user_ratings:
            movie_ratings[user_id] = user_ratings[movie_id]
    
    return movie_ratings

def get_average_rating(movie_id: str) -> Optional[float]:
    """Calculate average rating for a movie"""
    movie_ratings = get_movie_ratings(movie_id)
    if not movie_ratings:
        return None
    
    return sum(movie_ratings.values()) / len(movie_ratings)

def set_user_rating(user_id: str, movie_id: str, rating: float) -> None:
    """Set or update a user's rating for a movie"""
    ratings = load_ratings()
    
    if user_id not in ratings:
        ratings[user_id] = {}
    
    ratings[user_id][movie_id] = rating
    save_ratings(ratings)

def delete_user_rating(user_id: str, movie_id: str) -> bool:
    """Remove a user's rating for a movie"""
    ratings = load_ratings()
    
    if user_id in ratings and movie_id in ratings[user_id]:
        del ratings[user_id][movie_id]
        # Remove user entry if no ratings left
        if not ratings[user_id]:
            del ratings[user_id]
        save_ratings(ratings)
        return True
    
    return False