import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from data_operations import get_unique_genres, get_data_title_cleaned, get_movie

# PAGE
dash.register_page(
    __name__,
    path_template="/graph",
)

# DATAS
data_title = get_data_title_cleaned()
movies = get_movie(data_title)

# clean movies to get only runtime, years, genres
movies_runtime = movies[['title', 'runtime', 'release_year', 'genres']]

genres = get_unique_genres(data_title)
genres.insert(0, 'all')

# FORM
dropdownn_genres = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in genres],
        value=genres[0],
        clearable=False
    )
])

radios_items = html.Div([
    dbc.RadioItems(
        options=[{"label": x, "value": x} for x in ['Tout afficher', 'Après 1980']],
        value='Tout afficher',
        inline=True,
        id='time'
    )
])

# LAYOUT
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Graphique')
        ]),
    ]),
    dbc.Row([
        html.Label('Genre de film :'),
        dbc.Col([
            dropdownn_genres
        ], width=3),
        dbc.Col([
            radios_items
        ], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='graph')
        ], width=10),
    ]),
])


# CALLBACKS
@callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='time', component_property='value'),
     Input(component_id='genre-dropdown', component_property='value')]
)
def update_graph(col_chosen, selected_genre):
    if selected_genre != 'all':
        filtered_data = movies_runtime[movies_runtime['genres'].apply(lambda x: selected_genre in x)]
    else:
        filtered_data = movies_runtime

    # Filtrer par année si nécessaire
    if col_chosen == 'Après 1980':
        filtered_data = filtered_data[filtered_data['release_year'] >= 1980]

    # Créer le graphique
    fig = px.histogram(filtered_data, x='release_year', y='runtime', histfunc='avg')
    return fig