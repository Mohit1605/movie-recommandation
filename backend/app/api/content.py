from fastapi import APIRouter, HTTPException

from app.schemas.request import ContentRequest
from app.schemas.response import RecommendationResponse
from app.services.content_service import content_based_recommend
from app.core.hepler_func import dataframe_to_response

router = APIRouter(prefix="/content",tags=["Content Recommendation"])

@router.post("/",response_model=RecommendationResponse,summary="Content Based Movie Recommendation")
def recommend_movies(request: ContentRequest):
  """Generates content-based movie recommendations similar to a given title.

    Args:request: Request object containing movie title and top_n.

    Returns:Formatted RecommendationResponse.

    Raises:HTTPException: 404 if movie not found, 500 for internal errors.
    """
  try:
    recommendations = content_based_recommend(movie_name=request.title,top_n=request.top_n)

    return dataframe_to_response(recommendations)
  
  except ValueError as e: 
    raise HTTPException(status_code=404,detail=str(e))

  except Exception as e:
    raise HTTPException(status_code=500,detail=str(e))