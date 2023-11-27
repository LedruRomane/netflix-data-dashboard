# Import packages
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

children = []

for page in dash.page_registry.values():
    children.append(dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["path"])))

# Navbar 
navbar = dbc.NavbarSimple(
    children,
    brand="Netflix Datas Analysis Dashboard",
    brand_href="/",
    sticky="top",
)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        navbar
    ]),
    dash.page_container,
], fluid=True)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
