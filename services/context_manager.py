from db.connection import get_connection
import google.generativeai as genai
from utils.config import get_gemini_api_key, get_gemini_model
from db.models import SAMPLERESULTS_TABLE
import re
import json

genai.configure(api_key=get_gemini_api_key())
model = genai.GenerativeModel(get_gemini_model())

def format_prompt(query: str) -> str:
    prompt = f"""
        You are an expert SQL programmer. You have created a database that contains a table called {SAMPLERESULTS_TABLE['name']}.
        This table contains the following fields: {SAMPLERESULTS_TABLE['columns']}

        I want you to write an sql query to retrieve data that could be used as evidence to answer the following question
        {query}

        Your response should be in the format: {{ "sql_query": generated_sql_query}}
    """
    return prompt

def ask_gemini(query: str) -> str:
    prompt = format_prompt(query)
    response = model.generate_content(prompt)
    print(response.text)
    return response.text


def search_context(query: str) -> list[str]:
    content = ask_gemini(query=query)
    json_pattern = '\{.*\}'
    json_match = re.findall(json_pattern, content, flags=re.DOTALL)

    return json.loads(json_match[0])
    
