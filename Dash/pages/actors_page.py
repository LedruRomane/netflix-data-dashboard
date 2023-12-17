import dash
from dash import callback
from dash.dependencies import Input, Output

from itertools import combinations
import plotly.graph_objects as go

from layout.actor_layout import create_actor_layout

from utils.credits_utils import find_common_actors_movies, create_actor_network
from utils.titles_network_utils import create_movie_network_with_color


import pandas as pd

dash.register_page(__name__, path_template="/actors", title="Acteurs", name="Acteurs")

## Data ##
titles_data = pd.read_csv("./data/titles.csv")
credits_data = pd.read_csv("./data/credits.csv")
titles_data["title"].fillna("Unknown", inplace=True)
grouped = credits_data.groupby("id")["name"].apply(list)
actor_pairs = []
for actors in grouped:
    for pair in combinations(actors, 2):
        actor_pairs.append(pair)

unique_movie_ids = credits_data[credits_data["id"].isin(titles_data["id"])][
    "id"
].unique()
id_to_title_dict = (
    titles_data.dropna(subset=["title"]).set_index("id")["title"].to_dict()
)
dropdown_options = [
    {"label": title, "value": str(title_id)}
    for title_id, title in sorted(id_to_title_dict.items(), key=lambda item: item[1])
]
title_category_dict = {
    "all_time": -1,
    "2020": 2020,
    "2010": 2010,
    "2000": 2000,
    "20th": 1900,
}

title_selector = [
    {
        "label": "Top 10 des titres les mieux notés sur IMDB et TMDB ALL-TIME",
        "value": title_category_dict["all_time"],
    },
    {
        "label": "Top 10 des titres les mieux notés sur IMDB et TMDB années 2020",
        "value": title_category_dict["2020"],
    },
    {
        "label": "Top 10 des titres les mieux notés sur IMDB et TMDB années 2010",
        "value": title_category_dict["2010"],
    },
    {
        "label": "Top 10 des titres les mieux notés sur IMDB et TMDB années 2000",
        "value": title_category_dict["2000"],
    },
    {
        "label": "Top 10 des titres les mieux notés sur IMDB et TMDB du 20ième siècle",
        "value": title_category_dict["20th"],
    },
]


actor_selector_dropdown = [
    {"label": actor, "value": actor} for actor in credits_data["name"].unique()
]

layout = create_actor_layout(
    titles_dropdown_options=dropdown_options,
    actor_selector_dropdown_options=actor_selector_dropdown,
    best_titles_per_decade_century_list=title_selector,
)

## Callbacks ##


@callback(
    Output("film-selector-container", "style"),
    [Input("top-actors-dropdown", "value")],
)
def toggle_film_selector_visibility(selected_actor):
    if selected_actor:
        # Si un acteur est sélectionné, masquer le bouton et la liste
        return {"display": "none"}
    else:
        # Sinon, les afficher
        return {"display": "block"}


@callback(
    [
        Output("actor-network", "figure"),
        Output("sorted-actors-store", "data"),  # Stocker les données dans dcc.Store
    ],
    [
        Input("movie-id-dropdown", "value"),
        Input("top-actors-dropdown", "value"),  # Sélection de l'acteur
        Input("scale-factor-slider", "value"),
    ],
)
def update_graph(selected_movie_ids, selected_actor, scale_factor):
    if selected_actor:
        actor_movies = credits_data[credits_data["name"] == selected_actor][
            "id"
        ].unique()
        fig, sorted_actors = create_actor_network(
            credits_data, actor_movies, scale_factor
        )
    elif selected_movie_ids:
        fig, sorted_actors = create_actor_network(
            credits_data, selected_movie_ids, scale_factor
        )
    else:
        fig = go.Figure()
        sorted_actors = []

    sorted_actors_json = [
        {"actor": actor, "connections": connections}
        for actor, connections in sorted_actors
    ]

    return fig, sorted_actors_json


@callback(
    Output("top-actors-dropdown", "options"), [Input("sorted-actors-store", "data")]
)
def update_actor_list(sorted_actors_data):
    if sorted_actors_data:
        sorted_actors = [
            (item["actor"], item["connections"]) for item in sorted_actors_data[:10]
        ]
        return [{"label": actor, "value": actor} for actor, _ in sorted_actors]
    return []


@callback(
    Output("movie-id-dropdown", "options"),
    [Input("movie-id-dropdown", "value")],  # Sélection des films
)
def update_movie_dropdown(selected_movie_ids):
    # Si des films sont sélectionnés, mettre à jour la liste en fonction des acteurs en commun
    if selected_movie_ids:
        common_movie_ids = find_common_actors_movies(selected_movie_ids, credits_data)
        new_options = [
            {"label": id_to_title_dict[movie_id], "value": movie_id}
            for movie_id in common_movie_ids
        ]
    # Si rien n'est sélectionné, afficher tous les films
    else:
        new_options = [
            {"label": id_to_title_dict[movie_id], "value": movie_id}
            for movie_id in id_to_title_dict
        ]

    return new_options


@callback(
    [Output("score-selector", "style"), Output("score-selector-title", "style")],
    [Input("actor-selector", "value")],
)
def toggle_score_selector(selected_actors):
    if selected_actors:
        return {"display": "block"}, {"display": "block"}
    else:
        return {"display": "none"}, {"display": "none"}


@callback(
    Output("movie-network-graph", "figure"),
    [
        Input("node-size-slider", "value"),
        # Input("title-selection-dropdown", "value"),
        Input("actor-selector", "value"),
        Input("color-palette-selector", "value"),
        Input("score-selector", "value"),
    ],
)
def update_graph(
    node_size, selected_actors, color_palette, selected_scores
):
    # if title_selection:
    #     fig = create_movie_network_with_color(
    #         filtered_credits_data,
    #         titles_data,
    #         node_size,
    #         color_palette=color_palette,
    #         selected_scores=selected_scores,
    #     )
    if selected_actors:
        selected_movies = credits_data[credits_data["name"].isin(selected_actors)][
            "id"
        ].unique()
        filtered_credits_data = credits_data[credits_data["id"].isin(selected_movies)]
        fig = create_movie_network_with_color(
            filtered_credits_data,
            titles_data,
            node_size,
            color_palette=color_palette,
            selected_scores=selected_scores,
        )
    else:
        fig = create_movie_network_with_color(
            credits_data,
            titles_data,
            node_size,
            color_palette=color_palette,
            selected_scores=selected_scores,
        )
    return fig
