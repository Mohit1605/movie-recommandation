from fastapi import APIRouter, HTTPException
from app.core.logger_func import logger
from app.schemas.request import HybridRequest
from app.schemas.response import RecommendationResponse
from app.services.hybrid_service import hybrid_recommend
from app.core.hepler_func import dataframe_to_response

router = APIRouter(prefix="/Hybrid",tags=["Hybrid Recommendation"])

@router.post("/",response_model=RecommendationResponse,summary="Hybrid Based Movie Recommendation")
def recommend_movies(request: HybridRequest):
  """Generates hybrid movie recommendations based on user history and movie content.

    Args:request: Request object containing user_id, title, and top_n.

    Returns:Formatted RecommendationResponse.

    Raises:HTTPException: 404 if input data is invalid, 500 for internal errors.
    """
  try:
    recommendations = hybrid_recommend(user_id=request.user_id,movie_name=request.title,top_n=request.top_n)
    return dataframe_to_response(recommendations)
    
  except ValueError as e: 
    raise HTTPException(status_code=404,detail=str(e))

  except Exception as e:
    logger.error("erorr aave che",str(e))
    raise HTTPException(status_code=500,detail=str(e))