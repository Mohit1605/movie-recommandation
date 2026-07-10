import numpy as np
from typing import Dict, Any

def predict_rating(user_id:int, movie_id:int, artifacts:Dict[str,Any]) -> float:
    """Predicts a user's rating for a movie using Matrix Factorization (SVD).

    Calculates the predicted rating by combining the global mean, user and item 
    biases, and the dot product of the user and item latent factors. Handles 
    unseen users/movies by falling back to available bias terms or the global mean.

    Args:
        user_id: The ID of the user.
        movie_id: The ID of the movie.
        artifacts: Dictionary containing collaborative filtering matrices and biases.

    Returns:
        float: The predicted rating, clipped between 0.5 and 5.0.
    """
    collab = artifacts["collabrative"]

    pu = collab["pu"]
    qi = collab["qi"]

    bu = collab["bu"]
    bi = collab["bi"]

    global_mean = collab["global_mean"]

    user_mapping = collab["user_mapping"]
    movie_mapping = collab["movie_mapping"]

    min_rating = 0.5
    max_rating = 5.0

    known_user = user_id in user_mapping
    known_movie = movie_id in movie_mapping

    if not known_user and not known_movie:
        pred = global_mean

    elif not known_user:
        pred = global_mean + bi[movie_mapping[movie_id]]

    elif not known_movie:
        pred = global_mean + bu[user_mapping[user_id]]

    else:

        u = user_mapping[user_id]
        i = movie_mapping[movie_id]

        pred = (
            global_mean
            + bu[u]
            + bi[i]
            + np.dot(pu[u], qi[i])
        )

    pred = np.clip(pred, min_rating, max_rating)

    return float(pred)