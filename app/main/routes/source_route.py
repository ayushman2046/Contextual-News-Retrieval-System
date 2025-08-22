# app/main/routes/source_route.py
from flask import Blueprint, jsonify, request, current_app
from app.services.news_service import get_articles_by_source_service

source_router = Blueprint('source', __name__)

@source_router.route("/<source_name>", methods=["GET"])
def get_articles_by_source(source_name):
    # Get the optional 'limit' query parameter from the URL
    try:
        limit = int(request.args.get('limit', 5))
    except (ValueError, TypeError):
        return jsonify({"error": "Limit must be a valid number."}), 400

    # Get the database collection from the app's context
    collection = current_app.db.get_collection("news")

    # Call the synchronous service function
    articles = get_articles_by_source_service(collection, source_name)

    # Return the articles as a JSON response
    return jsonify({
        "count": min(len(articles), limit),
        "articles": articles[:limit]
    })