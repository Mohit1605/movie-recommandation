import joblib
from app.core.logger_func import logger
from app.core.config import CONTENT_DIR, COLLABRATIVE_DIR


artifacts = {
    "content": {},
    "collabrative": {}
}


def load_content_models():
  """Load all content-based recommendation artifacts."""
  try:

    logger.info("Loading Content-Based Models...")
    logger.info("Loading Content-Based Models - movie dataframe...")
    artifacts["content"]["movies_dataframe"] = joblib.load(CONTENT_DIR / "movies_dataframe.pkl")

    logger.info("Loading Content-Based Models - movie_indices...")
    artifacts["content"]["movie_indices"] = joblib.load(CONTENT_DIR / "movie_indices.pkl")

    logger.info("Loading Content-Based Models - overview_embeddings...")
    artifacts["content"]["overview_embeddings"] = joblib.load(CONTENT_DIR / "overview_embeddings.pkl")

    logger.info("Loading Content-Based Models - tfidf_matrix...")
    artifacts["content"]["tfidf_matrix"] = joblib.load(CONTENT_DIR / "tfidf_matrix.pkl")

    logger.info("Loading Content-Based Models - tfidf_vectorizer...")
    artifacts["content"]["tfidf_vectorizer"] = joblib.load(CONTENT_DIR / "tfidf_vectorizer.pkl")

    logger.info("✓ Content-Based Models Loaded")
  
  except Exception as e:
    logger.error(f"error occured at load collabrative :{str(e)}")
    raise

def load_collabrative_models():
  """Load all collabrative recommendation artifacts."""
  try:
     
    logger.info("Loading Collabrative Models...")

    logger.info("Loading Collabrative-Based Models - all_movies_id...")
    artifacts["collabrative"]["all_movies_id"] = joblib.load(COLLABRATIVE_DIR / "all_movies_id.pkl")

    logger.info("Loading Collabrative-Based Models - movie_dict...")
    artifacts["collabrative"]["movie_dict"] = joblib.load(COLLABRATIVE_DIR / "movie_dict.pkl")

    logger.info("Loading Collabrative-Based Models - user_history...")
    artifacts["collabrative"]["user_history"] = joblib.load(COLLABRATIVE_DIR / "user_history.pkl")

    logger.info("Loading Collabrative-Based Models - valid_user_ids...")
    artifacts["collabrative"]["valid_user_ids"] = joblib.load(COLLABRATIVE_DIR / "valid_user_ids.pkl")
    
    logger.info("Loading Collabrative-Based Models - pu...")
    artifacts["collabrative"]["pu"] = joblib.load(
        COLLABRATIVE_DIR / "pu.joblib"
    )

    logger.info("Loading Collabrative-Based Models - qi...")
    artifacts["collabrative"]["qi"] = joblib.load(
        COLLABRATIVE_DIR / "qi.joblib"
    )

    logger.info("Loading Collabrative-Based Models - bu...")
    artifacts["collabrative"]["bu"] = joblib.load(
        COLLABRATIVE_DIR / "bu.joblib"
    )

    logger.info("Loading Collabrative-Based Models - bi...")
    artifacts["collabrative"]["bi"] = joblib.load(
        COLLABRATIVE_DIR / "bi.joblib"
    )

    logger.info("Loading Collabrative-Based Models - global_mean...")
    artifacts["collabrative"]["global_mean"] = joblib.load(
        COLLABRATIVE_DIR / "global_mean.joblib"
    )

    logger.info("Loading Collabrative-Based Models - user_mapping...")
    artifacts["collabrative"]["user_mapping"] = joblib.load(
        COLLABRATIVE_DIR / "user_mapping.joblib"
    )

    logger.info("Loading Collabrative-Based Models - movie_mapping...")
    artifacts["collabrative"]["movie_mapping"] = joblib.load(
        COLLABRATIVE_DIR / "movie_mapping.joblib"
    )

    logger.info("✓ collabrative Models Loaded")

  except Exception as e:
    logger.error(f"error occured at load collabrative :{str(e)}")
    raise

def load_models():
  """Load all model artifacts."""
  try:
    load_content_models()
    load_collabrative_models()

    logger.info("✓ All Models Loaded Successfully")
  
  except ValueError as e:
    logger.error(f"Validation error during model loading: {str(e)}")  
    raise
  except FileNotFoundError as e:
    logger.error(f"Model file not found: {str(e)}")
    raise
  except Exception as e:
    logger.error(f"Unexpected error during model loading: {str(e)}")  
    raise



