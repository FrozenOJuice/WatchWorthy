from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from backend.reviews import schemas
from backend.reviews import utils as review_utils
from backend.movies import utils as movie_utils
from backend.authentication.security import get_current_user
from backend.authentication import utils as auth_utils
from backend.ratings import utils as ratings_utils

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/{movie_id}", response_model=schemas.ReviewListResponse)
@movie_utils.movie_exists
def get_reviews(
    movie_id: str,
    movie: dict,
    user: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    min_usefulness_vote: Optional[int] = None,
    min_total_votes: Optional[int] = None,
    skip: int = 0,
    limit: int = 50
):
    reviews = review_utils.load_reviews(movie_id)

    if user:
        reviews = [r for r in reviews if r["user"] and user.lower() in r["user"].lower()]
    if start_date:
        reviews = [r for r in reviews if r["date"] and r["date"] >= start_date]
    if end_date:
        reviews = [r for r in reviews if r["date"] and r["date"] <= end_date]
    if min_rating is not None:
        reviews = [r for r in reviews if r["rating"] and r["rating"] >= min_rating]
    if max_rating is not None:
        reviews = [r for r in reviews if r["rating"] and r["rating"] <= max_rating]
    if min_usefulness_vote is not None:
        reviews = [r for r in reviews if r["usefulness_vote"] and r["usefulness_vote"] >= min_usefulness_vote]
    if min_total_votes is not None:
        reviews = [r for r in reviews if r["total_votes"] and r["total_votes"] >= min_total_votes]

    return {"reviews": reviews[skip: skip + limit]}

@router.post("/{movie_id}")
@movie_utils.movie_exists
def add_review(
    movie_id: str,
    movie: dict,
    review_data: schemas.ReviewCreate,
    current_user=Depends(get_current_user)
):
    users = auth_utils.load_users()
    user = next((u for u in users if u['user_id'] == current_user.user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # If rating is provided in review, also save it to ratings system
    if review_data.rating is not None:
        ratings_utils.set_user_rating(current_user.user_id, movie_id, review_data.rating)

    new_review = review_utils.append_review_to_csv(
        movie_id=movie_id,
        username=user["username"],
        rating=review_data.rating,
        title=review_data.review_title,
        review_text=review_data.review_text
    )

    return {"message": "Review added successfully", "review": new_review}