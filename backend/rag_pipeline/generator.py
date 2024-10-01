# llm/query_generator.py
import os
from groq import Groq

client = Groq(api_key="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")

def generate_query_from_llm(table_summary, user_prompt, model="llama3-8b-8192"):
    """
    Uses Groq LLM to generate SQL query based on table summary and user prompt.
    
    Args:
        table_summary (str): Summary of the table structure.
        user_prompt (str): The user's natural language request.
        model (str): The LLM model to use for query generation.
    
    Returns:
        str: The generated SQL query.
    """
    prompt = f"Table Summary:\n{table_summary}\n\nUser Request:\n{user_prompt}\nPlease generate an SQL query and dont give anything else."
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model
    )
    
    return response.choices[0].message.content
