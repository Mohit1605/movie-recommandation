import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from app.core.loader import artifacts


def content_based_recommend(movie_name: str,tfidf_weight: float = 0.35,embedding_weight: float = 0.65,top_n: int = 5):
    
    new_movies = artifacts["content"]["movies_dataframe"]
    movie_indices = artifacts["content"]["movie_indices"]
    overview_embeddings = artifacts["content"]["overview_embeddings"]
    tfidf_vectorizer = artifacts["content"]["tfidf_vectorizer"]
    tfidf_matrix = artifacts["content"]["tfidf_matrix"]

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
    scaler = MinMaxScaler()

    tfidf_scores = scaler.fit_transform(
        tfidf_scores.reshape(-1, 1)
    ).flatten()

    embedding_scores = scaler.fit_transform(
        embedding_scores.reshape(-1, 1)
    ).flatten()

    # Final Score
    final_scores = (
        tfidf_weight * tfidf_scores +
        embedding_weight * embedding_scores
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
    ].copy()

    recommendations["content_score"] = final_scores[top_movies]

    return recommendations