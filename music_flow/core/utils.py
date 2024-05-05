import hashlib
import json
import os


def create_folder(path: str) -> str:
    """
    create folder, if it doesn't already exist
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")
    except OSError:
        print(f"Error: Creating directory: {path}")
    return path


def get_hash(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def read_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


path = os.getcwd()
path_base = os.path.join(path, "music_flow")

path_results = os.path.join(path, "results")
path_registry = os.path.join(path, "registry")
path_reports = os.path.join(path, "reports")

path_data_lake = os.path.join(path, "data_lake_v3")

path_data_lake_success = os.path.join(path_data_lake, "success")
path_data_lake_failed = os.path.join(path_data_lake, "failed")

path_data = os.path.join(path, "data")
path_features = os.path.join(path_data, "features")
path_dataset = os.path.join(path_data, "dataset")
path_raw = os.path.join(path_data, "raw")

path_env = os.path.join(path, ".env")
path_app = os.path.join(path, "app")
