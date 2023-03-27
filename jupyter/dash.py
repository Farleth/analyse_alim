from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
from dash.dash_table import FormatTemplate, DataTable

from dash_bootstrap_templates import load_figure_template

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

app.layout = html.Div([
    html.H1(id="title",
            children='AAAH')
        ]
    )

if __name__ == "__main__":
    app.run_server(debug=True)
