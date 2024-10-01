# db/queries.py

from database.db_connection import get_db_connection

def execute_custom_query(query):
    """
    Executes a custom SQL query and retrieves the data.
    
    Args:
        query (str): The SQL query to execute.
        
    Returns:
        list: A list of dictionaries representing the query result.
    """
    connection = get_db_connection()
    if connection is None:
        return []

    try:
        print(f"Executing Query: {query}")

        # Execute the query and fetch all results
        result = connection.execute(query).fetchall()

        # Format the result as a list of dictionaries
        data = [dict(row) for row in result]
        
        return data

    except Exception as e:
        print(f"Error executing custom query: {e}")
        return []
    
    finally:
        connection.close()
