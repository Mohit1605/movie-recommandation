import pandas as pd
from app.core.loader import artifacts
from app.services.prediction import predict_rating

def collabrative_based_recommend(user_id, top_n=10):
    """Generates movie recommendations for a user via collaborative filtering.

    Filters out already-watched movies, calculates predicted ratings for 
    unseen movies, and returns the top-N results.

    Args:
        user_id: The identifier of the user to get recommendations for.
        top_n: Number of recommendations to return (default 10).

    Returns:
        pd.DataFrame: A DataFrame containing 'movieId', 'title', and 
            'collabrative_score' for the recommended movies.

    Raises:
        KeyError: If the provided user_id is not in the valid user registry.
    """
    all_movies_id = artifacts["collabrative"]["all_movies_id"] 
    movies_dict = artifacts["collabrative"]["movie_dict"] 
    user_history = artifacts["collabrative"]["user_history"]
    valid_user_ids = artifacts["collabrative"]["valid_user_ids"]

    if not isinstance(user_id, int):
        raise ValueError("user_id must be an integer")

    if user_id not in valid_user_ids:
        raise KeyError(f"User with ID {user_id} not found.")

    # watched_movies = user_history[user_id] old
    watched_movies = set(user_history[user_id])

    recommendations = []

    for movie_id in all_movies_id:

        if movie_id in watched_movies:
            continue

        predicted_rating = predict_rating(
            user_id,
            movie_id,
            artifacts
        )

        recommendations.append((movie_id, predicted_rating))

    recommendations.sort(
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = recommendations[:top_n]

    results = []

    for movie_id, score in recommendations:

        results.append({
            "movieId": movie_id,
            "title": movies_dict.get(movie_id, "Unknown Movie"),
            "collabrative_score": round(score, 3)
        })

    return pd.DataFrame(results)