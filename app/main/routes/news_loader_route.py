# app/main/routes/news_loader_route.py
from flask import Blueprint, request, jsonify, abort, current_app
from app.utils.news_loader import load_news_data
import os

news_loader_router = Blueprint('news_loader', __name__)

@news_loader_router.route("/load-news", methods=["POST"])
def load_news():
    """
    Load news data from a JSON file into MongoDB.
    Default file path: data/news.json
    """
    try:
        file_path = "news_data.json"
        
        # Access the database from the current app's context
        db = current_app.db.db
        
        # The service function must be synchronous
        load_news_data(db, file_path)
        
        return jsonify({"message": f"News loaded successfully from {file_path}"})
    
    except FileNotFoundError:
        # Flask uses abort() for HTTP errors
        abort(404, description=f"File not found: {file_path}")
        
    except Exception as e:
        abort(500, description=str(e))