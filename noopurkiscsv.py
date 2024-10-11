import pandas as pd
from ragdash.chromadb import ChromaDB_VectorStore
from ragdash.groq import Groq
from groq import Groq as qqqq
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



client = qqqq(
    api_key="bvhgkml",
)

info=df_i.dtypes.astype(str)
# Create a prompt for the LLM to generate Python code for a DataFrame for a bar chart
csv_description_prompt = f"""
I have a CSV file with the following description:
{info}

Consider the CSV is read before in a DataFrame df_i. Can you generate the Python  code to extract and store dataframe df to make a bar chart? Assume the data is in a pandas dataframe called 'df_i'.Do not plot the graph, just extract the dataframe df and store it. Respond with only Python code. Do not answer with any explanations -- just the code.
"""

# Send the prompt to the Groq API
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system", 
            "content": "You are an python expert. Please help me generate a python code to extract and store dataframe df needed to make a bar chart.Your response should ONLY be based on the given context and follow the response guidelines and format instructions.",
        },
        {
            "role": "user",
            "content": csv_description_prompt,
        }
    ],
    model="llama3-8b-8192",
)

# Print the generated Python code for DataFrame extraction
extracted_df_code = chat_completion.choices[0].message.content
cleaned_response = extracted_df_code.replace("```", "").strip()
print("Extracted DataFrame Code:")
print(cleaned_response)
dfs = {
        0: df_i  # Use df read from the CSV
    }

dirname = os.path.dirname(__file__)

execution_context = {"pd": pd, "df_i": df_i, **dfs}

exec_context = execution_context.copy()
exec_context['dirname'] = dirname  # Include dirname in the context
exec_context.update(dfs)  # Include dfs in the context

exec(cleaned_response,exec_context)
df = exec_context.get('df', None)

print("df")
print(df)
print("df")
# Now use the extracted DataFrame code to get the chart generation code
# Prepare a new prompt to get the Plotly code


code = rd.generate_plotly_code(question="my_question", sql="sql", df=df,type_c="")

fig = rd.get_plotly_figure(plotly_code=code, df=df)
st.plotly_chart(fig, use_container_width=True)