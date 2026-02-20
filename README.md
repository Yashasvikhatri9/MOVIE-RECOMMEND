# Movie Recommender ML Module

This repository contains the machine learning component of a movie recommendation system.

## Structure
```
movie-recommender-ml/
├── data/
│   ├── raw/                     # Original movie dataset
│   └── processed/               # Cleaned dataset for training
│       └── movies_clean.csv
│       └── movies_with_trailers_safe.csv
├── models/
│   ├── vector.pkl                # Trained TF-IDF vectorizer
│   └── vector_reduced.pkl         # Precomputed embeddings
│   └── svd_model.pkl
├── notebooks/
│   ├── 1_data_cleaning.ipynb    # cleaning, preprocessing
│   └── 2_model_training.ipynb   # model training & saving
├── recommend_model.py           # your main inference module
├── requirements.txt             # dependencies
├── README.md                    # documentation
└── .gitignore
```

## Usage
- Import `recommend_movies` in Python projects.
- Ensure `vector.pkl`, `vector_reduced.pkl`, `svd_model.pkl`, `movies_with_trailers_safe.csv` and `movies_clean.csv` exist in the paths above.
