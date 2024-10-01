# db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    
    Returns:
        connection (sqlalchemy.engine.base.Connection): A connection object to interact with the database.
    """
    try:
        # Replace the following values with your actual MySQL credentials
        username = 'root'
        password = 'Password123'
        host = 'localhost'  # or your database host IP
        port = '3306'  # default MySQL port
        database_name = 'serverwala'
        
        # Create an engine and connection string for MySQL
        engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}')
        
        # Connect to the database
        connection = engine.connect()
        print("Database connection established successfully.")
        return connection
    
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        return None
