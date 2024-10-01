# query_builder.py
def build_select_query(table_name, columns, conditions=None):
    """
    Dynamically builds a SELECT SQL query based on the provided table name, columns, and conditions.
    
    Args:
        table_name (str): The name of the table to query.
        columns (list): A list of columns to retrieve.
        conditions (dict, optional): A dictionary of conditions for filtering the data (e.g., {'column': 'value'}).
    
    Returns:
        str: The dynamically built SQL SELECT query.
    """
    # Basic SELECT statement
    query = f"SELECT {', '.join(columns)} FROM {table_name}"

    # If there are conditions, add a WHERE clause
    if conditions:
        condition_clauses = [f"{column} = '{value}'" for column, value in conditions.items()]
        query += f" WHERE {' AND '.join(condition_clauses)}"
    
    return query
