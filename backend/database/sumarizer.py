# db/summarizer.py
from database.queries import execute_custom_query

def summarize_table(table_name):
    """
    Summarizes the table structure and provides sample rows for context.
    
    Args:
        table_name (str): The name of the table to summarize.
    
    Returns:
        str: A formatted summary of the table including columns and sample data.
    """
    # Fetch column information
    column_query = f"DESCRIBE {table_name};"

    column_info = execute_custom_query(column_query)
    print("qwerwetyrutioyupi")
    print(column_info)

    # Fetch sample data
    sample_data_query = f"SELECT * FROM {table_name} LIMIT 5;"
    sample_data = execute_custom_query(sample_data_query)
    print("qwerwetyrutio1111111111111111111yupi")
    print(sample_data)

    # Format the table summary
    summary = f"Table: {table_name}\nColumns:\n"
    for col in column_info:
        summary += f"- {col['Field']} ({col['Type']})\n"

    return summary
