import pandas as pd


def clean_titles(): 

    df_titles = pd.read_csv('./data/titles.csv')
    if (df_titles['seasons'].isnull().sum() > 0):
        df_titles['seasons'].fillna(0, inplace=True)
    df_title_cleaned =df_titles.dropna(subset=['imdb_id','imdb_score','imdb_votes','tmdb_popularity','tmdb_score'])

    return df_title_cleaned

