# app/main/routes/query_route.py
from flask import Blueprint, current_app, request, jsonify, abort
from app.services.query_parser import parse_user_query
from app.services.news_service import get_contextual_articles_service
from app.main.database import Database  # Assuming this is your synchronous DB class

query_router = Blueprint('query', __name__)

@query_router.route("/", methods=["POST"])
def analyze_query():
    # 1. Get the request body data (equivalent to FastAPI's Pydantic model)
    try:
        query_data = request.get_json()
        query_text = query_data.get("query")
        if not query_text:
            abort(400, description="Query text is required in the request body.")
    except Exception as e:
        abort(400, description="Invalid JSON format in request body.")

    collection = current_app.db.get_collection("news")
    
    # 3. Parse the user query (no change needed here as it's a synchronous function)
    parsed = parse_user_query(query_text)

    # 4. Extract and validate contextual information
    entities = parsed.get("entities", [])
    search_term = entities[0] if entities else None
    category = parsed.get("category")
    source = parsed.get("source")
    location = parsed.get("location")
    relevance_threshold = parsed.get("relevance_threshold")

    if not any([search_term, category, source, location, relevance_threshold]):
        abort(400, description="Could not extract meaningful context from the query.")

    # 5. Call the synchronous service function
    articles = get_contextual_articles_service(
        search_query=search_term,
        category=category,
        source=source,
        location=location,
        relevance_threshold=relevance_threshold,
        limit=5
    )
    
    # 6. Return the JSON response
    return jsonify({"count": len(articles), "articles": articles})