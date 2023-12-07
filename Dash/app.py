# app.py
import dash
import dash_bootstrap_components as dbc

def create_app():
    app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
    return app

app = create_app()
