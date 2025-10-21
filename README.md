# Movie Recommender ML Module

This repository contains the machine learning component of a movie recommendation system.

## Structure
```
movie-recommender-ml/
├── data/
│   ├── raw/                     # Original movie dataset
│   └── processed/               # Cleaned dataset for training
│       └── movies_clean.csv
├── models/
│   ├── tfidf.pkl                # Trained TF-IDF vectorizer
│   └── tfidf_matrix.pkl         # Precomputed embeddings
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
- Ensure `tfidf.pkl`, `tfidf_matrix.pkl`, and `movies_clean.csv` exist in the paths above.
