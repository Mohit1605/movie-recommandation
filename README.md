# 🎬 Hybrid Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?style=flat&logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=flat)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=flat&logo=docker)
![Status](https://img.shields.io/badge/Status-Complete-success?style=flat)

A production-ready **Hybrid Movie Recommendation System** combining **Content-Based Filtering**, **Collaborative Filtering (SVD)**, and deployed via **FastAPI** with **Docker** containerization.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Why Hybrid?](#why-hybrid)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Dataset](#dataset)
- [Installation](#installation)
- [API Usage](#api-usage)
- [Performance](#performance)
- [Future Enhancements](#future-enhancements)

---

## Overview

Modern streaming platforms need intelligent recommendation systems to help users discover relevant content. This project implements a **hybrid recommendation engine** that combines multiple techniques to overcome limitations of single-approach systems.

Instead of choosing between content similarity or user preferences, the system intelligently merges both methods:
1. **Content-Based Filtering** identifies similar movies using metadata
2. **Collaborative Filtering (SVD)** predicts personalized ratings
3. **Hybrid Pipeline** combines both for superior recommendations

**Key Advantage**: Two-stage retrieval reduces computational overhead while improving recommendation quality.

---

## Why Hybrid?

### Content-Based Filtering
- ✅ Works with limited user history
- ✅ Recommends similar movies
- ❌ Cannot capture community preferences
- ❌ May become repetitive

### Collaborative Filtering
- ✅ Highly personalized
- ✅ Discovers hidden patterns
- ❌ Cold-start problem
- ❌ Requires historical data

### Hybrid Approach
**Combines strengths of both** to deliver personalized recommendations of similar movies.

---

## Features

### 🎥 Content-Based Recommendation
- Movie similarity using weighted metadata (genres, keywords, cast, crew)
- TF-IDF vectorization
- Sentence Transformer embeddings
- Cosine similarity matching

### 👤 Collaborative Filtering
- Matrix factorization using SVD
- User preference learning
- Predicts unseen ratings
- Top-N personalized recommendations

### 🔥 Hybrid Recommendation
- Two-stage pipeline
- Candidate generation via content similarity
- Personalized re-ranking via SVD
- ~0.5 second inference time

### ⚡ Production Backend
- FastAPI REST APIs
- Modular service architecture
- Joblib artifact caching
- Docker containerization
- Swagger UI documentation

---

## Technology Stack

| Category | Tools |
|----------|-------|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **ML** | Scikit-Learn, Surprise (SVD), Sentence Transformers |
| **NLP** | TF-IDF Vectorizer, all-MiniLM-L6-v2 |
| **Data** | Pandas, NumPy |
| **Deployment** | Docker, Docker Compose |
| **Development** | VS Code, Git |

---

## System Architecture

```
┌─────────────────────┐
│      FastAPI        │
│   REST Server       │
└──────────┬──────────┘
           │
    ┌──────┼──────┐
    │      │      │
    ▼      ▼      ▼
  Content Collab Hybrid
  Service Service Service
    │      │      │
    └──────┼──────┘
           ▼
    ┌────────────────┐
    │ Model Artifacts│
    │                │
    │ • TF-IDF       │
    │ • Embeddings   │
    │ • SVD Model    │
    │ • Similarity   │
    │ • Dictionaries │
    └────────────────┘
```

---

## Recommendation Pipeline

### Hybrid Workflow

```
User ID + Movie Name
        │
        ▼
Content-Based Filtering
        │
        ▼
Top 50 Similar Movies
        │
        ▼
Collaborative Filtering (SVD)
        │
        ▼
Predict User Ratings
        │
        ▼
Rank by Predicted Score
        │
        ▼
Return Top-N Results
```

This two-stage approach significantly reduces search space while preserving quality.

---

## Dataset

**Source**: [The Movies Dataset (Kaggle)](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

| Metric | Value |
|--------|-------|
| Movies | ~45,000 |
| Users | ~270,000 |
| Ratings | ~26 Million |
| Rating Scale | 0.5 – 5.0 |

### Metadata Used
- **Genres** (weight × 2)
- **Keywords** (weight × 2)
- **Cast** (weight × 2)
- **Crew** (weight × 2)

Weighted features improve semantic similarity and recommendation relevance.

---

## Installation

### Prerequisites

```
Python 3.11+
Docker & Docker Compose (latest)
Git
```

### Clone Repository

```bash
git clone https://github.com/Mohit1605/movie-recommandation.git
cd movie-recommandation
```

### Local Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

### Docker Setup

```bash
# First time build
docker compose up --build

# Subsequent runs
docker compose up

# Run detached
docker compose up -d

# Stop containers
docker compose down
```

---

## API Usage

Access interactive documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/recommend/content` | POST | Similar movies |
| `/recommend/collaborative` | POST | Personalized movies |
| `/recommend/hybrid` | POST | Personalized similar movies |
| `/search/movies` | GET | Search movies |
| `/search/users` | GET | Search users |

---

## Example Requests

### Content-Based Recommendation

**Request**
```json
{
    "movie_name": "Avatar",
    "top_n": 10
}
```

**Response**
```json
{
    "recommendations": [
        {
            "movieId": 72998,
            "title": "Avatar",
            "similarity_score": 0.94
        },
        {
            "movieId": 19995,
            "title": "Avatar: The Way of Water",
            "similarity_score": 0.89
        }
    ]
}
```

### Collaborative Recommendation

**Request**
```json
{
    "user_id": 25,
    "top_n": 10
}
```

**Response**
```json
{
    "recommendations": [
        {
            "movieId": 4973,
            "title": "The Lord of the Rings: The Fellowship of the Ring",
            "predicted_rating": 4.82
        },
        {
            "movieId": 278,
            "title": "The Shawshank Redemption",
            "predicted_rating": 4.75
        }
    ]
}
```

### Hybrid Recommendation

**Request**
```json
{
    "user_id": 25,
    "movie_name": "Avatar",
    "top_n": 10
}
```

**Response**
```json
{
    "recommendations": [
        {
            "movieId": 603,
            "title": "The Matrix",
            "predicted_rating": 4.91,
            "content_similarity": 0.83
        },
        {
            "movieId": 558,
            "title": "Spider-Man",
            "predicted_rating": 4.68,
            "content_similarity": 0.79
        }
    ]
}
```

---

## Project Structure

```
movie-recommandation/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── content.py
│   │   │   ├── collaborative.py
│   │   │   ├── hybrid.py
│   │   │   └── search.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── content_service.py
│   │   │   ├── collab_service.py
│   │   │   └── hybrid_service.py
│   │   ├── utils/
│   │   │   └── artifacts.py
│   │   └── main.py
│   │
│   ├── artifacts/
│   │   ├── tfidf_vectorizer.pkl
│   │   ├── embeddings.npy
│   │   ├── svd_model.pkl
│   │   ├── similarity_matrix.npz
│   │   └── mappings.json
│   │
│   ├── notebooks/
│   │   ├── data_exploration.ipynb
│   │   ├── content_model.ipynb
│   │   └── collab_model.ipynb
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Content-Based Filtering

### How It Works

Each movie is represented as weighted metadata:
- Genres
- Keywords
- Cast
- Crew

These are combined and converted to numerical vectors using **TF-IDF** and **Sentence Transformers**.

### Example Feature Engineering

**Movie**: Avatar (2009)

```
Genres: Science Fiction, Adventure, Fantasy
Keywords: Alien, Avatar, Spaceship
Cast: Sam Worthington, Zoe Saldana
Crew: James Cameron
```

↓ (Vectorization)

```
TF-IDF Vector: [0.23, 0.45, 0.12, ...]
Embedding: [-0.12, 0.45, 0.78, ...]
```

### Recommendation Process

1. Lookup movie's weighted tags
2. Generate TF-IDF vector
3. Get semantic embedding
4. Compute cosine similarity with all movies
5. Rank by similarity score
6. Return top-N results

---

## Collaborative Filtering

### Matrix Factorization (SVD)

The system uses **Singular Value Decomposition** to learn latent factors:
- **User Latent Factors**: Represent user preferences
- **Movie Latent Factors**: Represent movie characteristics

### How Predictions Work

```
User Preference Vector × Movie Characteristic Vector = Predicted Rating
```

### Recommendation Process

1. Get list of unwatched movies for user
2. Predict rating for each movie using SVD
3. Filter movies with low predicted ratings
4. Sort by predicted rating (descending)
5. Return top-N recommendations

### Model Performance

| Metric | Score |
|--------|-------|
| RMSE | 0.8758 |
| MAE | 0.6721 |

Lower values indicate better prediction accuracy.

---

## Hybrid Recommendation

### Two-Stage Strategy

**Stage 1: Candidate Generation**
- Input: Movie name
- Process: Content-based filtering
- Output: Top 50 similar movies

**Stage 2: Personalized Ranking**
- Input: Top 50 candidates + User ID
- Process: SVD prediction
- Output: Top-N ranked by predicted user preference

### Benefits

✅ Reduces computation (50 predictions vs 45,000)
✅ Better personalization
✅ Improved recommendation relevance
✅ Maintains quality while improving speed

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Model Size | ~442 MB |
| Startup Time | 1–2 minutes |
| Avg Prediction | ~0.5 seconds |
| Artifact Loading | First-time only |

**Note**: Initial startup includes artifact loading. Subsequent predictions are cached.

---

## Model Artifacts

All trained models are serialized using **Joblib** and loaded at startup:

- SVD Collaborative Model
- TF-IDF Vectorizer
- Sentence Embeddings
- Cosine Similarity Matrix
- Movie ID Mappings
- User ID Mappings
- Metadata Lookups

This approach eliminates repeated training and ensures consistent predictions.

---

## Engineering Decisions

### Why Hybrid Over Single Approach?
- Content-based captures movie similarity
- Collaborative captures user preferences
- Hybrid leverages both for superior results

### Why Two-Stage Pipeline?
Predicting ratings for all 45,000 movies would be slow. Two-stage approach reduces to 50 predictions per request.

### Why SVD?
- Proven accuracy for recommendations
- Handles sparse matrices efficiently
- Fast inference time
- Production-ready implementation

### Why Sentence Transformers?
TF-IDF alone captures keywords. Semantic embeddings understand contextual similarity between movies.

### Why Joblib?
Precomputed artifacts enable instant deployment without retraining models.

---

## Running Locally

### Start Backend

```bash
cd backend
source .venv/bin/activate  # Activate venv
uvicorn app.main:app --reload
```

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### Test APIs

Open Swagger UI: `http://localhost:8000/docs`

1. Click on endpoint
2. Click "Try it out"
3. Enter parameters
4. Execute request
5. View JSON response

---

## Docker Deployment

### Build and Run

```bash
# Build images
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild after changes
docker compose up --build
```

### Environment Variables

Create `.env` in backend directory:

```
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
MAX_WORKERS=4
```

---

## Current Limitations

- Recommendations limited to dataset movies
- New users need rating history for personalization
- New movies require model retraining
- No automatic dataset updates

---

## Future Enhancements

### Short Term
- [ ] TMDB API integration for new movies
- [ ] Recommendation explanations
- [ ] User feedback loop
- [ ] Request caching with Redis

### Medium Term
- [ ] New user onboarding workflow
- [ ] Incremental model updates
- [ ] Model monitoring dashboard
- [ ] A/B testing framework

### Long Term
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Multi-recommendation strategies
- [ ] Real-time model updating
- [ ] Advanced analytics dashboard

---

## Deployment Checklist

- [ ] Test all API endpoints
- [ ] Verify artifact loading
- [ ] Check Docker image size
- [ ] Validate environment variables
- [ ] Test prediction latency
- [ ] Monitor memory usage
- [ ] Set up logging
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Setup error monitoring

---

## Challenges & Solutions

### Challenge 1: Large Model Artifacts (~442 MB)
**Solution**: Load artifacts once at startup, cache in memory

### Challenge 2: Slow Prediction with 45K Movies
**Solution**: Two-stage pipeline reduces to 50 predictions

### Challenge 3: 1-2 Minute Startup Time
**Solution**: Optimize artifact loading, parallelize initialization

### Challenge 4: Memory Management
**Solution**: Use efficient data structures, precompute similarities

---

## Lessons Learned

1. **Data Quality Matters**: Feature engineering is as important as model selection
2. **Hybrid > Single Approach**: Combining techniques yields better results
3. **Separate Training & Inference**: Offline training enables fast online serving
4. **Architecture Matters**: Modular design enables easier maintenance
5. **Engineering = ML**: Deployment challenges require careful engineering

---

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add feature"`
4. Push branch: `git push origin feature/your-feature`
5. Open Pull Request

---

## Author

**Mohit Parmar**
- Machine Learning & Backend Developer
- GitHub: [@Mohit1605](https://github.com/Mohit1605)
- LinkedIn: [Your LinkedIn]
- Email: [Your Email]

---

## License

MIT License - See LICENSE file for details

You are free to use, modify, and distribute this project.

---

## Acknowledgements

- **Kaggle** - The Movies Dataset
- **FastAPI** - Modern web framework
- **Scikit-Learn** - ML utilities
- **Surprise** - Collaborative filtering
- **Sentence Transformers** - Semantic embeddings
- **Docker** - Containerization

---

## Support

If you found this project helpful:
- ⭐ Star the repository
- 🍴 Fork and contribute
- 📢 Share with others

---

## Questions & Feedback

Open an issue or reach out via:
- Email
- GitHub Discussions
- LinkedIn

**Happy Recommending! 🎬🚀**