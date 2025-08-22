# app/main/routes/trending_route.py
from flask import Blueprint, jsonify, request, current_app
from app.services.news_service import get_trending_articles_service

trending_router = Blueprint('trending', __name__)

@trending_router.route("/", methods=["GET"])
def get_trending_articles():
    # 1. Get query parameters from the URL
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
    except (ValueError, TypeError):
        return jsonify({"error": "Latitude and longitude must be valid numbers."}), 400

    limit = int(request.args.get('limit', 5))

    # 2. Get the database collection from the app's context
    collection = current_app.db.get_collection("news")

    # 3. Call the synchronous service function
    articles = get_trending_articles_service(
        collection=collection,
        lat=lat,
        lon=lon,
        limit=limit
    )

    # 4. Return the articles as a JSON response
    return jsonify({"count": len(articles), "articles": articles})