from fastapi import APIRouter

router =  APIRouter(prefix="/health",tags=["health"])

@router.get("/")
def health():
  """ Returns the status of the API."""
  return{"status":"Running"}