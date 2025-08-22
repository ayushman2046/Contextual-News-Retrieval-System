import json
from app.main.database import Database

def load_news_data(db: Database, file_path: str):

    print(db)
    collection = db.get_collection("news_articles")
    
    with open(file_path, "r", encoding="utf-8") as f:
        news_list = json.load(f)
    
    inserted_count = 0
    for article in news_list:
        # Check if the article with the same id already exists
        if not collection.find_one({"id": article["id"]}):
            collection.insert_one(article) 
            inserted_count += 1
    
    print(f"Inserted {inserted_count} new articles into MongoDB.")
