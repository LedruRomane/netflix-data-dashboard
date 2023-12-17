from dash import dcc, html
import dash_bootstrap_components as dbc

style = {
    "padding": "10px",
    "margin": "10px",
    "border": "1px solid #ddd",
    "borderRadius": "5px",
    "overflowY": "auto",
    "boxShadow": "2px 2px 2px lightgrey",
    "display": "flex",
    "flexDirection": "column",
}

Explanation = [
    html.P("On peut observer plusieurs choses grâce à ce graphe:"),
    html.P(
        "1. Nœuds et liens : Chaque nœud (cercle) représente un film, et chaque lien (ligne) représente un acteur commun entre les films."
    ),
    html.P(
        "2. Acteurs clés : Les acteurs à inclure sont spécifiés comme Robert De Niro, Martin Scorsese et Al Pacino. Le réseau est construit autour des films dans lesquels ces acteurs spécifiques ont joué. On peut s'aider pour cela du graphe au dessus pour savoir qui sont les acteurs les plus populaires."
    ),
    html.P(
        "3. Lien entre acteurs et popularité d'un film : Ce graphe permet avant tout de voir si le fait d'avoir des acteurs populaires dans un film a un impact sur la popularité du film. On peut voir que les films avec Robert De Niro et Martin Scorsese sont très populaires avec note moyenne (imdb/tmdb) élevée."
    ),
]


def build_titles_network(
    title_selector, actor_selector_dropdown_options, default_actor_dropdown_options
):
    return dbc.Row(
        [
            dbc.Col([dcc.Graph(id="movie-network-graph")]),
            dbc.Col(
                [
                    dbc.Row(
                        [html.H1("Réseau de Films/Séries basé sur des Acteurs Communs")]
                    ),
                    dbc.Row(Explanation, style=style),
                    dbc.Row(
                        [
                            html.H2("Paramètres"),
                            html.H3("Taille des noeuds"),
                            dcc.Slider(
                                id="node-size-slider",
                                min=10,
                                max=50,
                                step=10,
                                value=20,
                            ),
                            # html.H3(
                            #     "Top 10 de tous les titres par décennies/siècles selon leurs notes obtenus sur IMDB/TMDB"
                            # ),
                            # dcc.Dropdown(
                            #     id="title-selection-dropdown",
                            #     options=title_selector,
                            #     multi=False,
                            # ),
                            html.H3(
                                "Acteurs à inclure (une fois sélectionné, la liste est re-calculé avec seulement les acteurs en commun)"
                            ),
                            dcc.Dropdown(
                                id="actor-selector",
                                options=actor_selector_dropdown_options,
                                value=default_actor_dropdown_options,
                                multi=True,
                            ),
                            html.H3(
                                "Palettes de couleurs (pour les films/séries sans note, la couleur grise est utilisée)"
                            ),
                            dcc.Dropdown(
                                id="color-palette-selector",
                                options=[
                                    {"label": "Viridis", "value": "viridis"},
                                    {"label": "Plasma", "value": "plasma"},
                                    {"label": "Inferno", "value": "inferno"},
                                    {"label": "Magma", "value": "magma"},
                                    {"label": "Cividis", "value": "cividis"},
                                    {"label": "Coolwarm", "value": "coolwarm"},
                                    {"label": "Spectral", "value": "Spectral"},
                                    {"label": "PiYG", "value": "PiYG"},
                                    {"label": "PRGn", "value": "PRGn"},
                                    {"label": "Twilight", "value": "twilight"},
                                    {"label": "HSV", "value": "hsv"},
                                    {"label": "Pastel1", "value": "Pastel1"},
                                    {"label": "Set3", "value": "Set3"},
                                    {"label": "Tab10", "value": "tab10"},
                                    {"label": "Accent", "value": "Accent"},
                                ],
                                value="viridis",  # Valeur par défaut
                            ),
                            html.H3(
                                id="score-selector-title",
                                title="Filtrer les films/séries par note (les films/séries sans note ne sont pas affichés)",
                            ),
                            dcc.Dropdown(
                                id="score-selector",
                                options=[
                                    {"label": str(score), "value": score}
                                    for score in range(1, 11)
                                ],
                                multi=True,
                                placeholder="Sélectionnez une note",
                            ),
                        ]
                    ),
                ],
                style=style,
            ),
        ],
    )
