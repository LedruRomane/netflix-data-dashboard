import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd


# Utils
def get_color_for_score(score, num_colors=10, color_palette="coolwarm"):
    """
    Retourne une couleur correspondant à la note du film.
    """
    cmap = plt.get_cmap(color_palette, num_colors)
    if pd.isna(score) or score < 0 or score > 10:
        return "#808080"
    color_index = int(score * (num_colors - 1) / 10)
    return matplotlib.colors.rgb2hex(cmap(color_index))


def filter_titles_by_score(titles_data, credits_data, selected_scores):
    # Calculer la note moyenne pour chaque film
    titles_data["average_score"] = titles_data[["imdb_score", "tmdb_score"]].mean(
        axis=1
    )
    # Filtrer les films dont la note moyenne est égale à la note sélectionnée
    filtered_titles = pd.DataFrame()
    for n in selected_scores:
        # Filtrer les lignes pour cet intervalle spécifique
        temp_df = titles_data[
            (titles_data["average_score"] >= n)
            & (titles_data["average_score"] <= n + 1)
        ]

        # Ajouter les résultats au DataFrame filtré
        filtered_titles = pd.concat([filtered_titles, temp_df])

    filtered_titles = filtered_titles.drop_duplicates()

    # Filtrer les données de crédits pour inclure uniquement les films sélectionnés
    return credits_data[credits_data["id"].isin(filtered_titles["id"])]


def filter_titles_per_year(titles_data, credits_data, year):
    # Filtrer les films dont la note moyenne est égale à la note sélectionnée
    filtered_titles = pd.DataFrame()
    # Filtrer les lignes pour cet intervalle spécifique
    temp_df = titles_data[
        (titles_data["year"] >= year) & (titles_data["year"] <= year + 10)
    ]
    # Filtrer les résultats pour avoir seulement les 10 premiers
    temp_df = temp_df.sort_values(by=["average_score"], ascending=False).head(10)

    # Ajouter les résultats au DataFrame filtré
    filtered_titles = pd.concat([filtered_titles, temp_df])

    filtered_titles = filtered_titles.drop_duplicates()
    # Filtrer les données de crédits pour inclure uniquement les films sélectionnés
    actors = credits_data[credits_data["id"].isin(filtered_titles["id"])]
    return actors, filtered_titles


def create_movie_network_with_color(
    credits_data,
    titles_data,
    node_size=10,
    color_palette="coolwarm",
    selected_scores=None,
):
    """
    Crée un graphe de réseau pour les films connectés par des acteurs communs et attribue une couleur
    aux nœuds en fonction de la note moyenne du film.

    Args:
    credits_data (pd.DataFrame): DataFrame contenant les données des acteurs et des films.
    titles_data (pd.DataFrame): DataFrame contenant les informations sur les films.
    node_size (int): Taille des nœuds dans le graphe.

    Returns:
    plotly.graph_objs._figure.Figure: Un objet Figure Plotly représentant le graphe de réseau.
    """

    if selected_scores is not None and len(selected_scores) > 0:
        # Filtrer les films en fonction de la note
        credits_data = filter_titles_by_score(
            titles_data, credits_data, selected_scores
        )
    # Création d'un dictionnaire pour associer chaque acteur à ses films
    actor_to_movies = {}
    for index, row in credits_data.iterrows():
        actor_to_movies.setdefault(row["name"], []).append(row["id"])

    # Création d'un graphe vide
    G = nx.Graph()

    # Ajout des nœuds (films) et des arêtes (relations entre films basées sur des acteurs communs)
    for actor, movies in actor_to_movies.items():
        for i in range(len(movies)):
            for j in range(i + 1, len(movies)):
                G.add_edge(movies[i], movies[j])

    # Positionnement des nœuds
    pos = nx.spring_layout(G)

    # Création des arêtes
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Création des nœuds
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    for node in G.nodes():
        x, y = pos[node]
        # Calculer la note moyenne du film
        film_data = titles_data[titles_data["id"] == node]
        if not film_data.empty:
            imdb_score = film_data["imdb_score"].values[0]
            tmdb_score = film_data["tmdb_score"].values[0]
            avg_score = (
                (imdb_score + tmdb_score) / 2
                if pd.notnull(imdb_score) and pd.notnull(tmdb_score)
                else None
            )

            node_text.append(f"{film_data['title'].values[0]} - Avg Score: {avg_score}")
            # Attribuer une couleur en fonction de la note
            node_color.append(
                get_color_for_score(avg_score, color_palette=color_palette)
            )
        else:
            node_text.append("Unknown Film")
            node_color.append("#808080")  # Gris pour les films inconnus
        node_x.append(x)
        node_y.append(y)

    # Création de la figure Plotly
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        marker=dict(showscale=False, size=node_size, color=node_color, line_width=2),
    )

    # Création de la figure finale
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Réseau de Films basé sur des Acteurs Communs",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig
