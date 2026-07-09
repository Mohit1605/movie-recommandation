from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODELS_DIR = BASE_DIR / "model_supporting_file"

CONTENT_DIR = MODELS_DIR / "Content_Based_Data"

COLLABRATIVE_DIR = MODELS_DIR / "Collabrative_Based_Data"

print(BASE_DIR)
print(CONTENT_DIR)
print(COLLABRATIVE_DIR)