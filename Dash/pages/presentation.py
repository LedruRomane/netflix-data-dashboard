import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, dcc, callback, dash_table
from data_operations import get_unique_genres, get_data_title_cleaned
import pandas as pd

# PAGE
dash.register_page(
    __name__,
    path_template="/presentation",
)

# DATAS

data_title = get_data_title_cleaned()

checklist_style = {
    'padding': '10px',
    'margin': '10px',
    'border': '1px solid #ddd',
    'borderRadius': '5px',
    'overflowY': 'auto',
    'boxShadow': '2px 2px 2px lightgrey',
    'display': 'flex',
    'flexDirection': 'column',
}

checkbox_style = {
    'margin': '5px',
    'display': 'inline-block'
}

# LAYOUT
layout = html.Div([
    html.H1('Présentation des données'),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table',
                data=data_title.to_dict('records'),
                columns=[{"name": col, "id": col} for col in data_title.columns],
                page_size=12, 
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                }
            ),
        ], width=7),
        dbc.Col([
            dcc.Checklist(
            id='columns-checklist',
            options=[{'label': col, 'value': col} for col in data_title.columns],
            value=data_title.columns.tolist(),  # Toutes les colonnes sont sélectionnées par défaut
            inline=True,
            style=checklist_style,
            labelStyle=checkbox_style
            ),
        ]),
    ]),
])

# CALLBACKS

# checkboxes
@callback(
    Output("table", "columns"), Input('columns-checklist', 'value')
)
def update_table(selected_columns):
    columns_to_show = [{"name": col, "id": col} for col in data_title.columns if col in selected_columns]
    return columns_to_show