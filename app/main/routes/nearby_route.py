# app/main/routes/nearby_route.py
from flask import Blueprint, jsonify, request, current_app
from app.services.news_service import get_nearby_articles_service

nearby_router = Blueprint('nearby_articles', __name__)

@nearby_router.route("/", methods=["GET"])
def get_nearby_articles():
    # Retrieve query parameters from request.args
    # .get() provides a default value (None) if the parameter is not in the URL, preventing errors
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
    except (ValueError, TypeError):
        return jsonify({"error": "Latitude and longitude must be valid numbers."}), 400

    # These parameters have default values, so they're less critical
    radius = float(request.args.get('radius', 10))
    limit = int(request.args.get('limit', 5))

    articles = get_nearby_articles_service(
        lat=lat,
        lon=lon,
        radius=radius
    )
    
    return jsonify({"count": len(articles), "articles": articles})