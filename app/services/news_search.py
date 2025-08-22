# app/services/news_search.py
from app.utils.haversine import haversine_distance

def build_mongo_filter(parsed_query):
    filters = {}

    if parsed_query.get("category"):
        filters["category"] = parsed_query["category"]

    if parsed_query.get("source"):
        filters["source_name"] = {"$regex": parsed_query["source"], "$options": "i"}

    if parsed_query.get("min_relevance_score"):
        filters["relevance_score"] = {"$gte": parsed_query["min_relevance_score"]}

    if parsed_query.get("query"):
        filters["$or"] = [
            {"title": {"$regex": parsed_query["query"], "$options": "i"}},
            {"description": {"$regex": parsed_query["query"], "$options": "i"}},
        ]

    return filters


def search_news(db, parsed_query):
    collection = db.get_collection("news")
    filters = build_mongo_filter(parsed_query)

    articles = list(collection.find(filters, {"_id": 0}))

    # optional: filter by location radius
    if parsed_query.get("latitude") and parsed_query.get("longitude") and parsed_query.get("radius_km"):
        nearby_articles = []
        for article in articles:
            if "latitude" in article and "longitude" in article:
                distance = haversine_distance(
                    parsed_query["latitude"], parsed_query["longitude"],
                    article["latitude"], article["longitude"]
                )
                if distance <= parsed_query["radius_km"]:
                    article["distance_km"] = round(distance, 2)
                    nearby_articles.append(article)
        articles = nearby_articles

    # sort relevance first, then publication_date
    articles.sort(key=lambda x: (x.get("relevance_score", 0), x.get("publication_date", "")), reverse=True)

    return articles[:10]
