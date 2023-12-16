# Analyse du jeux de données Netflix (TUDUM)

<table style="margin: auto;">
    <tr>
        <td><img src="doc/netflix.png" alt="Netflix Logo" width="250" /></td>
        <td><img src="doc/lyon1.png" alt="Lyon 1 logo" width="250" /></td>
    </tr>
</table>

## Description des jeux de données 📄

**Aperçu du jeu de données :**

- un fichier `data/titres.csv` comprenant 5 000 titres uniques disponibles sur Netflix (films/séries) dont 15 colonnes détaillant divers aspects de chaque titre.
- un fichier `data/credits.csv` avec plus de 77 000 entrées pour les acteurs et les réalisateurs, comprenant 5 colonnes.

### Fichier des films/séries (`data/titles.csv`)

| Colonne               | Description de la donnée (Français)                     |
|-----------------------|---------------------------------------------------------|
| id                    | L'identifiant du titre sur JustWatch.                   |
| title                 | Le nom du titre.                                        |
| show_type             | Type de programme : série TV ou film.                   |
| description           | Une brève description.                                  |
| release_year          | L'année de sortie.                                      |
| age_certification     | La classification par âge.                              |
| runtime               | La durée de l'épisode (série) ou du film.               |
| genres                | Liste des genres.                                       |
| production_countries  | Liste des pays ayant produit le titre.                  |
| seasons               | Nombre de saisons (pour les séries).                    |
| imdb_id               | L'identifiant du titre sur IMDB.                        |
| imdb_score            | Note sur IMDB.                                          |
| imdb_votes            | Nombre de votes sur IMDB.                               |
| tmdb_popularity       | Popularité sur TMDB.                                    |
| tmdb_score            | Note sur TMDB.                                          |

### Fichier des acteurs/réalisateurs (`data/credits.csv`)

| Colonne         | Description de la donnée (Français)                 |
|-----------------|-----------------------------------------------------|
| person_ID       | L'identifiant de la personne sur JustWatch.         |
| id              | L'identifiant du titre sur JustWatch.               |
| name            | Le nom de l'acteur ou du réalisateur.               |
| character_name  | Le nom du personnage.                               |
| role            | Rôle : ACTEUR ou RÉALISATEUR.                       |

## Mise en place de l'environnement

## Pré-requis

- python >= 3.11
- pip

## Mise en place de l'environnement virtuel `venv` (optionnel mais conseillé)

[Documentation](https://docs.python.org/3/library/venv.html)

### Création de l'environnement virtuel

```shell
$ python3.X -m venv venv
```

### Source de ce dernier

Vous devez selon votre OS et votre Shell éxécuter la bonne commande `source`, referez-vous au tableau suivant dans la [documentation](https://docs.python.org/3/library/venv.html#how-venvs-work)

```shell
$ source venv/bin/activate
```

> Note: à chaque fois que vous ouvrez un nouveau terminale et que vous souhaitez utiliser l'environnement python dans ce projet vous devez éxécuter la commande de sourcing sinon vous utiliserez le python installé de manière globale sur votre machine.

## Installation des dépendances du projet

```shell
$ pip install -r requirements.txt
```

## Lancer le serveur

```shell
$ make run
```

## Troubleshooting

En cas d'erreur nous vous invitons à :

- Vous assurez que vous utilisez bien la version python de l'environnement virtuel.
- Que vous installez bien toutes les dépendances avec `pip`.


Todo: Créer une page en + pour présenter les données à côté du Dash.

## Informations sur les Dataframe et leurs traitements

### Titles, les différents shows de la plateforme (film & séries).  (`titles_df`)

```
RangeIndex: 5850 entries, 0 to 5849
Data columns (total 15 columns):
 #   Column                Non-Null Count  Dtype
---  ------                --------------  -----
 0   id                    5850 non-null   object   -> id du show
 1   title                 5849 non-null   object   -> titre du show
 2   type                  5850 non-null   object   -> type du show (film ou série)
 3   description           5832 non-null   object   -> description du show
 4   release_year          5850 non-null   int64    -> année de sortie du show
 5   age_certification     3231 non-null   object   -> age minimum pour regarder le show
 6   runtime               5850 non-null   int64    -> durée du show
 7   genres                5850 non-null   object   -> genres du show
 8   production_countries  5850 non-null   object   -> pays de production du show
 9   seasons               2106 non-null   float64  -> nombre de saisons du show
 10  imdb_id               5447 non-null   object   -> id imdb du show
 11  imdb_score            5368 non-null   float64  -> score imdb du show sur 10
 12  imdb_votes            5352 non-null   float64  -> nombre de votes imdb du show
 13  tmdb_popularity       5759 non-null   float64  -> popularité du show sur tmdb (poid, plus c'est élevé plus c'est populaire)
 14  tmdb_score            5539 non-null   float64  -> score tmdb du show sur 10
dtypes: float64(5), int64(2), object(8)
```

### Credits, les acteurs et directeurs des shows (`credits_df`)

```
RangeIndex: 77801 entries, 0 to 77800
Data columns (total 5 columns):
 #   Column     Non-Null Count  Dtype
---  ------     --------------  -----
 0   person_id  77801 non-null  int64
 1   id         77801 non-null  object
 2   name       77801 non-null  object
 3   character  68029 non-null  object
 4   role       77801 non-null  object
dtypes: int64(1), object(4)
```

### Nettoyage des données

- Aucune lignes dupliquées.
- Données nulles gardés pour la plupart des analyses car les champs manquants ne sont pas considérés.
