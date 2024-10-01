# frontend/dashboard.py
import dash
from dash import dcc, html
import plotly.express as px

# Sample layout
app = dash.Dash(__name__)

def create_dashboard(relevant_data, insights):
    """
    Creates a dashboard using Dash to display relevant data and LLM-generated insights.
    
    Args:
        relevant_data (list): The retrieved relevant data from the database.
        insights (str): The LLM-generated insights.
    
    Returns:
        layout (html.Div): The dashboard layout.
    """
    # Generate a chart from relevant data (using Plotly for visualization)
    fig = px.line(relevant_data, x='timestamp', y='usage_time', title='User Activity Over Time')

    return html.Div([
        html.H1("BI Agent Dashboard"),
        dcc.Graph(figure=fig),
        html.Div([
            html.H3("LLM-Generated Insights:"),
            html.P(insights)
        ])
    ])

if __name__ == '__main__':
    # Sample data for testing
    relevant_data = [
        {'timestamp': '2024-01-01', 'usage_time': 50, 'user_id': 123},
        {'timestamp': '2024-01-02', 'usage_time': 60, 'user_id': 123},
        # Add more data...
    ]
    insights = "Based on the data, the user activity increased by 20% over the week."

    app.layout = create_dashboard(relevant_data, insights)
    app.run_server(debug=True)
