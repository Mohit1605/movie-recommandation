from pydantic import BaseModel, Field, validator

class ContentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Movie title")
    top_n: int = Field(default=10, ge=1, le=50)
    
    @validator('title')
    def title_not_empty_or_whitespace(cls, v):
        if not v.strip():
            raise ValueError('title cannot be empty or whitespace-only')
        return v

class CollabrativeRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID (must be positive)")
    top_n: int = Field(default=10, ge=1, le=50)

class HybridRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID (must be positive)")
    title: str = Field(..., min_length=1, max_length=100, description="Movie title")
    top_n: int = Field(default=10, ge=1, le=50)
    
    @validator('title')
    def title_not_empty_or_whitespace(cls, v):
        if not v.strip():
            raise ValueError('title cannot be empty or whitespace-only')
        return v