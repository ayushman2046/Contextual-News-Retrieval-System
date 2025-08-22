# app/main/routes/score_route.py
from flask import Blueprint, jsonify, request, current_app
from app.services.news_service import get_articles_by_score_service

score_router = Blueprint('score', __name__)

@score_router.route("/", methods=["GET"])
def get_articles_by_score():
    # 1. Get the 'threshold' query parameter from the URL
    try:
        # Flask uses request.args to get query parameters
        # .get() is safe and returns None if the parameter isn't present
        threshold = float(request.args.get('threshold', 0.7))
    except (ValueError, TypeError):
        return jsonify({"error": "Threshold must be a valid number."}), 400

    # 2. Get the database collection from the app's context
    collection = current_app.db.get_collection("news")

    # 3. Call the synchronous service function
    # Note: the get_articles_by_score_service must be synchronous
    articles = get_articles_by_score_service(collection, threshold)

    # 4. Return the articles as a JSON response
    return jsonify({"count": len(articles), "articles": articles})