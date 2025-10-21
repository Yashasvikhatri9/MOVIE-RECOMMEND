import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request

app = Flask(__name__)
vector = pickle.load(open("/models/vector.pkl", "rb"))
svd = pickle.load(open("/models/svd_model.pkl", "rb"))
vector_reduced = pickle.load(open("/models/vector_reduced.pkl", "rb"))
movie = pd.read_csv("/data/processed/movies_clean.csv")

# Build query text for recommendation
def build_query(user_info: dict):
    # Get user movie IDs, default to empty lists
    watched = user_info.get("watched_ids", [])
    searched = user_info.get("searched_ids", [])
    bookmarked = user_info.get("bookmarked_movies", [])

    all_movies = list(set(watched + searched + bookmarked))

    if all_movies:
        # If there are any movies from the user, combine their text
        selected = movie[movie["id"].isin(all_movies)]
        combined_text = " ".join(selected["combined_text"].dropna().tolist())
        if combined_text.strip():
            return combined_text

    # If no movies provided or combined_text is empty, fallback to genres/language
    genres = user_info.get("genres", "")
    language = user_info.get("language", "")
    fallback_query = (genres + " " + language).strip()
    if fallback_query:
        return fallback_query

    # If everything is missing, return a generic empty string (or a default genre query)
    return "comedy action"  # optional default query


# Recommendation function
def recommend_movies(query: str, top_n: int = 10):
    if not query or not query.strip():
        return []
    movies_filtered = movie[(movie["vote_average"] > 2) & (movie["vote_count"] > 40)].reset_index(drop=True)
    query_vec = vector.transform([query.lower()])
    query_vec_reduced = svd.transform(query_vec)
    similarity = cosine_similarity(query_vec_reduced, vector_reduced[movies_filtered.index.to_numpy()]).flatten()
    top_indices = similarity.argsort()[::-1][:top_n]
    recommended = movies_filtered.iloc[top_indices][['id','imdb_id','title','vote_average','vote_count','genres','backdrop_path','poster_path','trailer_link']].copy()
    recommended['similarity'] = similarity[top_indices]
    return recommended.to_dict(orient="records")

# Flask API endpoint
@app.route("/recommend_movies", methods=["POST"])
def recommend_movies_api():
    user_info = request.json or {}

    query_text = build_query(user_info)
    if not query_text:
        return jsonify({"error": "Unable to construct query text."}), 400

    recommendations = recommend_movies(query_text)

    bookmarked = user_info.get("bookmarked_movies", [])
    
    return jsonify({
        "recommendations": recommendations,
        "bookmarked_movies": bookmarked
    })