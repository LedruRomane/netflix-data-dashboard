import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from data_operations import get_tvshow, get_unique_genres, get_data_title_cleaned

### PAGE ###

dash.register_page(
    __name__,
    path_template="/tvshow",
)

### DATAS ###

data_title = get_data_title_cleaned()
tvshow = get_tvshow(data_title)

# clean tvshows to get only runtime, years, genres
tvshow_runtime = tvshow[['title', 'runtime', 'release_year', 'genres']]

genres = get_unique_genres(data_title)
genres.insert(0, 'all')

### FORM COMPONENTS ###
default_dropdown_value = genres[0]
dropdownn_genres = html.Div([
    dcc.Dropdown(
        id='genre-tvshow-dropdown',
        options=[{'label': genre, 'value': genre} for genre in genres],
        value=default_dropdown_value,
        clearable=False
    )
])

radios_items = html.Div([
    dbc.RadioItems(
        options=[{"label": x, "value": x} for x in ['Tout afficher', 'Après 1980']],
        value='Tout afficher',
        inline=True,
        id='time-tvshow-radio'
    )
])

### LAYOUT ###

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('SERIES'),
        ]),
    ], style={'margin': '10px'}),

    # Graph 1 : Durée moyenne des films par année
    dbc.Row([
        html.H3('Durée moyenne d\'un épisode de séries Netflix par an'),
        html.Label('Genre de la série :'),
        dbc.Col([
            dropdownn_genres
        ], width=3),
        dbc.Col([
            radios_items
        ], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='graph-tvshow')
        ], width=10),
    ]),

    # Graph 2 : ?
    dbc.Row([
        html.H3('Genre de séries Netflix les plus appréciés'),
    ]),
])


### CALLBACKS ###

# Graph 1 : Durée moyenne des films par année
@callback(
    Output(component_id='graph-tvshow', component_property='figure'),
    [Input(component_id='time-tvshow-radio', component_property='value'),
     Input(component_id='genre-tvshow-dropdown', component_property='value')]
)
def update_graph(col_chosen, selected_genre):
    if selected_genre != 'all':
        filtered_data = tvshow_runtime[tvshow_runtime['genres'].apply(lambda x: selected_genre in x)]
    else:
        filtered_data = tvshow_runtime

    # Filtrer par année si nécessaire
    if col_chosen == 'Après 1980':
        filtered_data = filtered_data[filtered_data['release_year'] >= 1980]

    # Créer le graphique
    fig = px.histogram(filtered_data, x='release_year', y='runtime', histfunc='avg')
    return fig