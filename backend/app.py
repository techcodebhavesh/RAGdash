# app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from rag_pipeline.pipeline import run_rag_pipeline

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Business BI Agent"),
    dcc.Input(id='user-request', type='text', placeholder='Enter your request...'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='generated-query-output', style={'whiteSpace': 'pre-line'}),
    dcc.Graph(id='result-graph')
])

@app.callback(
    Output('generated-query-output', 'children'),
    Output('result-graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    Input('user-request', 'value')
)
def update_graph(n_clicks, user_request):
    if n_clicks > 0 and user_request:
        table_name = "server"  # Assuming you want to query the 'server' table
        result = run_rag_pipeline(table_name, user_request)

        generated_query = result["generated_query"]
        query_result = result["query_result"]

        # If the query result is empty, handle it gracefully
        if not query_result:
            return f"No data returned for the query: {generated_query}", {}

        # Create a DataFrame for plotting
        import pandas as pd
        df = pd.DataFrame(query_result)

        # Assuming the first column is the x-axis and the second is the y-axis for simplicity
        if len(df.columns) >= 2:
            x_column = df.columns[0]
            y_column = df.columns[1]
            fig = px.bar(df, x=x_column, y=y_column, title=f"Results for: {generated_query}")
        else:
            fig = px.line(df, title="Insufficient data for graphing")

        return f"Generated SQL Query:\n{generated_query}", fig
    return "", {}

if __name__ == '__main__':
    app.run_server(debug=True)
