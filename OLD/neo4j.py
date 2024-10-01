import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal, RDF
import os
from groq import Groq

def csv_to_rdf(csv_file_path):
    # Load CSV data
    patients = pd.read_csv(csv_file_path)

    # Create a new RDF Graph
    g = Graph()

    # Define Namespace URIs
    PPL = Namespace('http://example.org/people/')
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    SCHEMA = Namespace("http://schema.org/")

    # Bind namespaces
    g.bind("foaf", FOAF)
    g.bind("schema", SCHEMA)
    g.bind("ppl", PPL)

    for col, row_val in patients.iterrows():
        pt_id = URIRef(f"http://example.org/ID/{row_val['Id']}")

        # Add nodes to RDF graph
        g.add((pt_id, RDF.type, FOAF.Identifier))
        g.add((Literal(row_val['BIRTHDATE']), RDF.type, FOAF.Date))
        g.add((Literal(row_val['DEATHDATE']), RDF.type, FOAF.Date))
        g.add((Literal(row_val['SSN']), RDF.type, PPL.SSN))
        g.add((Literal(row_val['FIRST']), RDF.type, SCHEMA.FirstName))
        g.add((Literal(row_val['LAST']), RDF.type, SCHEMA.LastName))
        g.add((Literal(row_val['GENDER']), RDF.type, FOAF.Gender))

        # Add relationships
        g.add((Literal(row_val['FIRST']), SCHEMA['FIRST_NAME_OF'], pt_id))
        g.add((Literal(row_val['LAST']), SCHEMA['LAST_NAME_OF'], pt_id))
        g.add((Literal(row_val['BIRTHDATE']), SCHEMA['BIRTHDAY_OF'], pt_id))
        g.add((Literal(row_val['DEATHDATE']), SCHEMA['DEATHDATE_OF'], pt_id))
        g.add((Literal(row_val['SSN']), PPL['SSN_OF'], pt_id))
        g.add((Literal(row_val['GENDER']), FOAF['GENDER_OF'], pt_id))

    # Serialize the RDF graph to a file
    rdf_file_path = 'patient_data.rdf'
    g.serialize(destination=rdf_file_path, format='turtle')

    return rdf_file_path

# Example usage
rdf_file = csv_to_rdf('patient_data.csv')

from rdflib import Graph
from rdflib_neoj import Neo4jStore, Neo4jStoreConfig, HANDLE_VOCAB_URI_STRATEGY

def import_rdf_to_neo4j(rdf_file_path, neo4j_uri, username, password):
    # Create the Aura DB authentication variable list
    auth_data = {
        'uri': neo4j_uri,
        'database': "neo4j",
        'user': username,
        'pwd': password
    }

    # Create configuration prefixes to the namespaces used
    prefixes = {
        'ppl': Namespace('http://example.org/people/'),
        'foaf': Namespace("http://xmlns.com/foaf/0.1/"),
        'schema': Namespace("http://schema.org/")
    }

    # Define your custom mappings & store config
    config = Neo4jStoreConfig(auth_data=auth_data,
                              custom_prefixes=prefixes,
                              handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
                              batching=True)

    # Create the RDF Graph, parse & ingest the data to Neo4j, and close the store
    neo4j_graph = Graph(store=Neo4jStore(config=config))
    neo4j_graph.parse(rdf_file_path, format="ttl")
    neo4j_graph.close(True)

# Example usage
import_rdf_to_neo4j(rdf_file, 'bolt://127.0.0.1:7687', 'neo4j', 'nSa6IaxH6GgRg2sFmvUd8KPAoahDkHa0mX5Qpg1Htnc')

from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import Neo4jVector

def create_vector_embeddings(neo4j_uri, username, password, index_name):
    # Create Vector Embedding Index
    Neo4jVector.from_existing_graph(
        HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5"),
        url=neo4j_uri,
        username=username,
        password=password,
        database='neo4j',
        index_name=index_name,
        node_label="resource",
        text_node_properties=['text'],
        embedding_node_property='embedding',
    )

# Example usage
create_vector_embeddings('bolt+s://79c26ce3.databases.neo4j.io:7687', 'neo4j', 'nSa6IaxH6GgRg2sFmvUd8KPAoahDkHa0mX5Qpg1Htnc', 'Instance01')

def generate_dashboard(prompt):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

# Example prompt
prompt = '''
System: The context below contains entries about the patient's healthcare data, including healthcare expenses and coverage. 
You are allowed to share information based on the context provided.
Please limit your answer to the information provided in the context. 
If you don't know the answer, just say that you don't know.
'''

# Generate a dashboard response
dashboard_response = generate_dashboard(prompt)
print(dashboard_response)
