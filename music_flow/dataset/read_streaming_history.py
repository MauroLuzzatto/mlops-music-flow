import json
import os

import pandas as pd

from music_flow.config import dataset_settings
from music_flow.core.utils import path_data

path_raw = os.path.join(path_data, "full_history")
path_save = os.path.join(path_data, "full_history_streams.csv")


def read_streams() -> pd.DataFrame:
    """extract the streams from the StreamingHistory file

    Returns:
        pd.DataFrame: DataFrame with all streams
    """
    output = []
    for root, _, files in os.walk(path_raw):
        for file in files:
            if "Streaming_History_Audio" in file:
                output.append(os.path.join(root, file))

    full_data = []
    for file in output:
        print(file)
        with open(file, encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
        full_data.extend(data)

    df_streams = pd.DataFrame(full_data)
    df_streams.to_csv(path_save, sep=";")
    print(f"save to: {path_save}")
    return df_streams


if __name__ == "__main__":
    df = read_streams()

    df["ts"] = pd.to_datetime(df["ts"])
    print(df.shape)
    df.drop_duplicates(
        subset=[
            "ts",
            "master_metadata_track_name",
            "master_metadata_album_artist_name",
            "ms_played",
        ],
        inplace=True,
    )
    print(df.shape)

    import pandas as pd
    import duckdb

    query = """
    select
        master_metadata_track_name as track_name,
        master_metadata_album_artist_name as artist_name,
        spotify_track_uri,
        count(*) as streams,
        min(ts) as first_stream,
        max(ts) as last_stream,
        sum(ms_played) as total_play_time_ms,
    from df
    -- more than 30 sec play time
    where ms_played >= 30 * 1000
    group by 1, 2, 3
    """

    df_streams = duckdb.query(query).df()  # returns a result dataframe

    print(df_streams.head())
    df_streams.to_csv(
        os.path.join(path_data, r"new_targets.csv"), encoding="utf-8", sep="\t"
    )
