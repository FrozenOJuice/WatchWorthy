import json
import csv
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

DATA_PATH = Path("backend/data/movieData")

def load_reviews(movie_id: str) -> List[Dict[str, Any]]:
    """Load reviews for a movie from its folder."""
    movie_dir = DATA_PATH / movie_id
    reviews_file = movie_dir / "reviews.csv"

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

def append_review_to_csv(movie_id: str, username: str, rating: float, title: str, review_text: str) -> Dict[str, Any]:
    """Append a new review to the movie's CSV file in its folder."""
    movie_dir = DATA_PATH / movie_id
    movie_dir.mkdir(exist_ok=True)
    
    csv_file = movie_dir / "reviews.csv"
    file_exists = os.path.exists(csv_file)

    fieldnames = ["Date of Review", "User", "Usefulness Vote", "Total Votes", 
                  "User's rating out of 10", "Review Title", "Review"]

    new_review = {
        "Date of Review": datetime.utcnow().strftime("%d %B %Y"),
        "User": username,
        "Usefulness Vote": 0,
        "Total Votes": 0,
        "User's rating out of 10": rating,
        "Review Title": title,
        "Review": review_text
    }

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_review)

    return {
        "date": new_review["Date of Review"],
        "user": new_review["User"],
        "usefulness_vote": new_review["Usefulness Vote"],
        "total_votes": new_review["Total Votes"],
        "rating": float(new_review["User's rating out of 10"]) if new_review["User's rating out of 10"] else None,
        "title": new_review["Review Title"],
        "review": new_review["Review"]
    }