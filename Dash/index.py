# Import packages
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Netflix Datas Analysis Dashboard', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
            html.Div(dcc.Link(f"{page['name']} - {page['path']}", href=page["path"]))                
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
    ]), html.Hr(),
    dash.page_container,
], fluid=True)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
