# Analyse-De-Donnees-Netflix

Todo: Créer une page en + pour présenter les données à côté du Dash.

1. Présenter les données.


Deux jeux de données joints :

Titles, les différents shows de la plateforme (film & séries).
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

Credits, les acteurs et directeurs des shows.
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

2. Clean les données.

- Aucune lignes dupliquées.
- Données nulles probablement à garder compte tenu de l'importance du champs correspondant (ex: pas de description pour un show).