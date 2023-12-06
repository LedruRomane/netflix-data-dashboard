import pandas as pd
import ast

### DATA OPERATIONS ###

# Function return cleaned data
def get_data_title_cleaned(): 
    # Import data
    df_titles = pd.read_csv('./data/titles.csv')

    # Clean data, Drop rows with missing values (not much)
    if (df_titles['seasons'].isnull().sum() > 0):
        df_titles['seasons'].fillna(0, inplace=True)

    df_title_cleaned =df_titles.dropna(subset=['imdb_id','imdb_score','imdb_votes','tmdb_popularity','tmdb_score'])

    # Clean id, title, age_certification into string
    df_title_cleaned['id'] = df_title_cleaned['id'].astype(str)
    df_title_cleaned['title'] = df_title_cleaned['title'].astype(str)
    df_title_cleaned['age_certification'] = df_title_cleaned['age_certification'].astype(str)

    # Remode id column (not needed)
    df_title_cleaned.drop(columns=['imdb_id'], inplace=True)
    df_title_cleaned.drop(columns=['id'], inplace=True)

    return df_title_cleaned

# Function return list of genres existing in the dataset
def get_unique_genres(df):
    unique_genres = set()
    df_genres = df.copy()
    df_genres['genres'] = df['genres'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    for genres_list in df_genres['genres']:
        unique_genres.update(genres_list)

    return sorted(list(unique_genres))

# Getters
def get_movie(df):
    df = df[df['type'] == 'MOVIE']
    return df

def get_tvshow(df):
    df = df[df['type'] == 'SHOW']
    return df