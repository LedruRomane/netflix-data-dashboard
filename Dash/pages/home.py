import dash
from dash import html

dash.register_page(
    __name__,
    path_template="/",
)

layout = html.Div("Présentation des données")