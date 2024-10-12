import pandas as pd
from ragdash.chromadb import ChromaDB_VectorStore
from ragdash.groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os


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

# Read CSV file
csv_path = 'F:/Mayur/vit/innov8ors/ollama/AutoDash/Sample_CSVs/dairy_dataset.csv'  # Path to your CSV file
df_i = pd.read_csv(csv_path)

python_code = rd.generate_python(df=df_i, type_c="pie")

df = rd.extract_dataframe(python_code,df=df_i)

dirname = os.path.dirname(__file__)


print("df")
print(df)
print("df")
# Now use the extracted DataFrame code to get the chart generation code
# Prepare a new prompt to get the Plotly code


code = rd.generate_plotly_code(question=None,df_metadata= df.columns,
                               sql=None, df=df,type_c="pie")

fig = rd.get_plotly_figure(plotly_code=code, df=df)
st.plotly_chart(fig, use_container_width=True)