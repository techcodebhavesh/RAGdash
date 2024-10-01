import pandas as pd
from pandas_profiling import ProfileReport
import os
from groq import Groq
import base64
import io
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Groq API client
client = Groq(
    api_key="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",
)

# Function to handle CSV upload and generate a profile report
def process_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Profile the data
    profile = ProfileReport(df, title="Data Profile Report", explorative=True)
    profile.to_file("data_profile.html")

    return df, profile

# Function to ask the LLM for chart suggestions based on a data summary
def ask_llm_about_data(data_summary, column_names):
    chart_options = "Supported chart types: bar, scatter, line, pie. "
    columns_list = f"Available columns: {', '.join(column_names)}. "
    
    messages = [
        {
            "role": "user",
            "content": f"Suggest visualizations based on the following data summary:\n\n{data_summary}\n\n{chart_options}{columns_list}Please specify the chart type and the columns for the x-axis and y-axis (if applicable)."
        }
    ]
    
    # LLM response
    response = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    return response.choices[0].message.content

# Function to clean the data
def clean_data(df):
    # Drop duplicate rows
    df = df.drop_duplicates()

    # Handle missing values: Fill numeric columns with median, categorical with mode
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())
    
    return df

# Function to generate a chart
def generate_chart(df, chart_type, x, y=None):
    if chart_type == 'bar':
        fig = px.bar(df, x=x, y=y)
    elif chart_type == 'scatter':
        fig = px.scatter(df, x=x, y=y)
    elif chart_type == 'line':
        fig = px.line(df, x=x, y=y)
    elif chart_type == 'pie':
        fig = px.pie(df, names=x)
    else:
        raise ValueError("Unsupported chart type")

    return fig

# Dash App Initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout for the app
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("CSV Data Analyzer"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            )),
        ]),
        dbc.Row([
            dbc.Col(dcc.Loading(id="loading-output", children=[html.Div(id='output-data-upload')], type="default")),
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='output-chart-suggestions')),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='output-chart')),
        ]),
    ])
])

# Callback to process the uploaded CSV
@app.callback(
    Output('output-data-upload', 'children'),
    Output('output-chart-suggestions', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
)
def update_output(contents, filename):
    if contents is None:
        return html.Div("Upload a CSV file to analyze."), ""

    # Assuming contents is the base64 encoded CSV
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    
    # Process CSV and clean data
    df = clean_data(df)

    # Summarize the data for the LLM
    data_summary = df.describe().to_string()
    column_names = df.columns.tolist()

    # Ask LLM for chart suggestions
    chart_suggestions = ask_llm_about_data(data_summary, column_names)
    
    # Display data and chart suggestions
    return html.Div(f"Data successfully processed for {filename}"), html.Div(f"Suggested charts: {chart_suggestions}")

# Callback to generate chart based on LLM suggestion
@app.callback(
    Output('output-chart', 'figure'),
    Input('output-chart-suggestions', 'children')
)
def display_chart(suggestions):
    # Example of parsing the LLM's suggestion
    if 'bar' in suggestions.lower():
        chart_type = "bar"
        x_column = 'Age'  # Extracted from LLM suggestion (example)
        y_column = 'Salary'  # Extracted from LLM suggestion (example)
    elif 'scatter' in suggestions.lower():
        chart_type = "scatter"
        x_column = 'Age'  # Extracted from LLM suggestion (example)
        y_column = 'Salary'  # Extracted from LLM suggestion (example)
    elif 'line' in suggestions.lower():
        chart_type = "line"
        x_column = 'Age'  # Extracted from LLM suggestion (example)
        y_column = 'Salary'  # Extracted from LLM suggestion (example)
    elif 'pie' in suggestions.lower():
        chart_type = "pie"
        x_column = 'Category'  # Extracted from LLM suggestion (example)
    else:
        raise ValueError("Unsupported chart type suggested by LLM")
    
    # Generate chart based on the parsed suggestion
    fig = generate_chart(df, chart_type, x=x_column, y=y_column if chart_type != 'pie' else None)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
