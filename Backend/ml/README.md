# ML Module - Movie Recommender

This folder contains the **ML part** of a movie recommender system.

## Structure

```
ml/
├── recommend_model.py   # Inference module
├── train_model.ipynb    # Notebook for training TF-IDF / model
├── requirements.txt     # ML dependencies
├── data/
│   ├── raw/             # Raw datasets
│   └── processed/       # Cleaned dataset (movies_clean.csv)
├── models/
│   ├── tfidf.pkl
│   └── tfidf_matrix.pkl
├── __init__.py
```

## Usage

```python
from ml.recommend_model import recommend_movies

recommend_movies("romantic comedy")
```

