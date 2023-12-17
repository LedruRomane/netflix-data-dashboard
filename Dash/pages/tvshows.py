import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from data_operations import get_tvshow, get_unique_genres, get_data_title_cleaned
import plotly.graph_objects as go
from plotly.graph_objs import Scatter

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

# clean tvshows to get only years, genres, tmdb & imdb scores
tvshow_avg_score = tvshow[['title', 'release_year', 'genres', 'tmdb_score', 'imdb_score']]

# calculates the avg between imdb and tmdb
for index, show in tvshow_avg_score.iterrows():
    tvshow_avg_score.at[index, 'avg_score'] = (show['tmdb_score'] + show['imdb_score']) / 2

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

# second dropdown for second graph
dropdown_genres2 = html.Div([
    dcc.Dropdown(
        id='dropdown_genres2',
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

    # Graph 2 : Genre les plus appréciés
    dbc.Row([
        html.H3('Moyenne des notes des séries les plus appréciés par an (source TMDb et IMDb)'),
        html.Label('Genre de la série :'),
        dbc.Col([
            dropdown_genres2
        ], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='graph-tmdb')
        ], width=10),
    ]),
])


### CALLBACKS ###

# Graph 1 : Durée moyenne d'un épisode de série par année
@callback(
    Output(component_id='graph-tvshow', component_property='figure'),
    [Input(component_id='time-tvshow-radio', component_property='value'),
     Input(component_id='genre-tvshow-dropdown', component_property='value')]
)
def update_graph1(col_chosen, selected_genre):
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

# Graph 2 : Score imdb et tmdb pour chaque genre par an
@callback(
    Output(component_id='graph-tmdb', component_property='figure'),
    Input(component_id='dropdown_genres2', component_property='value')
)
def update_graph_line(selected_genre):
    if selected_genre == 'all':
        filtered_data = tvshow
    else:
        filtered_data = tvshow[tvshow['genres'].str.contains(selected_genre)]

    filtered_data = filtered_data[['release_year', 'imdb_score', 'tmdb_score']]

    grouped_data = filtered_data.groupby('release_year').mean()

    fig = go.Figure()

    fig.add_trace(Scatter(x=grouped_data.index, y=grouped_data['imdb_score'], mode='lines', name='IMDb Score'))
    fig.add_trace(Scatter(x=grouped_data.index, y=grouped_data['tmdb_score'], mode='lines', name='TMDB Score'))

    fig.update_layout(
        title='IMDb and TMDB Scores by Year for Selected Genre',
        xaxis_title='Year',
        yaxis_title='Average Score',
        legend_title='Score Type'
    )

    return fig