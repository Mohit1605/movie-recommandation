from fastapi import FastAPI
from app.core.loader import load_models
import app.api.health as health_router
import app.api.content as content_router
import app.api.collabrative as collabrative_router
import app.api.hybrid as hybrid_router
import app.api.search_user as search_user_router
import app.api.search_movie_name as search_movie_name_router

app = FastAPI(title="Movie Recommandation System",version="1.0.0")


@app.on_event("startup")
def startup_event():
  load_models()

app.include_router(health_router.router)
app.include_router(content_router.router)
app.include_router(collabrative_router.router)
app.include_router(hybrid_router.router)
app.include_router(search_user_router.router)
app.include_router(search_movie_name_router.router)
