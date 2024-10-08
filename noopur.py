from ragdash.chromadb import ChromaDB_VectorStore
from ragdash.groq import Groq
from ragdash.exceptions import ValidationError  
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

try:
    rd.connect_to_mysql(host=config['db_host'], dbname=config['db_name'], user=config['db_user'], password=config['db_password'], port=3306)
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()


# data ka extarction
my_questions = {
    "bar": "extract the data appropriate for bar chart",
    "pie": "extract the data appropriate for pie chart",
    "line": "extract the data appropriate for line chart",
    "scatter": "extract the data appropriate for scatter chart"
}


results = {}

# Generate SQL queries and DataFrames for each chart type with error handling
for chart_type, question in my_questions.items():
    try:
        sql = rd.generate_sql(question)
        df = rd.run_sql(sql)

        # Store DataFrame and SQL in results
        results[chart_type] = {
            "df": df,
            "sql": sql
        }

        # Display DataFrame
        st.dataframe(df, use_container_width=True)

    except ValidationError as e:
        st.error(f"Validation error for {chart_type} chart: {e}")
        results[chart_type] = None  # Store None to indicate failure

    except Exception as e:
        st.error(f"Error processing {chart_type} chart: {e}")
        results[chart_type] = None  # Store None to indicate failure

# Generate Plotly code and figures with error handling
for chart_type in results:
    if results[chart_type] is not None:
        try:
            df = results[chart_type]["df"]
            sql = results[chart_type]["sql"]
            code = rd.generate_plotly_code(question=my_questions[chart_type], sql=sql, df=df, type_c=chart_type)
            fig = rd.get_plotly_figure(plotly_code=code, df=df)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error generating {chart_type} plot: {e}")
