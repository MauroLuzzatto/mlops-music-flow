import json
import logging
import os
import time
from pprint import pprint
import numpy as np

import pandas as pd

from music_flow.config import dataset_settings
from music_flow.core.batch_spotify_api import BatchSpotifyAPI
from music_flow.core.features.get_raw_features import get_track_id
from music_flow.core.utils import (
    path_data,
)

logger = logging.getLogger(__name__)

path_target_values = os.path.join(path_data, dataset_settings.TARGERT_VALUES)
path_data_lake_failed = r"/Users/mauroluzzatto/Documents/python_scripts/track-recommender/data_lake_v3/failed"
path_data_lake_success = r"/Users/mauroluzzatto/Documents/python_scripts/track-recommender/data_lake_v3/success"


from music_flow.core.features.tracker import Tracker
from dataclasses import dataclass


@dataclass
class DataPoint:
    track_id: str
    artist_id: str
    data: dict


def download_audio_features_batch(is_retry_failed_files: bool = False) -> bool:
    """
    This function will download the audio features from the spotify API and store them in a json file.
    The json file will be stored in the path_data_lake folder.

    Args:
        is_retry_failed_files (bool): indicate if failed files should be retired or not

    Returns:
        bool: has_finished
    """
    df = pd.read_csv(path_target_values, sep=";")
    files_failed_set = set(os.listdir(path_data_lake_failed))
    number_of_files_failed = len(os.listdir(path_data_lake_failed))

    files_set = set(os.listdir(path_data_lake_success))
    number_of_files_success = len(os.listdir(path_data_lake_success))

    num_missing = len(df) - number_of_files_failed - number_of_files_success

    print(f"Files missing: {num_missing}")

    success = 0.000001
    failed = 0

    start_time = time.time()

    batch = BatchSpotifyAPI()

    def chunker(seq, size):
        return (seq[pos : pos + size] for pos in range(0, len(seq), size))

    for chunk in chunker(df, 50):
        data_points = []
        for index, row in chunk.iterrows():
            if index % 1_000 == 0:  # type: ignore
                print(f"{index}/{len(df)}")

            track_name: str = row["track_name"]
            artist_name: str = row["artist_name"]
            hash: str = row["hash"]
            filename: str = f"{hash}.json"
            if (
                (filename in files_set) or (filename in files_failed_set)
            ) or is_retry_failed_files:
                continue

            data = {
                "track_name": track_name,
                "artist_name": artist_name,
                "hash": hash,
                "filename": filename,
            }

            try:
                tracker = Tracker(name=track_name, artist=artist_name)
                track_id = tracker.track_id
                artist_id = tracker.artist_id
            except Exception as e:
                print(e)
                track_id = None
                artist_id = None

            if not (track_id or artist_id):
                failure_dict = {
                    "status": "failed",
                    "failure_type": "search_track_url",
                    "track_id": None,
                }
                data.update(failure_dict)
                failed += 1
                save_dict_to_json(data, path_data_lake_failed, data["filename"])
                continue

            data_point = DataPoint(track_id, artist_id, data)
            data_points.append(data_point)

        track_ids = [data_point.track_id for data_point in data_points]
        artist_ids = [data_point.artist_id for data_point in data_points]

        if not track_ids:
            continue

        response, _ = batch.get_batch_audio_features(track_ids)
        audio_features_dict = batch.convert_batch_response_to_dict(
            response["audio_features"]
        )
        response, _ = batch.get_batch_tracks(track_ids)
        tracks_dict = batch.convert_batch_response_to_dict(response["tracks"])

        response, _ = batch.get_batch_artists(artist_ids)
        artists_dict = batch.convert_batch_response_to_dict(response["artists"])

        for data_point in data_points:
            track_id = data_point.track_id
            artist_id = data_point.artist_id
            data = data_point.data

            # we are doing an all or nothing approach here
            try:
                data["audio_features"] = audio_features_dict[track_id]
                data["artist"] = artists_dict[artist_id]
                data["track"] = tracks_dict[track_id]
                data["status"] = "success"
            except Exception as e:
                data["status"] = "failed"
                print(e)

            if data["status"] == "success":
                save_dict_to_json(data, path_data_lake_success, data["filename"])
                success += 1
            else:
                # save_dict_to_json(data, path_data_lake_failed, data["filename"])
                failed += 1
                # logger.debug(f"{data}")
                # print(status_code)
                pprint(data)

        end_time = time.time()
        print(f"Success: {int(success)}, Failed: {failed}, Ratio: {failed/success:.2f}")
        print(f"--> Elapsed time: {(end_time -start_time)/60:.2f} min")

        # if success > 150 and failed / success > 5.0:
        #     raise Exception("Too many failed requests")

    return True


def save_dict_to_json(data: dict, path: str, filename: str):
    """save data to json file

    Args:
        data (dict): _description_
        path (str): _description_
        filename (str): _description_
    """
    assert filename.endswith(".json"), "filename must be a json file"

    with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(max_retries=5):
    download_audio_features_batch()

    # while retries < max_retries:
    #     try:
    #         has_finished = download_audio_features_batch()
    #     except Exception as e:
    #         print(e)
    #         time.sleep(60 * 3)

    #     retries += 1
    #     if has_finished:
    #         break


if __name__ == "__main__":
    main()
