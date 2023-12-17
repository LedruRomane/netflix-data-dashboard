from dash import dcc, html
import dash_bootstrap_components as dbc

from components.titles_network import build_titles_network
from components.actor_network import build_actor_network


# Dash Layouts of the page ##
def create_actor_layout(
    titles_dropdown_options,
    best_titles_per_decade_century_list,
    actor_selector_dropdown_options,
):
    default_title_ids_for_dropdown = ["tm180542", "tm155787", "tm84618"]
    default_actor_for_dropdown = ["Robert De Niro", "Martin Scorsese", "Al Pacino"]
    default_dropdown_options = []

    for options in titles_dropdown_options:
        if options["value"] in default_title_ids_for_dropdown:
            default_dropdown_options.append(options["value"])

    TitleNetworkGraph = build_titles_network(
        title_selector=best_titles_per_decade_century_list,
        actor_selector_dropdown_options=actor_selector_dropdown_options,
        default_actor_dropdown_options=default_actor_for_dropdown,
    )
    ActorNetwork = build_actor_network(
        titles_dropdown_options=titles_dropdown_options,
        default_dropdown_options=default_dropdown_options,
    )

    layout = html.Div(
        [
            ActorNetwork,
            TitleNetworkGraph,
            dbc.Row(
                [
                    html.P(
                        "2023 Analyse de données - Projet Netflix",
                        style={"textAlign": "center"},
                    )
                ],
                style={"margin": "30px"},
            ),
        ]
    )
    return layout
