import google.generativeai as genai
from utils.config import get_gemini_api_key, get_gemini_model
import re
import json
from prompts.prompts import prompts
genai.configure(api_key=get_gemini_api_key())
model = genai.GenerativeModel(get_gemini_model())  # or other variant

def format_prompt(query: str, context_chunks: list[str]) -> str:
    context_str = str(context_chunks)
    prompt = f"""
        You are an expert soil agronomist. Use the following data on soil test results for a particular period of time to answer the user query.

        Soil test results:
        {context_str}

        User Query:
        {query}

        Respond clearly. Be as detailed as you can in your answer.
        Do not include any fluff words like references to the question in your response. Just get right to the analysis.
        The response should be in the format {{ "analysis": your_analysis_here}}
    """
    return prompt

def ask_gemini(query: str, context_chunks: list[str]) -> str:
    prompt = format_prompt(query, context_chunks)
    response = model.generate_content(prompt)
    json_pattern = '\{.*\}'
    json_match = re.findall(json_pattern, response.text, flags=re.DOTALL)

    return json.loads(json_match[0])


def executive_summary(results: list, guides: list):
    prompt = prompts['executive_summary_prompt'].format(str(results), str(guides))
    response = model.generate_content(prompt)
    print(response)
    return response.text


def recommendations_summary(results: list, guides: list, recommendations: list):
    prompt = prompts['recommendations_summary_prompt'].format(str(results), str(guides), str(recommendations))
    response = model.generate_content(prompt)
    print(response)
    return response.text

def plot_summary(chemical: str, results: list, guides: list):
    prompt = prompts['plot_summary_prompt'].format(str(chemical), str(results), str(guides))
    response = model.generate_content(prompt)
    print(response)
    return response.text
