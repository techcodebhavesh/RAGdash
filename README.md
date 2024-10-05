# RAGdash

**RAGdash** is a Python-based RAG (Retrieval-Augmented Generation) system designed to seamlessly generate SQL queries and retrieve data through natural language prompts. By combining the power of natural language processing and data querying, RAGdash simplifies database interactions, making it easier for users to extract insights using conversational queries.

## Description

RAGdash allows users to interact with their MySQL databases using natural language prompts. The project leverages Retrieval-Augmented Generation (RAG) to map these prompts to SQL queries, offering a more intuitive interface for non-technical users to extract, analyze, and manipulate data from their databases. Users can ask questions about their data, and RAGdash will automatically generate and execute the SQL queries, returning relevant results.

## Features
- Natural language-based SQL query generation
- Seamless interaction with MySQL databases (local or remote)
- Streamlit-based web interface for ease of use
- Easily configurable environment variables for connecting to databases

## Getting Started

### Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **MySQL** (local or remote)
  
Make sure your system has **Python** and **pip** installed. You can verify the installation by running:

```bash
python --version
pip --version
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RAGdash.git
   cd RAGdash
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install MySQL locally, or ensure you have access to a remote MySQL instance. If using a local MySQL instance, you can install it on Linux with:
   ```bash
   sudo apt install mysql-server
   ```

4. Set up a MySQL database and create a table for the program to interact with.

### Configuration

Create a `.env` file in the root directory with the following content:
   ```bash
   GROQ_API_KEY=<groq_api_key>
   DB_HOST="localhost"
   DB_USER="root"
   DB_PASSWORD="Password"
   DB_NAME="sakila"
   ```

   Replace `DB_USER`, `DB_PASSWORD`, and `DB_NAME` with your actual MySQL credentials and database details.

### Usage

Once the setup is complete, you can launch the RAGdash application by running the following command:

```bash
streamlit run app.py
```

This will launch the web interface for interacting with the database using natural language prompts.

### Example Workflow

1. Set up a MySQL database and table with data you want to query.
2. Launch the app and enter a natural language query (e.g., "Show me all the sales data from last month").
3. RAGdash will convert the query to SQL, run it against the database, and display the results on the Streamlit dashboard.

## Contribution

Feel free to contribute to RAGdash by submitting pull requests. Any improvements in code structure, features, or documentation are welcome.

## License

This project is licensed under the MIT License.
