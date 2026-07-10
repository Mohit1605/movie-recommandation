from fastapi import APIRouter, Query
import pandas as pd
import re  # ✅ ADD THIS IMPORT
from app.core.loader import artifacts
from app.schemas.response import MovieSearchResponse, MovieSuggestion

router = APIRouter(prefix="/movies", tags=["Movie Search"])

@router.get(
    "/search",
    response_model=MovieSearchResponse,
    summary="Search movies by title"
)
def search_movies(
    q: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="Movie title"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=20
    )
):
    """Searches for movies by title using a tiered matching strategy."""
    
    movies = artifacts["content"]["movies_dataframe"][
        ["movieId", "title"]
    ].copy()

    query = q.strip().lower()

    if not query:
        return MovieSearchResponse(
            movies=[],
            total=0
        )

    title_lower = movies["title"].str.lower()

    # 1. Exact match
    exact = movies[title_lower == query]

    # 2. Starts with query
    starts = movies[
        title_lower.str.startswith(query)
        & ~movies.index.isin(exact.index)
    ]

    # 3. Any word starts with query
    # ✅ FIX: Escape special regex characters
    escaped_query = re.escape(query)
    word_start = movies[
        title_lower.str.contains(rf"\b{escaped_query}", regex=True, na=False)
        & ~movies.index.isin(exact.index)
        & ~movies.index.isin(starts.index)
    ]

    # 4. Contains query anywhere
    # ✅ FIX: Use regex=False for simple substring search (faster, safer)
    contains = movies[
        title_lower.str.contains(query, regex=False, na=False)
        & ~movies.index.isin(exact.index)
        & ~movies.index.isin(starts.index)
        & ~movies.index.isin(word_start.index)
    ]

    results = (
        pd.concat(
            [exact, starts, word_start, contains],
            ignore_index=True
        )
        .head(limit)
    )

    return MovieSearchResponse(
        movies=[
            MovieSuggestion(
                movieId=int(row.movieId),
                title=row.title
            )
            for row in results.itertuples(index=False)
        ],
        total=len(results)
    )