import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from data_operations import get_unique_genres, get_data_title_cleaned, get_movie

### PAGE ###

dash.register_page(
    __name__,
    path_template="/movies",
)

### DATAS ###

data_title = get_data_title_cleaned()
movies = get_movie(data_title)

# clean movies to get only runtime, years, genres
movies_runtime = movies[['title', 'runtime', 'release_year', 'genres']]

# clean movies to get only years, genres, tmdb & imdb scores
movies_avg_score = movies[['title', 'release_year', 'genres', 'tmdb_score', 'imdb_score']]

# calculates the avg between imdb and tmdb
for index, show in movies_avg_score.iterrows():
    movies_avg_score.at[index, 'avg_score'] = (show['tmdb_score'] + show['imdb_score']) / 2

genres = get_unique_genres(data_title)
genres.insert(0, 'all')

genres = get_unique_genres(data_title)
genres.insert(0, 'all')

### FORM COMPONENTS ###
default_dropdown_value = genres[0]
dropdownn_genres = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in genres],
        value=default_dropdown_value,
        clearable=False
    )
])

# second dropdown for second graph
dropdown_genres2 = html.Div([
    dcc.Dropdown(
        id='genre-movies-dropdown2',
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
        id='time'
    )
])

# second radio buttons for second graph
radios_items_score = html.Div([
    dbc.RadioItems(
        options=[{"label": x, "value": x} for x in ['Tout afficher', 'IMDb', 'TMDb']],
        value='Tout afficher',
        inline=True,
        id='score-movies-radio'
    )
])


### LAYOUT ###

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('FILMS'),
        ]),
    ], style={'margin': '10px'}),

    # Graph 1 : Durée moyenne des films par année
    dbc.Row([
        html.H3('Durée moyenne des films Netflix par année'),
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

    # Graph 2 : Genre les plus appréciés
    dbc.Row([
        html.H3('Moyenne des notes des films les plus appréciés par an (source TMDb et IMDb)'),
        html.Label('Genre de film :'),
            dbc.Col([
                dropdown_genres2
            ], width=3),
            dbc.Col([
                radios_items_score
            ], width=3),
        ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='graph-score')
        ], width=10),
    ]),
])


### CALLBACKS ###

# Graph 1 : Durée moyenne des films par année
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

# Graph 2 : Score imdb et tmdb pour chaque genre par an
@callback(
    Output(component_id='graph-score', component_property='figure'),
    [Input(component_id='score-movies-radio', component_property='value'),
     Input(component_id='genre-movies-dropdown2', component_property='value')]
)
def update_graph2(col_chosen, selected_genre):
    if selected_genre != 'all':
        filtered_data = movies_avg_score[movies_avg_score['genres'].apply(lambda x: selected_genre in x)]
    else:
        filtered_data = movies_avg_score

    # Filtrer par imdb ou tmdb, ou la moyenne des deux
    avg_score = 'avg_score'
    if col_chosen == 'IMDb':
        avg_score = 'imdb_score'
    elif col_chosen == 'TMDb':
        avg_score = 'tmdb_score'
    else:
        avg_score = 'avg_score'        

    # Créer le graphique
    fig = px.histogram(filtered_data, x='release_year', y= avg_score, histfunc='avg')
    return fig