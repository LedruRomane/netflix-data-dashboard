import pandas as pd
import ast
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

### DATA OPERATIONS ###


# Function return cleaned data
def get_data_title_cleaned():
    # Import data
    df_titles = pd.read_csv("./data/titles.csv")

    # Clean data, Drop rows with missing values (not much)
    if df_titles["seasons"].isnull().sum() > 0:
        df_titles["seasons"].fillna(0, inplace=True)

    df_title_cleaned = df_titles.dropna(
        subset=["imdb_id", "imdb_score", "imdb_votes", "tmdb_popularity", "tmdb_score"]
    )

    # Clean id, title, age_certification into string
    df_title_cleaned["id"] = df_title_cleaned["id"].astype(str)
    df_title_cleaned["title"] = df_title_cleaned["title"].astype(str)
    df_title_cleaned["age_certification"] = df_title_cleaned[
        "age_certification"
    ].astype(str)

    # Remode id column (not needed)
    df_title_cleaned.drop(columns=["imdb_id"], inplace=True)
    df_title_cleaned.drop(columns=["id"], inplace=True)

    return df_title_cleaned


# Function return list of genres existing in the dataset
def get_unique_genres(df):
    unique_genres = set()
    df_genres = df.copy()
    df_genres["genres"] = df["genres"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    for genres_list in df_genres["genres"]:
        unique_genres.update(genres_list)

    return sorted(list(unique_genres))


# Getters
def get_movie(df):
    df = df[df["type"] == "MOVIE"]
    return df


def get_tvshow(df):
    df = df[df["type"] == "SHOW"]
    return df


# normalize data
def normalize_df(df):
    text_fields = ["age_certification", "genres", "production_countries"]
    array_fields = ["genres", "production_countries"]

    df["type"] = df["type"].map({"MOVIE": 1, "SHOW": 0})

    # R : 17+
    # TV-MA : 17+
    # PG-13 : 13+
    # TV-14 : 14+
    # PG : 8+
    # TV-PG : 8+
    # TV-G : 7+
    # TV-Y7 : 7+
    # G : 6+
    # TV-Y : 2+
    df["age_certification"] = df["age_certification"].map(
        {
            "nan": 0,
            "TV-Y": 1,
            "G": 2,
            "TV-Y7": 3,
            "TV-G": 4,
            "TV-PG": 5,
            "PG": 6,
            "PG-13": 7,
            "TV-14": 8,
            "TV-MA": 9,
            "R": 10,
        }
    )

    df["genres"] = df["genres"].str.split(",")
    df = df.explode("genres")

    df["genres"] = df["genres"].str.replace("[", "")
    df["genres"] = df["genres"].str.replace("]", "")
    df["genres"] = df["genres"].str.replace("'", "")
    df["genres"] = df["genres"].str.replace(" ", "")

    # transform genres into integer
    genres_list = df["genres"].unique().tolist()
    genres_list = {genres_list[i]: i for i in range(0, len(genres_list))}
    df["genres"] = df["genres"].map(genres_list)

    # split production_countries : duplicate rows
    df["production_countries"] = df["production_countries"].str.split(",")
    df = df.explode("production_countries")

    df["production_countries"] = df["production_countries"].str.replace("[", "")
    df["production_countries"] = df["production_countries"].str.replace("]", "")
    df["production_countries"] = df["production_countries"].str.replace("'", "")
    df["production_countries"] = df["production_countries"].str.replace(" ", "")

    # transform production_countries into integer
    production_countries_list = df["production_countries"].unique().tolist()
    production_countries_list = {
        production_countries_list[i]: i
        for i in range(0, len(production_countries_list))
    }
    df["production_countries"] = df["production_countries"].map(
        production_countries_list
    )

    # drop rows with nan values
    df = df.dropna()

    # drop description & title columns
    df = df.drop(columns=["description", "title"])

    # Normalize data
    scaler = MinMaxScaler()
    norm = scaler.fit_transform(df)
    df = pd.DataFrame(norm, columns=df.columns)

    return df
