# Analyse du jeux de données Netflix (TUDUM)

<table style="margin: auto;">
    <tr>
        <td><img src="doc/netflix.png" alt="Netflix Logo" width="250" /></td>
        <td><img src="doc/lyon1.png" alt="Lyon 1 logo" width="250" /></td>
    </tr>
</table>


2. [Pré-ambule](#pré-ambule)
3. [Description des jeux de données](#description-des-jeux-de-données-)
   - [Fichier des films/séries (`data/titles.csv`)](#fichier-des-filmsséries-datatitlescsv)
   - [Fichier des acteurs/réalisateurs (`data/credits.csv`)](#fichier-des-acteursréalisateurs-datacreditscsv)
4. [Mise en place de l'environnement](#mise-en-place-de-l'environnement)
   - [Pré-requis](#pré-requis)
   - [Mise en place de l'environnement virtuel `venv`](#mise-en-place-de-l'environnement-virtuel-venv)
     - [Création de l'environnement virtuel](#création-de-l'environnement-virtuel)
     - [Source de ce dernier](#source-de-ce-dernier)
5. [Installation des dépendances du projet](#installation-des-dépendances-du-projet)
6. [Lancer le serveur](#lancer-le-serveur)
7. [Troubleshooting](#troubleshooting)
8. [Informations sur les Dataframe et leurs traitements](#informations-sur-les-dataframe-et-leurs-traitements)
   - [Titles, les différents shows de la plateforme (film & séries)](#titles-les-différents-shows-de-la-plateforme-film-&-séries)
   - [Credits, les acteurs et directeurs des shows](#credits-les-acteurs-et-directeurs-des-shows)
9. [Nettoyage des données](#nettoyage-des-données)

# Pré-ambule

L'application est accessible [ici](http://51.38.178.218:8090) (merci à @Romane)

## Etudiants

| Nom                 | Prénom | Numéros Etudiants |
|---------------------|--------|-------------------|
| CECILLON            | Enzo   | 11805901          |
| LEDRU               | Romane | 22105081          |
| COUTURIER-PETRASSON | Claire | 11710714          |

## Description des jeux de données 📄

**Aperçu du jeu de données :**

- un fichier `data/titres.csv` comprenant 5 000 titres uniques disponibles sur Netflix (films/séries) dont 15 colonnes détaillant divers aspects de chaque titre.
- un fichier `data/credits.csv` avec plus de 77 000 entrées pour les acteurs et les réalisateurs, comprenant 5 colonnes.

### Fichier des films/séries (`data/titles.csv`)

| Colonne               | Description de la donnée (Français)                     |
|-----------------------|---------------------------------------------------------|
| id                    | L'identifiant du titre                                   |
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
| person_ID       | L'identifiant de la personne.                        |
| id              | L'identifiant du titre.                              |
| name            | Le nom de l'acteur ou du réalisateur.               |
| character_name  | Le nom du personnage.                               |
| role            | Rôle : ACTEUR ou RÉALISATEUR.                       |

## Mise en place de l'environnement

### Pré-requis

- python >= 3.11
- pip

### Mise en place de l'environnement virtuel `venv`

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

### Titles, les différents shows de la plateforme (film & séries)

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

### Credits, les acteurs et directeurs des shows

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

## Nettoyage des données

- Aucune lignes dupliquées.
- Données nulles gardés pour la plupart des analyses car les champs manquants ne sont pas considérés.

## Analyse des données

### Durée moyenne d'un film ou d'un épisode de série

#### Durée moyenne d'un épisode de séries Netflix par an
Pour certains genre (ex: documentaires), la durée moyenne d'un épisode de série ne varie pratiquement pas au fil des décennies. En revanche, certains genres changent énormément:

- l'animation fait un bond au milieu des années 90. La durée moyenne d'un épisode est presque doublée. On constate une légère baisse autour de 2010 puis une augmentation constante, probablement grâce aux nouvelles technologies.

- Pour tous les autres genres, on voit une augmentation progressive de la durée moyenne d'un épisode, ce qui peut s'expliquer par la généralisation de la télévision dans les foyers puis à partir des années 2010 par l'essort des plateformes de streaming, qui promeuvent en particuliers les séries.

Les séries ont plus de budget et sont plus populaires auprès du grand public. Certaines se rapprochent davantage du court ou moyen métrage. 

#### Durée moyenne des films Netflix par an
La durée moyenne d'un film, à l'inverse, stagne voir semble diminuer.

### Moyenne des notes TMDb et IMDb
A noter :
- Les utilisateurs de Tmdb mettent en moyenne des notes plus élevées que les utilisateurs d'IMDb.
- les pics descendants sur le graphe linéaires correspondent à une absence de données.

#### Moyenne des notes des films les plus appréciés par an
Excepté pour le sport et l'horreur (baisse puis notes constantes après 1996), on constate une baisse générale des notes moyennes attribuées aux films à partir de la fin des années 90.
Cela peut s'expliquer par l'augmentation du nombre de films produits par an et la multiplicité des spectateurs qui prennent le temps de noter les films.

#### Moyenne des notes des séries les plus appréciés par an (source TMDb et IMDb)
On constate également une baisse générale des notes de séries, même si elle est moins importante que pour les films.

### Evolution de la production de films et séries Netflix dans les 10 pays les plus producteurs
Le rendu du graphe n'est pas totalement conforme à ce que nous voulions montrer car la préparation des données pour ce graphe s'est révélée plus complexe que prévu. Le problème principal a été le filtre sur les 10 pays les plus producteurs de films et séries. En effet, chaque titre peut avoir un ou plusieurs pays de production ce qui rend la combinaison avec les années beaucoup plus compliqué car cela génère des tuples plutôt que des identifiant uniques pour chaque titre. Nous ne sommes pas parvenu à résoudre ce problème dans le temps imparti.

Le graphe permet néanmoins de voir l'évolution de la production de films et séries dans la plupart des pays. On voit notamment que les US sont très au-dessus des autres, avec plus de 200 films et séries produits à partir de 2017. Entre 2018 et 2020, cela réprensente une production 3,5 supérieure à celle de l'Inde, 2e du classement. 
Si on regarde indépendamment la production de films et de séries, on voit que c'est la production de films qui influe le plus sur le classement puisque ce sont les US et l'Inde qui en produisent le plus, avec des nombres bien supérieurs à ceux des autres pays. 
Les US restent également en tête pour les séries mais les disparités sont moins fortes entre les autres pays. On voit notamment l'émergence des séries Japonaises (Jdrama) et Coréennes (Kdrama), toujours plus populaires auprès du grand public.
