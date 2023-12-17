import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, html, dcc, callback, dash_table
from data_operations import get_data_title_cleaned, normalize_df
import plotly.express as px
import pandas as pd
import ast
from collections import Counter
import plotly.graph_objects as go

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
normalised_data = normalize_df(get_data_title_cleaned())

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

    # Graph 3 : Répartition des titres par année avec un slider pour être plus précis
    dbc.Row([
        html.H3('Répartition des titres par année'),
        dcc.Dropdown(
            id='type-selector-3',
            options=[
                {'label': 'Movies', 'value': 'MOVIE'},
                {'label': 'Shows', 'value': 'SHOW'},
                {'label': 'Both', 'value': 'BOTH'}
            ],
            value='BOTH',  # Valeur par défaut
            clearable=False
        ),
        dcc.Graph(id='year-line'),
        dcc.RangeSlider(1950, 2023, 10, value=[1980, 2020], id='years-slider', marks={i: '{}'.format(i) for i in range(1950, 2023, 10)}),
    ], style=style),

    # Graph 4 : Heatmap 
    dbc.Row([
        dbc.Col([
            html.H3('Heatmap'),
            html.P('Sélectionnez les champs à afficher :'),
            dcc.Checklist(
                id='field-selector',
                options=[{'label': col, 'value': col} for col in [
                    'type',
                    'release_year',
                    'age_certification',
                    'runtime',
                    'genres',
                    'production_countries',
                    'seasons',
                    'imdb_score',
                    'imdb_votes',
                    'tmdb_popularity',
                    'tmdb_score'
                ]],
                value=['type',
                    'runtime',
                    'imdb_score',
                    'imdb_votes',
                    'tmdb_popularity',
                    'tmdb_score'],  # Toutes les colonnes sont sélectionnées par défaut
                inline=True,
                style={
                    'maxWidth': '600px',
                    'margin': '20px auto',
                    'padding': '10px',
                    'borderRadius': '5px',
                    'backgroundColor': '#f9f9f9',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'fontSize': '16px',
                },
                inputStyle={
                    'cursor': 'pointer',
                    'marginRight': '5px'
                },
                labelStyle={
                    'marginRight': '10px',  # Space out the labels
                    'cursor': 'pointer',
                }
            ),
        ]),
        dbc.Col([
            dcc.Graph(id='heatmap'),
        ]),
    ], style=style),

    # Footer
    dbc.Row([
        html.P('2023 Analyse de données - Projet Netflix', style={'textAlign': 'center'})
    ], style={'margin': '30px'}),
    
    # Graph 5 : Evolution de la production de films et séries dans les 10 pays les plus producteurs
    dbc.Row([
        html.H3('Evolution de la production de films et séries dans les 10 pays les plus producteurs'),
        dcc.Dropdown(
            id='type-selector-5',
            options=[
                {'label': 'Movies', 'value': 'MOVIE'},
                {'label': 'Shows', 'value': 'SHOW'},
                {'label': 'Both', 'value': 'BOTH'}
            ],
            value='BOTH',  # Valeur par défaut
            clearable=False
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure={}, id='lineplot')
            ], width=10),
    ]),
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

# Graph 3 : Répartition des titres par année avec un slider pour être plus précis
@callback(
    Output('year-line', 'figure'),
    [Input('type-selector-3', 'value'),
     Input('years-slider', 'value')]
)
def update_graph(selected_type, selected_years):
    filtered_data = data_title[
        (data_title['release_year'] >= selected_years[0]) & 
        (data_title['release_year'] <= selected_years[1])
    ]

    fig = go.Figure()

    if selected_type == 'BOTH':
        for t in ['MOVIE', 'SHOW']:
            type_data = filtered_data[filtered_data['type'] == t]
            year_count = Counter(type_data['release_year'])
            labels, values = zip(*sorted(year_count.items()))

            fig.add_trace(go.Scatter(x=labels, y=values, mode='lines', name=t))
    else:
        type_data = filtered_data[filtered_data['type'] == selected_type]
        year_count = Counter(type_data['release_year'])
        labels, values = zip(*sorted(year_count.items()))
        fig.add_trace(go.Scatter(x=labels, y=values, mode='lines', name=selected_type))


    return fig

# Graph 4 : Heatmap
@callback(
    Output('heatmap', 'figure'),
    Input('field-selector', 'value')
)
def update_heatmap(selected_fields):
    filtered_data = normalised_data[selected_fields]
    fig = px.imshow(filtered_data.corr(), text_auto=True, aspect="auto")
    return fig
    
# Graph 5 : Evolution de la production de films et séries dans les 10 pays les plus producteurs
@callback( 
    Output('lineplot', 'figure'),
    [Input('type-selector-5', 'value')]
)
def update_graph(selected_type):
    filtered_data = data_title
    if selected_type != 'BOTH':
        filtered_data = data_title[data_title['type'] == selected_type]
    
    # Compter les productions par pays et par année
    data_tuples = list(zip(filtered_data['production_countries'], filtered_data['release_year']))

    # Utilisation de Counter
    production_count = Counter(data_tuples)
           
    # Préparer les données pour le graphique
    years = []
    countries = []
    counts = []
    for (release_year, production_countries), count in production_count.items():
        years.append(release_year)
        countries.append(production_countries)
        counts.append(count)

    # Filtrer pour les 10 premiers pays
    top_countries = [production_countries for production_countries, count in Counter(countries).most_common(10)]
    filtered_data = [(release_year, production_countries, count) for release_year, production_countries, count in zip(years, countries, counts) if production_countries in top_countries]

    # Créer le DataFrame pour le graphique
    df = pd.DataFrame(filtered_data, columns=['release_year', 'production_countries', 'count'])

    fig = px.line(df, x='production_countries', y='count', color='release_year', title='Production Over Time by Country')

    return fig