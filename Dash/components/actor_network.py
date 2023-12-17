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
        "1. Points de connexion centraux (nœuds) : Les acteurs qui sont représentés par de plus gros nœuds, comme celui étiqueté 'Robert De Niro' au centre, semblent être les plus connectés. Cela signifie qu'ils ont joué avec un plus grand nombre d'acteurs dans les films sélectionnés."
    ),
    html.P(
        "2. Interconnectivité des films : Les films listés (par exemple, 'Goodfellas', 'Once Upon a Time in America', 'Taxi Driver') ont probablement des acteurs en commun, ce qui est illustré par les lignes qui les connectent."
    ),
    html.P(
        "3. Communautés d'acteurs : Des groupes d'acteurs souvent castés ensemble peuvent être identifiés, indiquant des collaborations fréquentes ou des équipes de production similaires."
    ),
]


def build_actor_network(titles_dropdown_options, default_dropdown_options):
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            html.H1(
                                "Lien entre les acteurs ayant joué dans un même film"
                            ),
                        ]
                    ),
                    dbc.Row(Explanation, style=style),
                    dbc.Row(
                        [
                            dcc.Store(
                                id="sorted-actors-store"
                            ),  # Stocke les données des acteurs triés
                            html.H2("Paramètres du réseau"),
                            html.H3("Top 10 acteurs les plus connectés"),
                            dcc.Dropdown(id="top-actors-dropdown"),
                            html.H3("Liste des films actualisé dynamiquement"),
                            html.Div(
                                id="film-selector-container",
                                style={"display": "none"},
                                children=[
                                    dcc.Dropdown(
                                        id="movie-id-dropdown",
                                        options=titles_dropdown_options,
                                        # Par défaut, on prend des films où on voit beaucoup Scorcese et De Niro.
                                        value=default_dropdown_options,
                                        multi=True,
                                    ),
                                ],
                            ),
                            html.H3("Ajustement de la taille des noeuds"),
                            dcc.Slider(
                                id="scale-factor-slider",
                                min=0.1,
                                max=0.25,
                                step=0.01,
                                value=0.1,
                                marks={i / 10: str(i / 10) for i in range(1, 26, 1)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                },
                            ),
                        ]
                    ),
                ],
                style=style,
            ),
            dbc.Col([dcc.Graph(id="actor-network")]),
        ]
    )
