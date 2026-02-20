import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request
from huggingface_hub import hf_hub_download
app = Flask(__name__)
vector = joblib.load(hf_hub_download("yashasvi-01-02/movie-recommendation", "models/vector.joblib"))
vector_reduced = joblib.load(hf_hub_download("yashasvi-01-02/movie-recommendation", "models/vector_reduced.joblib"))
svd = joblib.load(hf_hub_download("yashasvi-01-02/movie-recommendation", "models/svd_model.joblib"))
movie = pd.read_csv(hf_hub_download("yashasvi-01-02/movie-recommendation", "data/processed/movies_clean.csv"))

def build_query(user_info: dict):
    watched = user_info.get("watched_ids", [])
    searched = user_info.get("searched_ids", [])
    bookmarked = user_info.get("bookmarked_movies", [])
    all_movies = list(set(watched + searched + bookmarked))
    genres = user_info.get("genres", "")
    language = user_info.get("language", "")
    if all_movies:
        selected = movie[movie["id"].isin(all_movies)]
        combined_text = " ".join(selected["combined_text"].dropna().tolist())
        if combined_text.strip():
            return (combined_text + " " + genres + " " + language).strip()
    first_query = (genres + " " + language).strip()
    return first_query

def recommend_movies(query: str, top_n: int = 10):
    if not query or not query.strip():
        return []
    movies_filtered = movie[(movie["vote_average"] > 2) & (movie["vote_count"] > 40)]
    query_vec = vector.transform([query.lower()])
    query_vec_reduced = svd.transform(query_vec)
    similarity = cosine_similarity(query_vec_reduced, vector_reduced[movies_filtered.index.to_numpy()]).flatten()
    top_indices = similarity.argsort()[::-1][2:top_n+1]
    recommended = movies_filtered.iloc[top_indices][['id','imdb_id','title','vote_average','vote_count','genres','backdrop_path','poster_path','trailer_link']].copy()
    recommended['similarity'] = similarity[top_indices]
    return recommended.to_dict(orient="records")

# Flask API endpoint
@app.route("/recommend_movies", methods=["POST"])
def recommend_movies_api():
    user_info = request.json or {}
    user_id = user_info.get("user")
    query_text = build_query(user_info)
    recommendations = recommend_movies(query_text)
    bookmarked = user_info.get("bookmarked_movies", [])
    return jsonify({
        "user":user_id,
        "recommendations": recommendations,
        "bookmarked_movies": bookmarked
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)