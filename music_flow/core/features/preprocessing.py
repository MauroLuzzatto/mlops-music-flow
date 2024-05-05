import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

from music_flow.config import model_settings

key_mapping = {
    0: "C",
    1: "C#/Db",
    2: "D",
    3: "D#/Eb",
    4: "E",
    5: "F",
    6: "F#/Gb",
    7: "G",
    8: "G#/Ab",
    9: "A",
    10: "A#/Bb",
    11: "B",
}


def limit_max_plays(dataset) -> pd.DataFrame:
    """limit the max value of plays to max_value"""
    dataset["plays"] = dataset["plays"].clip(upper=model_settings.MAX_PREDICTION_VALUE)
    return dataset


def get_one_hot_encoding(df, column):
    """
    convert list of features into one hot encoded values
    """
    df_one_hot = pd.get_dummies(df[column])
    df = df.drop(column, axis=1)
    df = df.join(df_one_hot)
    return df


def list_to_one_hot_encoding(df, column):
    df[column] = df[column].apply(
        lambda row: [entry.strip() for entry in row[1:-1].split(",")]
    )
    mlb = MultiLabelBinarizer()
    df_one_hot = pd.DataFrame(
        mlb.fit_transform(df.pop(column)), columns=mlb.classes_, index=df.index
    )
    df = df.join(df_one_hot)
    return df


def map_keys_to_string(key: int) -> str:
    """map keys to string

    Args:
        key (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        string_key = key_mapping[int(key)]
    except ValueError:
        string_key = "Unknown"
    return string_key


def reverse_prediction(value):
    return np.expm1(value)


def feature_preprocessing(dataset: pd.DataFrame):
    """feature preprocessing"""
    dataset = limit_max_plays(dataset)

    drop_columns = [
        "type",
        "id",
        "uri",
        "track_href",
        "analysis_url",
        "id_hash",
        "release_date",
        "isrc",
        "album",
        "track_name",
        "artist_name",
        "release_date_precision",
        "source",
        "hash",
        "error",
    ]

    columns = list(set(drop_columns) & set(list(dataset)))
    dataset.drop(columns=columns, inplace=True)

    # transformation step
    for column in [
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "plays",
    ]:
        dataset[column] = dataset[column].apply(np.log1p)

    # feature engineering
    # - us np.log1 for skewed variables like instrumentalness
    # https://www.kaggle.com/general/93016

    dataset["key"] = dataset["key"].apply(map_keys_to_string)

    dataset = get_one_hot_encoding(dataset, column="key")
    dataset = list_to_one_hot_encoding(dataset, column="artist_genres")

    all_keys = list(key_mapping.values()) + ["Unknown"]
    for col in all_keys:
        if col not in dataset:
            dataset[col] = 0

    list(dataset)
    return dataset
