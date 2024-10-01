# pipeline/rag_pipeline.py
from database.sumarizer import summarize_table
from rag_pipeline.generator import generate_query_from_llm
from rag_pipeline.retriever  import execute_llm_query

def run_rag_pipeline(table_name, user_request):
    """
    Runs the entire RAG pipeline: summarizes the table, generates the SQL query via LLM,
    and executes the generated query.
    
    Args:
        table_name (str): The name of the table to summarize and query.
        user_request (str): The user's natural language query request.
    
    Returns:
        dict: Contains the generated SQL query and the result of executing the query.
    """
    # Summarize the table
    table_summary = summarize_table(table_name)
    print("Table Summary:\n", table_summary)
    
    # Generate SQL query from LLM
    generated_query = generate_query_from_llm(table_summary, user_request)
    
    # Execute the SQL query
    query_result = execute_llm_query(generated_query)
    
    return {
        "generated_query": generated_query,
        "query_result": query_result
    }
