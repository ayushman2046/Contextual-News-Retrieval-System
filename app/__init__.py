# flask_app.py
from flask import Flask, jsonify, Blueprint, request
from app.main import config
from app.main.database import Database
from app.main.routes.category_route import category_router
from app.main.routes.source_route import source_router
from app.main.routes.score_route import score_router
from app.main.routes.nearby_route import nearby_router
from app.main.routes.search_route import search_router
from app.main.routes.trending_route import trending_router
from app.main.routes.query_route import query_router
from app.main.routes.news_loader_route import news_loader_router

def create_app(config_name: str = "dev"):

    app_config = config.config_by_name[config_name]()

    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(app_config)
    
    # Attach DB to app
    app.db = Database(app)

    # Create a central Blueprint
    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

    api_blueprint.register_blueprint(category_router, url_prefix="/category")
    api_blueprint.register_blueprint(source_router, url_prefix="/source")
    api_blueprint.register_blueprint(score_router, url_prefix="/score")
    api_blueprint.register_blueprint(nearby_router, url_prefix="/nearby")
    api_blueprint.register_blueprint(search_router, url_prefix="/search")
    api_blueprint.register_blueprint(trending_router, url_prefix="/trending")
    api_blueprint.register_blueprint(query_router, url_prefix="/query")
    api_blueprint.register_blueprint(news_loader_router, url_prefix="/news-loader")

    app.register_blueprint(api_blueprint)

    return app