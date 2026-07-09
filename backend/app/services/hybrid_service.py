from sklearn.preprocessing import MinMaxScaler
from app.services.content_service import content_based_recommend
from app.core.loader import artifacts
from app.services.prediction import predict_rating
import pandas as pd

def hybrid_recommend(user_id,movie_name,top_k=50,top_n=10,content_weight=0.6,collabrative_weight=0.4):
    """Generates hybrid movie recommendations by combining content and collaborative scores.

    Retrieves content-based candidates, calculates collaborative ratings for those 
    candidates, normalizes both scores, and ranks them based on a weighted hybrid score.

    Args:
        user_id: The ID of the user requesting recommendations.
        movie_name: The title of the seed movie.
        top_k: Number of candidate movies to initially retrieve.
        top_n: Number of final recommendations to return.
        content_weight: Weight assigned to the content-based score.
        collabrative_weight: Weight assigned to the collaborative score.

    Returns:
        pd.DataFrame: DataFrame containing 'movieId', 'title', 'content_score',
            'collabrative_score', and 'hybrid_score'.

    Raises:
        KeyError: If the provided user_id is invalid.
        RuntimeError: If the hybrid recommendation process fails.
    """
    try:
      valid_user_ids = artifacts["collabrative"]["valid_user_ids"]
      if not isinstance(user_id, int):
        raise ValueError("user_id must be an integer")
    
      if not isinstance(movie_name, str) or not movie_name.strip():
        raise ValueError("movie_name must be a non-empty string")
      
      # Validate User
      if user_id not in valid_user_ids:
          raise KeyError(f"User ID {user_id} not found.")

      # Content Candidates
      candidates = content_based_recommend(
          movie_name=movie_name,
          top_n=top_k
      )

      if isinstance(candidates, str):
          return candidates
      if candidates is None or len(candidates) == 0:
        raise ValueError(f"No recommendations found for movie '{movie_name}'")
      # Predict Ratings
      collabrative_scores = []

      for movie_id in candidates["movieId"]:

          predicted_rating = predict_rating(
                user_id,
                movie_id,
                artifacts
            )

          collabrative_scores.append(predicted_rating)

      candidates["collabrative_score"] = collabrative_scores


      # Normalize Scores
      scaler = MinMaxScaler()

      # candidates["content_score"] = scaler.fit_transform(
      #     candidates[["content_score"]]
      # )

      candidates["collabrative_score"] = scaler.fit_transform(
          candidates[["collabrative_score"]]
      )

      # Hybrid Score
      candidates["hybrid_score"] = (
          content_weight * candidates["content_score"] +
          collabrative_weight * candidates["collabrative_score"]
      )

      # Final Ranking
      candidates = candidates.sort_values(
          "hybrid_score",
          ascending=False
      )

      recommand_list = candidates[
          [
              "movieId",
              "title",
              "content_score",
              "collabrative_score",
              "hybrid_score"
          ]
      ].head(top_n)
      
      return pd.DataFrame(recommand_list)
    except Exception as e:
        raise RuntimeError(f"Hybrid recommendation failed: {e}")