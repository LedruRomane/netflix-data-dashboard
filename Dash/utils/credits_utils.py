import networkx as nx
import plotly.graph_objects as go


def find_common_actors_movies(selected_movie_ids, df):
    if not selected_movie_ids:
        return df["id"].unique().tolist()

    selected_actors = df[df["id"].isin(selected_movie_ids)]["name"].unique()
    common_movies = df[df["name"].isin(selected_actors)]["id"].unique()
    return common_movies.tolist()


def create_actor_network(df, movie_ids, scale_factor=0.5):
    """
    Crée un graphe de réseau pour les acteurs qui ont joué dans les films spécifiés.

    Args:
    df (pd.DataFrame): DataFrame contenant les données des acteurs et des films.
    movie_ids (list): Liste des identifiants des films à inclure dans le graphe.
    scale_factor (float): Dans ce code, j'ai ajouté un facteur de mise à l'échelle de 0.5 pour la taille des nœuds, avec une taille de base de 5.
    base_node_size (int): Vous pouvez ajuster ce facteur de mise à l'échelle pour obtenir la représentation visuelle souhaitée. Plus la valeur est élevée, plus la différence de taille entre les nœuds sera perceptible.

    Returns:
    plotly.graph_objs._figure.Figure: Un objet Figure Plotly représentant le graphe de réseau.
    """

    # Filtrage des données pour les films spécifiés
    filtered_df = df[df["id"].isin(movie_ids)]

    # Création d'un graphe vide
    G = nx.Graph()

    # Ajout des nœuds (acteurs) et des arêtes (relations entre acteurs) dans le graphe
    for movie_id in movie_ids:
        actors = filtered_df[filtered_df["id"] == movie_id]["name"].unique()
        for actor in actors:
            G.add_node(actor)
        for i in range(len(actors)):
            for j in range(i + 1, len(actors)):
                G.add_edge(actors[i], actors[j])

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
    for node in G.nodes():
        x, y = pos[node]
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
        text=list(G.nodes()),
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            size=10,
            color=[],
            colorbar=dict(
                thickness=15,
                title="Nombre de Connexions",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
    )

    # Ajout du nombre de connexions comme attribut de couleur pour les nœuds
    node_adjacencies = []

    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies
    node_trace.marker.size = [adj * scale_factor for adj in node_adjacencies]

    # Créer un dictionnaire pour compter les connexions pour chaque acteur
    actor_connections = {actor: len(list(G.neighbors(actor))) for actor in G.nodes()}
    # Trier les acteurs par nombre de connexions
    sorted_actors = sorted(actor_connections.items(), key=lambda x: x[1], reverse=True)

    # Création de la figure finale
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Réseau des acteurs dans les films/séries sélectionnés",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="A chaque sélection de films/séries, la liste est re-calculé avec seulement les acteurs en commun.",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig, sorted_actors
