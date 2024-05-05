from typing import Optional, Tuple

from music_flow.config import settings


def get_formatted_features(data: dict, is_flattened: Optional[bool] = True) -> dict:
    """format the features from the spotify api for a given track

    Args:
        data (dict): [description]
        flattened (Optional[bool], optional): [description]. Defaults to True.

    Returns:
        dict: [description]
    """
    # TODO: check that the data is valid

    try:
        features = extract_features(data)
    except KeyError as e:
        print(e)
        return {}

    if is_flattened:
        features = flatten_dict(features)

    features["metadata"] = data.get("metadata", {})

    exclude_keys = ["id_hash", "type", "uri", "track_href", "analysis_url"]
    for key in exclude_keys:
        if key in features:
            del features[key]

    features["metadata"] = data.get("metadata", {})
    return features


def extract_features(data: dict) -> dict:
    """_summary_

    Args:
        data (dict): _description_

    Returns:
        dict: _description_
    """
    features = {}
    track = data["track"]

    track_dict = {
        "track_name": data["track_name"],
        "artist_name": data["artist_name"],
        "number_of_available_markets": len(track["available_markets"]),
        "num_artists": len(track["artists"]),
        "duration_ms": track["duration_ms"],
        "explicit": track["explicit"],
        "popularity": track["popularity"],
        "isrc": track["external_ids"]["isrc"],
    }

    release_date = track["album"]["release_date"]
    year, month, day, date_is_complete = process_release_date(release_date)

    album_dict = {
        "release_date_precision": track["album"]["release_date_precision"],
        "release_year": year,
        "release_month": month,
        "release_day": day,
        "date_is_complete": date_is_complete,
        "album": track["album"]["name"],
    }

    if "artist" in data:
        artist_dict = {
            "aritist_followers": data["artist"]["followers"]["total"],
            "artist_popularity": data["artist"]["popularity"],
            "artist_genres": data["artist"]["genres"],
        }
        features["artist"] = artist_dict

    features["track"] = track_dict
    features["album"] = album_dict
    features["audio_features"] = data["audio_features"]

    if settings.INCLUDE_AUDIO_ANALYSIS_DATASET and "audio_analysis" in data:
        features["audio_analysis"] = data["audio_analysis"]

    return features


def flatten_dict(features: dict) -> dict:
    """The function flattens a nested dictionary into a single level dictionary

    Args:
        features (dict): _description_

    Returns:
        dict: _description_
    """
    features_flattend = {}
    for _, sub_value in features.items():
        for key, value in sub_value.items():
            features_flattend[key] = value
    return features_flattend


def process_release_date(release_date: str) -> Tuple[int, int, int, bool]:
    """
    extract the year, month and day from the release date

    Args:
        release_date (str): _description_

    Returns:
        Tuple[int, int, int, bool]: _description_
    """
    split_date = release_date.split("-")
    day = 1
    month = 1
    if len(split_date) == 3:
        year, month, day = split_date
        date_is_complete = True
    elif len(split_date) == 2:
        year, month = split_date
        date_is_complete = False
    else:
        year = split_date[0]
        date_is_complete = False
    return int(year), int(month), int(day), date_is_complete
