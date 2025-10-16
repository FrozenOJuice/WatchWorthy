import json
import csv
import os
from pathlib import Path
from datetime import datetime
from functools import wraps
from fastapi import HTTPException

DATA_PATH = Path("backend/data/movies")


def load_movies():
    """Load all movies and their metadata."""
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
    """Fetch a single movie's metadata."""
    movie_dir = DATA_PATH / movie_id
    metadata_file = movie_dir / "metadata.json"

    if metadata_file.exists():
        with open(metadata_file, "r", encoding="utf-8") as f:
            return {"id": movie_id, "metadata": json.load(f)}
    return None


def load_reviews(movie_id: str):
    """Load reviews for a movie."""
    movie_dir = DATA_PATH / movie_id
    reviews_file = movie_dir / f"{movie_id}.csv"

    if not reviews_file.exists():
        return []

    reviews = []
    with open(reviews_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reviews.append({
                "date": row.get("Date of Review"),
                "user": row.get("User"),
                "usefulness_vote": int(row["Usefulness Vote"]) if row.get("Usefulness Vote") else None,
                "total_votes": int(row["Total Votes"]) if row.get("Total Votes") else None,
                "rating": float(row["User's rating out of 10"]) if row.get("User's rating out of 10") else None,
                "title": row.get("Review Title"),
                "review": row.get("Review")
            })
    return reviews


def append_review_to_csv(movie_id: str, username: str, rating: int, title: str, review_text: str):
    """Append a new review to the movie's CSV file."""
    csv_file = DATA_PATH / movie_id / f"{movie_id}.csv"
    file_exists = os.path.exists(csv_file)

    fieldnames = ["date", "user", "usefulness_vote", "total_votes", "rating", "title", "review"]

    new_review = {
        "date": datetime.utcnow().strftime("%d %B %Y"),
        "user": username,
        "usefulness_vote": 0,
        "total_votes": 0,
        "rating": rating,
        "title": title,
        "review": review_text
    }

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_review)

    return new_review


# --- Decorators ---
def movie_exists(func):
    """Decorator to ensure a valid movie ID before calling the route."""
    @wraps(func)
    def wrapper(movie_id: str, *args, **kwargs):
        movie = get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return func(movie_id, *args, movie=movie, **kwargs)
    return wrapper
