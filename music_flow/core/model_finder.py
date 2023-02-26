import os
from typing import List, Optional

from music_flow.core.utils import path_results
from music_flow.file_handling import load_json

default_max = 1_000_000
default_min = 0


def get_latest_folder(folders: List[str]) -> str:
    """
    Returns the latest folder in the results folder

    Returns:
        str: _description_
    """

    folders.sort()
    try:
        return folders[-1]
    except IndexError:
        raise FileNotFoundError("No folder found")


def get_best_score_folder(folders: List[str], metric: Optional[str]) -> str:
    """
    Returns the folder with the best score for a given metric

    Args:
        metric (str): name of the metric to use

    Raises:
        ValueError: _description_
        FileNotFoundError: _description_

    Returns:
        str: _description_
    """

    metrics = {
        "r2_score": ("higher", default_min),
        "mean_absolute_error": ("lower", default_max),
        "mean_squared_error": ("lower", default_max),
        "mean_absolute_percentage_error": ("lower", default_max),
    }

    if not metric:
        raise ValueError(f"Metric not specified - options: {metrics.keys()}")

    direction, max_score = metrics[metric]
    best_folder = None
    for folder in folders:
        try:
            path = os.path.join(path_results, folder, "results", "best_score.json")
            data = load_json(path)
        except FileNotFoundError:
            continue
        score = data["score"][metric]
        if direction == "higher" and score > max_score:
            max_score = score
            best_folder = folder
        elif direction == "lower" and score < max_score:
            max_score = score
            best_folder = folder

    if best_folder is None:
        raise FileNotFoundError("No best score file found")

    return best_folder


def get_model_folder(
    mode: str = "latest", metric: Optional[str] = None, path: Optional[str] = None
) -> str:
    """_summary_

    Args:
        mode (str, optional): _description_. Defaults to "latest".
        metric (Optional[str], optional): _description_. Defaults to None.
        path (Optional[str], optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """

    if path is None:
        path = path_results

    folders = os.listdir(path)

    if mode == "latest":
        folder = get_latest_folder(folders)
    elif mode == "best_score":
        folder = get_best_score_folder(folders, metric)
    else:
        raise ValueError("Mode not found - options: latest, best_score")
    return folder


if __name__ == "__main__":
    folder = get_model_folder()
    folder = get_model_folder(metric="r2_score", mode="best_score")