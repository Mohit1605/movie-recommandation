from sklearn.preprocessing import MinMaxScaler
from app.services.content_service import content_based_recommend
from app.core.loader import artifacts
from app.services.prediction import predict_rating
import pandas as pd

def hybrid_recommend(user_id,movie_name,top_k=50,top_n=10,content_weight=0.4,collabrative_weight=0.6):
    try:
      valid_user_ids = artifacts["collabrative"]["valid_user_ids"]

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
        print("error aave che",str(e))
        return str(e)