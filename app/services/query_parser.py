# app/services/query_parser.py
import json
from app.langchain.invoke_langchain import invoke_langchain
from app.langchain.news_query_prompt import news_query_prompt

def parse_user_query(user_query):
    input_vars = {"user_query": user_query}
    response = invoke_langchain(news_query_prompt, input_vars)

    try:
        parsed = json.loads(response.content)  # response.content contains LLM output
        return parsed
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {response.content}")
