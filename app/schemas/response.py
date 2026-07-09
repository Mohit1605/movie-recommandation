from pydantic import BaseModel


class MovieRecommendation(BaseModel):
    movieId: int
    title: str
    content_score: float | None = None
    collabrative_score : float | None = None
    hybrid_score : float | None = None


class RecommendationResponse(BaseModel):
    recommendations: list[MovieRecommendation]

class UserSearchResponse(BaseModel):
    users: list[int]
    total: int

class MovieSuggestion(BaseModel):
    movieId: int
    title: str


class MovieSearchResponse(BaseModel):
    movies: list[MovieSuggestion]
    total: int