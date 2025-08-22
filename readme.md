# NewsHub - Contextual News Data Retrieval System

A Flask-based backend system that provides intelligent news article retrieval using LLM-powered query processing and MongoDB storage.

## Features

- **Smart Query Processing**: LLM-based entity extraction and intent recognition
- **Location-Based Search**: Find news articles near specific locations
- **Multiple Search Options**: Category, source, score-based, and trending news
- **Relevance Scoring**: AI-powered article ranking based on query context

## Tech Stack

- **Backend**: Flask
- **Database**: MongoDB
- **LLM Integration**: OpenAI API
- **Language**: Python 3.10+

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone {github_link}
   cd newshub
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

2. **Configure MongoDB**
   - Update MongoDB URI in `app/main/config.py`

3. **Load Data and Run**
   ```bash
   python utils/news_loader.py
   python run.py
   ```

Server starts at `http://localhost:5000`

## API Endpoints

**Base URL**: `http://localhost:5000/api/v1`

| Endpoint | Method | Description | Example |
|----------|---------|-------------|---------|
| `/query` | POST | Smart query processing | `{"query": "sports news in Delhi"}` |
| `/category` | GET | Category-based news | `/category?name=Technology` |
| `/nearby` | GET | Location-based news | `/nearby?lat=28.6&lon=77.2&radius=10` |
| `/trending` | GET | Trending articles | `/trending?limit=5` |
| `/search` | GET | Text search | `/search?query=Elon+Musk` |
| `/source` | GET | Source-based news | `/source?name=BBC` |
| `/score` | GET | Score-based filtering | `/score?threshold=0.7` |

## Example Response

```json
{
  "articles": [
    {
      "title": "Article Title",
      "description": "Article summary...",
      "url": "https://example.com/news",
      "publication_date": "2025-03-22T17:33:09",
      "source_name": "News Source",
      "category": ["Technology"],
      "relevance_score": 0.95,
      "latitude": 28.6139,
      "longitude": 77.2090
    }
  ],
  "count": 1
}
```
