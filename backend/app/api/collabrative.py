from fastapi import APIRouter, HTTPException

from app.schemas.request import CollabrativeRequest
from app.schemas.response import RecommendationResponse
from app.services.collabrative_service import collabrative_based_recommend
from app.core.hepler_func import dataframe_to_response

router = APIRouter(prefix="/collabrative",tags=["Collabrative Recommendation"])

@router.post("/",response_model=RecommendationResponse,summary="Collabrative Based Movie Recommendation")
def recommend_movies(request: CollabrativeRequest):
  """Generates collaborative filtering movie recommendations for a given user.

    Args:request: Request object containing user_id and top_n.

    Returns:Formatted RecommendationResponse.

    Raises:HTTPException: 404 if input is invalid, 500 for internal errors.
    """
  try:
    recommendations = collabrative_based_recommend(user_id=request.user_id,top_n=request.top_n)

    return dataframe_to_response(recommendations)
  
  except ValueError as e: 
    raise HTTPException(status_code=404,detail=str(e))
  
  except RuntimeError as e: 
    raise HTTPException(status_code=500, detail=str(e))
  except KeyError as e:  
    raise HTTPException(status_code=404, detail=str(e))
  
  except Exception as e:
    raise HTTPException(status_code=500,detail=str(e))