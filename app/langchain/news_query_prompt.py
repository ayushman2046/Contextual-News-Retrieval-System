# app/langchain/prompts/news_query_prompt.py
from app.langchain.invoke_langchain import create_prompt_template

SYS_PROMPT = """
    You are a news assistant AI. Your task is to extract structured information from a user's query.
    Return the result as valid JSON with the following structure:

    {{
        "entities": ["<person/organization/location/event>", ...],
        "intent": "<category|source|search|nearby|score>",
        "location": {{"lat": <float>, "lon": <float>}}  - null if not applicable
    }}

    Rules:
    - Extract all important named entities.
    - intent must be exactly one of: category, source, search, nearby, score.
    - If the query mentions a place, try to resolve it to lat/lon (use null if not available).
    - Return JSON only, no extra text or explanation.
"""

USER_TEMPLATE = "User Query: {user_query}"

news_query_prompt = create_prompt_template(USER_TEMPLATE, SYS_PROMPT)
