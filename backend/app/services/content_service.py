import numpy as np

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from app.core.loader import artifacts


def content_based_recommend(movie_name: str,tfidf_weight: float = 0.4,embedding_weight: float = 0.6,top_n: int = 5) -> pd.DataFrame:
    """Calculates hybrid content-based movie recommendations.

    Computes a weighted average of TF-IDF and embedding-based cosine 
    similarities to rank movies similar to the input title.

    Args:
        movie_name: The title of the movie to find recommendations for.
        tfidf_weight: Weight assigned to TF-IDF similarity.
        embedding_weight: Weight assigned to embedding similarity.
        top_n: Number of recommendations to return.

    Returns:
        pd.DataFrame: DataFrame containing 'movieId', 'title', and 
            'content_score' for the top-N recommended movies.

    Raises:
        ValueError: If the requested movie_name does not exist in the dataset.
    """
    new_movies = artifacts["content"]["movies_dataframe"]
    movie_indices = artifacts["content"]["movie_indices"]
    overview_embeddings = artifacts["content"]["overview_embeddings"]
    tfidf_vectorizer = artifacts["content"]["tfidf_vectorizer"]
    tfidf_matrix = artifacts["content"]["tfidf_matrix"]

    if not isinstance(movie_name, str) or not movie_name.strip():
        raise ValueError("Movie name must be a non-empty string")

    # Find movie index
    try:
        idx = movie_indices[movie_name]
    except KeyError:
        raise ValueError(f"Movie '{movie_name}' not found.")

    # TF-IDF Similarity
    tfidf_scores = cosine_similarity(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    # Embedding Similarity
    embedding_scores = cosine_similarity(
        overview_embeddings[idx].reshape(1, -1),
        overview_embeddings
    ).flatten()

    # Normalize scores

    tfidf_scores = MinMaxScaler().fit_transform(
        tfidf_scores.reshape(-1, 1)
    ).flatten()

    embedding_scores = MinMaxScaler().fit_transform(
        embedding_scores.reshape(-1, 1)
    ).flatten()

    total_weight = tfidf_weight + embedding_weight
    tfidf_normalized = tfidf_weight / total_weight  
    embedding_normalized = embedding_weight / total_weight 

    # Final Score
    final_scores = (
        tfidf_normalized * tfidf_scores +
        embedding_normalized * embedding_scores
    )

    # Sort
    movie_indices_sorted = np.argsort(final_scores)[::-1]

    # Remove queried movie
    movie_indices_sorted = movie_indices_sorted[
        movie_indices_sorted != idx
    ]

    # Top N
    top_movies = movie_indices_sorted[:top_n]

    # Return DataFrame
    recommendations = new_movies.iloc[top_movies][
        ["movieId", "title"]
    ]

    recommendations["content_score"] = final_scores[top_movies]

    return recommendations