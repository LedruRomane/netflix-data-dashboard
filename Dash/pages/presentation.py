import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, html, dcc, callback, dash_table
from data_operations import get_data_title_cleaned
import plotly.express as px
import pandas as pd
import ast
from collections import Counter

### PATH ###
dash.register_page(
    __name__,
    path_template="/",
)

### DATAS ###

data_title = get_data_title_cleaned()
number_of_titles = len(data_title.index)
number_of_movies = len(data_title[data_title['type'] == 'MOVIE'].index)
number_of_shows = len(data_title[data_title['type'] == 'SHOW'].index)

### STYLES ###

style = {
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

### LAYOUT ###

layout = html.Div([
    html.H1('Présentation des données', style={'textAlign': 'center'}),
    html.H3('Netflix Movies and TV Shows'),

    # Informations sur le dataset
    dbc.Row([
        html.H3('Informations sur le dataset'), 
        html.P(f'Nombre de titres : {number_of_titles}'),
        html.P(f'Nombre de films : {number_of_movies}'),
        html.P(f'Nombre de séries : {number_of_shows}'),
    ], style=style),
   

    # Tableau de toutes les données
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                style_data={
                    'textAlign': 'left',
                },
                id='table',
                data=data_title.to_dict('records'),
                columns=[{"name": col, "id": col} for col in data_title.columns],
                page_size=12,
            ),
        ], width=9, style=style),
        dbc.Col([
            html.H5('Champs disponibles sur le dataset'),
            dcc.Checklist(
            id='columns-checklist',
            options=[{'label': col, 'value': col} for col in data_title.columns],
            value=data_title.columns.tolist(),  # Toutes les colonnes sont sélectionnées par défaut
            inline=True,
            style=style,
            labelStyle=checkbox_style
            ),
        ]),
    ]),

    # Graph 1 : Répartition des titres par genre
    dbc.Row([
        html.H3('Répartition des titres par genre'),
        dcc.Dropdown(
            id='type-selector',
            options=[
                {'label': 'Movies', 'value': 'MOVIE'},
                {'label': 'Shows', 'value': 'SHOW'},
                {'label': 'Both', 'value': 'BOTH'}
            ],
            value='BOTH',  # Valeur par défaut
            clearable=False
        ),
        dcc.Graph(id='genre-pie-chart')
    ], style=style),

    # Graph 2 : Répartition des titres par pays
    dbc.Row([
        html.H3('Répartition des titres par pays (de production)'),
        dcc.Dropdown(
            id='type-selector-2',
            options=[
                {'label': 'Movies', 'value': 'MOVIE'},
                {'label': 'Shows', 'value': 'SHOW'},
                {'label': 'Both', 'value': 'BOTH'}
            ],
            value='BOTH',  # Valeur par défaut
            clearable=False
        ),
        dcc.Graph(id='country-pie-chart')
    ], style=style),
])

### CALLBACKS ###

# Tableau 1: checkboxes datatable
@callback(
    Output("table", "columns"), Input('columns-checklist', 'value')
)
def update_table(selected_columns):
    columns_to_show = [{"name": col, "id": col} for col in data_title.columns if col in selected_columns]
    return columns_to_show

# Graph 1 : Répartition des titres par genre
@callback(
    Output('genre-pie-chart', 'figure'),
    [Input('type-selector', 'value')]
)
def update_graph(selected_type):
    filtered_data = data_title
    if selected_type != 'BOTH':
        filtered_data = data_title[data_title['type'] == selected_type]

    genre_counts = Counter()
    for genres in filtered_data['genres']:
        if pd.notna(genres):
            genres_list = ast.literal_eval(genres)
            genre_counts.update(genres_list)

    labels = list(genre_counts.keys())
    values = list(genre_counts.values())

    fig = px.pie(
        names= labels,
        values= values,
        hole=.3,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

# Graph 2 : Répartition des titres par pays (de production)
@callback(
    Output('country-pie-chart', 'figure'),
    [Input('type-selector-2', 'value')]
)
def update_graph(selected_type):
    filtered_data = data_title
    if selected_type != 'BOTH':
        filtered_data = data_title[data_title['type'] == selected_type]

    country_count = Counter()
    for country in filtered_data['production_countries']:
        if pd.notna(country):
            country_list = ast.literal_eval(country)
            country_count.update(country_list)

    labels = list(country_count.keys())
    values = list(country_count.values())

    fig = px.pie(
        names= labels,
        values= values,
        hole=.3,
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig