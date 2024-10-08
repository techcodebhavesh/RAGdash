from ragdash.chromadb import ChromaDB_VectorStore
from ragdash.groq import Groq
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MyRAGdash(ChromaDB_VectorStore, Groq):
    def __init__(self, config=None):
        # Initialize both base classes
        ChromaDB_VectorStore.__init__(self, config=config)
        Groq.__init__(self, config=config)

# Usage example
config = {
    'db_user': os.getenv('DB_USER'),
    'db_password': os.getenv('DB_PASSWORD'),
    'db_host': os.getenv('DB_HOST'),
    'db_name': os.getenv('DB_NAME')
}

print(config)

rd = MyRAGdash(config=config)

rd.connect_to_mysql(host=config['db_host'], dbname=config['db_name'], user=config['db_user'], password=config['db_password'], port=3306)

# rd.train(ddl="""CREATE TABLE Employees (
#     EmployeeID INT PRIMARY KEY,
#     FirstName VARCHAR(50),
#     LastName VARCHAR(50),
#     Email VARCHAR(100),
#     Phone VARCHAR(15),
#     HireDate DATE,
#     JobTitle VARCHAR(50),
#     Salary DECIMAL(10, 2),
#     Department VARCHAR(50)


# );""")

my_question = st.session_state.get("my_question", default=None)

if my_question is None:
    my_question = st.text_input(
        "Type your question here.",
        key="my_question",
    )
else:
    st.text(my_question)
    
    sql = rd.generate_sql(my_question)

    st.text(sql)

    df = rd.run_sql(sql)    
        
    st.dataframe(df, use_container_width=True)

    code = rd.generate_plotly_code(question=my_question, sql=sql, df=df)

    fig = rd.get_plotly_figure(plotly_code=code, df=df)

    st.plotly_chart(fig, use_container_width=True)
