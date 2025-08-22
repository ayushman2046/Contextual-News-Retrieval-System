# app/main/routes/category_route.py
from flask import Blueprint, jsonify, current_app
from app.services.news_service import get_articles_by_category_service

category_router = Blueprint("category_related_articles", __name__)

@category_router.route("/<category>")
def get_articles_by_category(category):
    collection = current_app.db.get_collection('news_article')
    articles = get_articles_by_category_service(collection, category)
    
    return jsonify({"count": len(articles), "articles": articles})