import pymysql
import os
from groq import Groq

def connect_db():
    print("Connecting to the database...")
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Password@123',
        db='autodashtestrag',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connected to the database.")
    return connection

# Function to query the database based on user question
def query_db(question):
    try:
        print(f"Executing query for the question: {question}")
        conn = connect_db()
        cursor = conn.cursor()
        
        # SQL query to search the database (customize based on your table and question logic)
        sql_query = """
        SELECT * 
        FROM Orders 
        WHERE MATCH(customer_name, product_name, order_status) 
        AGAINST (%s IN NATURAL LANGUAGE MODE) 
        LIMIT 5;
        """
        print("SQL Query: ", sql_query)
        
        cursor.execute(sql_query, (question,))
        results = cursor.fetchall()
        
        print(f"Query executed successfully, number of records found: {len(results)}")
        conn.close()
        return results
    
    except Exception as e:
        print(f"Error during database query: {str(e)}")
        return None

# Function to generate response using Groq API
def generate_response(sql_data, question):
    print("Generating response based on SQL data...")
    
    if not sql_data:
        print("No data found to generate a response.")
        return "No relevant data found for your query."

    # Convert SQL data into text that can be used by Groq's LLM
    context = "Here is the data related to your question:\n"
    for row in sql_data:
        context += f"Order ID: {row['order_id']}, Customer: {row['customer_name']}, Product: {row['product_name']}, Status: {row['order_status']}\n"

    # Initialize Groq client with API key from environment variables
    print("Initializing Groq client...")
    client = Groq(api_key="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")

    # Use Groq API to generate a response
    print("Calling Groq API for text generation...")
    print("Context for response generation:")
    print(context)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": context
            },
            {
                "role": "user",
                "content": question
            }
        ],
        model="llama3-8b-8192",  # You can replace with your desired model
    )
    
    generated_text = chat_completion.choices[0].message.content
    print("Response generated successfully.")
    
    return generated_text

# Main pipeline for RAG
def rag_pipeline(question):
    print(f"Starting the RAG pipeline for the question: {question}")
    
    # Step 1: Retrieve relevant data from SQL database
    sql_data = query_db(question)
    
    if not sql_data:
        return "No relevant data found for your query."
    
    # Step 2: Generate response using Groq API based on retrieved data
    response = generate_response(sql_data, question)
    
    print("RAG pipeline completed.")
    return response

# Example question to test the pipeline
if __name__ == "__main__":
    user_question = input("Enter your question: ")
    response = rag_pipeline(user_question)
    print("Final Response:")
    print(response)
