import json
import csv
import os
from pathlib import Path
from datetime import datetime
from functools import wraps
from fastapi import HTTPException

DATA_PATH = Path("backend/data/movieData")

def load_movies():
    """Load all movies and their metadata from individual folders."""
    movies = []
    for movie_dir in DATA_PATH.iterdir():
        if movie_dir.is_dir():
            metadata_file = movie_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                movies.append({
                    "id": movie_dir.name,
                    "metadata": metadata
                })
    return movies

def get_movie_by_id(movie_id: str):
    """Fetch a single movie's metadata by folder name."""
    movie_dir = DATA_PATH / movie_id
    metadata_file = movie_dir / "metadata.json"

    if metadata_file.exists():
        with open(metadata_file, "r", encoding="utf-8") as f:
            return {"id": movie_id, "metadata": json.load(f)}
    return None

# --- Decorators ---
def movie_exists(func):
    """Decorator to ensure a valid movie ID (folder) before calling the route."""
    @wraps(func)
    def wrapper(movie_id: str, *args, **kwargs):
        movie = get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return func(movie_id, *args, movie=movie, **kwargs)
    return wrapper