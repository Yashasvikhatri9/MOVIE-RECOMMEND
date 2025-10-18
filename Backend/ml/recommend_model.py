import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Load model and data
tfidf = joblib.load("models/tfidf.pkl")
tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")
movies = pd.read_csv("data/processed/movies_clean.csv")

def recommend_movies(query: str, top_k: int = 10):
    if not query.strip():
        return []
    query_vec = tfidf.transform([query])
    sims = cosine_similarity(query_vec, tfidf_matrix).flatten()
    idx = sims.argsort()[-top_k:][::-1]
    return movies.iloc[idx][["id","title","genres","vote_average"]].to_dict(orient="records")

if __name__ == "__main__":
    example_query = "action adventure"
    print(pd.DataFrame(recommend_movies(example_query)))
