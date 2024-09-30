import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from groq import Groq
import dash
from dash import dcc, html
import plotly.express as px

# Initialize the Groq client
client = Groq(api_key="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")

def load_data(file_path):
    """Load the CSV data."""
    print(f"Loading data from {file_path}...")
    data = pd.read_csv(file_path)
    print("Data loaded successfully. First few rows:")
    print(data.head())
    return data

def preprocess_data(data):
    """Preprocess the data: handle missing values and normalize."""
    print("Preprocessing data: handling missing values...")
    data.ffill(inplace=True)  # Forward fill missing values
    print("Data after preprocessing (first few rows):")
    print(data.head())
    return data

def analyze_data_with_llm(data):
    """Use LLM to analyze data and determine potential relationships."""
    print("Analyzing data using LLM...")
    data_summary = data.describe(include='all').to_string()
    
    # Generate a prompt for LLM to find relationships
    prompt = f"Given the following data summary:\n{data_summary}\n\n" \
             "Identify potential relationships between columns and suggest pairs to create a knowledge graph."
    
    print("Generated prompt for LLM:")
    print(prompt)
    
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192"
    )
    
    llm_response = response.choices[0].message.content
    print("LLM response received:")
    print(llm_response)
    
    return llm_response

def create_knowledge_graph(data, relationships):
    """Create a knowledge graph based on relationships in the data."""
    print("Creating a knowledge graph based on the LLM's relationships...")
    G = nx.Graph()
    
    for relationship in relationships.split('\n'):
        if relationship.strip():  # Ignore empty lines
            parts = relationship.split(',')
            if len(parts) == 2:  # Ensure we have exactly two parts
                source, target = parts
                G.add_edge(source.strip(), target.strip())
            else:
                print(f"Warning: Skipped invalid relationship format: {relationship}")
    
    print(f"Knowledge graph created with {len(G.nodes)} nodes and {len(G.edges)} edges.")
    return G

def visualize_graph(G):
    """Visualize the knowledge graph."""
    print("Visualizing the knowledge graph...")
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_color='lightblue', font_size=10, node_size=2000, font_color='black')
    plt.title("Knowledge Graph")
    plt.show()

def create_charts(data):
    """Create various charts for the dashboard."""
    print("Creating charts for the dashboard...")
    bar_chart = px.bar(data, x=data.columns[0], y=data.columns[1], title="Bar Chart Example")
    scatter_chart = px.scatter(data, x=data.columns[0], y=data.columns[1], title="Scatter Plot Example")
    line_chart = px.line(data, x=data.columns[0], y=data.columns[1], title="Line Chart Example")

    print("Charts created successfully.")
    return bar_chart, scatter_chart, line_chart

# Initialize Dash app
app = dash.Dash(__name__)

# Load and preprocess data
data = load_data('data.csv')
data = preprocess_data(data)

# Analyze data with LLM to determine relationships
relationships = analyze_data_with_llm(data)

# Create knowledge graph
G = create_knowledge_graph(data, relationships)

# Create charts
bar_chart, scatter_chart, line_chart = create_charts(data)

# Dashboard layout
app.layout = html.Div([
    html.H1("Data Analysis Dashboard"),
    dcc.Graph(figure=bar_chart),
    dcc.Graph(figure=scatter_chart),
    dcc.Graph(figure=line_chart),
    html.H2("Knowledge Graph"),
    dcc.Graph(figure=px.line(title="Graph Placeholder"))  # Placeholder for the knowledge graph
])

# Run the server
if __name__ == "__main__":
    print("Starting the Dash server...")
    app.run_server()
