# utils.py
import os
import pandas as pd
import networkx as nx
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")

def load_data(file_path):
    """Load CSV data."""
    return pd.read_csv(file_path)

def preprocess_data(data):
    """Preprocess the data: handle missing values and normalize."""
    data.fillna(method='ffill', inplace=True)
    return data

def create_knowledge_graph(data):
    """Create a knowledge graph based on relationships in the data."""
    G = nx.Graph()
    for _, row in data.iterrows():
        G.add_edge(row['Column1'], row['Column2'])  # Replace with your columns
    return G

def extract_embeddings(data, text_column):
    """Generate embeddings for the text data."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(data[text_column].tolist())
    return embeddings

def reduce_dimensions(embeddings):
    """Reduce dimensions of embeddings for visualization."""
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)
    tsne = TSNE(n_components=2, random_state=42)
    return tsne.fit_transform(embeddings_scaled)

def create_faiss_index(embeddings):
    """Create a FAISS index for efficient retrieval."""
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance
    index.add(np.array(embeddings, dtype=np.float32))  # Add embeddings to the index
    return index

def retrieve_similar_documents(index, query_embedding, k=5):
    """Retrieve similar documents based on a query embedding."""
    distances, indices = index.search(np.array([query_embedding], dtype=np.float32), k)
    return indices.flatten(), distances.flatten()

def generate_response(query, data):
    """Generate a response using the Groq API based on the data."""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Using the data: {data}, respond to the query: {query}"
            }
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content
