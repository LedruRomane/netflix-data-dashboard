# Import packages
import dash_bootstrap_components as dbc
import dash
from app import app

### MENU NAVBAR ###
children = []
for page in dash.page_registry.values():
    children.append(dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["path"])))

navbar = dbc.NavbarSimple(
    children,
    brand="Netflix Datas Analysis Dashboard",
    brand_href="/",
    sticky="top",
)

### SKELETON BASE LAYOUT ###
app.layout = dbc.Container([
    dbc.Row([
        navbar
    ]),
    dash.page_container,
], fluid=True)

### SERVE APP ###
if __name__ == '__main__':
    app.run_server(debug=True)