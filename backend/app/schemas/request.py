from pydantic import BaseModel, Field


class ContentRequest(BaseModel):
    title: str = Field(..., description="Movie title")
    top_n: int = Field(default=10, ge=1, le=50)


class CollabrativeRequest(BaseModel):
    user_id: int = Field(..., description="User ID")
    top_n: int = Field(default=10, ge=1, le=50)


class HybridRequest(BaseModel):
    user_id: int = Field(..., description="User ID")
    title: str = Field(..., description="Movie title")
    top_n: int = Field(default=10, ge=1, le=50)