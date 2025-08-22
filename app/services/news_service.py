from flask import current_app
from app.utils.haversine import haversine_distance

def get_articles_by_category_service(category_name):
    collection = current_app.db.get_collection('news_articles')
    return collection.find(
        {"category": category_name}, {"_id": 0}
    ).sort(
        "publication_date", -1
    ).to_list(length=5)

def get_articles_by_source_service(source_name: str):
    collection = current_app.db.get_collection('news_articles')
    query = {"source_name": {"$regex": f"^{source_name}$", "$options": "i"}}
    return  collection.find(
        query, {"_id": 0}
    ).sort(
        "publication_date", -1
    ).to_list(length=5)

def get_articles_by_score_service(threshold: float):
    collection = current_app.db.get_collection('news_articles')
    return  collection.find(
        {"relevance_score": {"$gte": threshold}}, {"_id": 0}
    ).sort(
        "relevance_score", -1
    ).to_list(length=5)

def search_articles_service(query: str):
    # You can add more sophisticated text search here later
    collection = current_app.db.get_collection('news_articles')
    return  collection.find(
        {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
            ]
        },
        {"_id": 0},
    ).sort("relevance_score", -1).to_list(length=5)

def get_nearby_articles_service(lat: float, lon: float, radius: float):
    # This uses a generator to efficiently filter and rank articles
    # without loading the entire collection into memory.
    collection = current_app.db.get_collection('news_articles')
    articles_cursor = collection.find({}, {"_id": 0})
    nearby_articles = []

    for article in articles_cursor:
        if "latitude" in article and "longitude" in article:
            distance = haversine_distance(lat, lon, article["latitude"], article["longitude"])
            if distance <= radius:
                article["distance_km"] = round(distance, 2)
                nearby_articles.append(article)

    # Manual sort after filtering
    nearby_articles.sort(key=lambda x: x["distance_km"])

    return nearby_articles[:5]

def get_trending_articles_service(lat: float, lon: float, limit: int):

    collection = current_app.db.get_collection('news_articles')
    return  collection.find(
        {}, {"_id": 0}
    ).sort(
        [("publication_date", -1), ("relevance_score", -1)]
    ).to_list(length=limit)

# No need for haversine_distance, as MongoDB will handle the calculation
# from app.utils.haversine import haversine_distance


def get_contextual_articles_service(
    search_query=None,
    category=None,
    source=None,
    location=None,
    relevance_threshold=None,
    limit: int = 5,
    radius_km: float = 10.0  # default radius for nearby search
):
    collection = current_app.db.get_collection('news_articles')

    # 1. Build the basic match query (no $geoNear)
    match_query = {}
    if search_query:
        match_query["$or"] = [
            {"title": {"$regex": search_query, "$options": "i"}},
            {"description": {"$regex": search_query, "$options": "i"}}
        ]
    if category:
        match_query["category"] = category
    if source:
        match_query["source_name"] = {"$regex": f"^{source}$", "$options": "i"}
    if relevance_threshold:
        match_query["relevance_score"] = {"$gte": relevance_threshold}

    # Fetch all matching documents
    articles = list(collection.find(match_query, {"_id": 0}))

    # 2. If location is provided, filter manually using Haversine
    if location and "lat" in location and "lon" in location:
        lat, lon = location["lat"], location["lon"]
        nearby_articles = []
        for article in articles:
            if "latitude" in article and "longitude" in article:
                distance = haversine_distance(lat, lon, article["latitude"], article["longitude"])
                if distance <= radius_km:
                    article["distance_km"] = round(distance, 2)
                    nearby_articles.append(article)
        articles = nearby_articles

        # Sort by distance for nearby search
        articles.sort(key=lambda x: x["distance_km"])
    else:
        # Sort by relevance_score if available, otherwise by publication_date
        articles.sort(
            key=lambda x: (
                x.get("relevance_score", 0),
                x.get("publication_date", "")
            ),
            reverse=True
        )

    # Limit results
    return articles[:limit]