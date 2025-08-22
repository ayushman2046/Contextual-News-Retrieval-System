# app/main/routes/search_router.py
from flask import Blueprint, jsonify, request, current_app
from app.services.news_service import search_articles_service

search_router = Blueprint('search_articles', __name__)

@search_router.route("/", methods=["GET"])
def search_articles():
    # Get the 'query' and 'limit' parameters from the URL
    query_string = request.args.get('query')
    limit = int(request.args.get('limit', 5))

    # Ensure a query string was provided
    if not query_string:
        return jsonify({"error": "A search query is required."}), 400

    # Get the database collection from the app's context
    collection = current_app.db.get_collection("news")

    # Call the synchronous service function
    articles = search_articles_service(collection, query_string)

    # Return the results as a JSON response
    return jsonify({"count": len(articles), "articles": articles})