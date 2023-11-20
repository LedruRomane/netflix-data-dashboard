import dash
from dash import html

dash.register_page(
    __name__,
    path_template="/test",
)
layout = html.Div("Forward outlook")