from fastapi import APIRouter, Query
from app.core.loader import artifacts
from app.schemas.response import UserSearchResponse

router = APIRouter(prefix="/search_users", tags=["User Search"])


@router.get("/",response_model=UserSearchResponse,summary="Search User IDs")
def search_users(q: str = Query(...,min_length=1,description="Partial user ID"),limit: int = Query(10,ge=1,le=50)):
    """
    Search user IDs using prefix matching.
    """

    user_ids = artifacts["collabrative"]["valid_user_ids"]

    matches = [
        uid
        for uid in sorted(user_ids)
        if str(uid).startswith(q)
    ]

    matches = matches[:limit]

    return UserSearchResponse(
        users=matches,
        total=len(matches)
    )