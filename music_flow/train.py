import os

import pandas as pd
from xgboost import XGBRegressor  # type: ignore

from music_flow.__init__ import __version__ as model_version
from music_flow.config import dataset_settings, settings
from music_flow.core.features.preprocessing import feature_preprocessing
from music_flow.core.model_registry import ModelRegistry
from music_flow.core.utils import path_dataset, path_results
from music_flow.model.dataset import Dataset
from music_flow.model.trainer import Trainer

# move to settings
param_distributions = {
    "learning_rate": [0.001, 0.01, 0.1, 0.25],
    "max_depth": [3, 5, 7, 9, 11, 13, 15, 18],
    "min_child_weight": [1, 3, 5, 7, 9],
    "subsample": [0.25, 0.5, 0.8, 1.0],
    "colsample_bytree": [0.25, 0.5, 0.7],
    "n_estimators": [100, 200],
    "objective": ["reg:squarederror"],
}
# move to settings
cv_settings = {
    "n_iter": 50,  # 100 total combinations testes
    "scoring": "neg_mean_squared_error",
    "cv": 3,
    "random_state": 0,
    "n_jobs": -1,
    "verbose": 3,
}


path_dataset_file = os.path.join(path_dataset, dataset_settings.FINAL_DATASET)
dataset = pd.read_csv(path_dataset_file, sep=";", index_col=0)  # type: ignore
dataset = feature_preprocessing(dataset)

# move to settings
# add datatype to settings
target_column = "plays"
columns_scope = [
    "number_of_available_markets",
    "num_artists",
    "duration_ms",
    "explicit",
    "popularity",
    "release_year",
    "release_month",
    "release_day",
    "date_is_complete",
    "danceability",
    "energy",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature",
    "A",
    "A#/Bb",
    "B",
    "C",
    "C#/Db",
    "D",
    "D#/Eb",
    "E",
    "F",
    "F#/Gb",
    "G",
    "G#/Ab",
    "Unknown",
]

dataset.sample(frac=1, random_state=42)
X: pd.DataFrame = dataset[columns_scope]
y: pd.Series = dataset[target_column]

# y = np.log1p(y)

print(X.describe().T)
print(type(X))

dataset = Dataset(X=X, y=y)
dataset.do_train_test_split()
data_log = dataset.get_data_log()
print(data_log)

estimator = XGBRegressor()

trainer = Trainer(
    estimator=estimator,
    dataset=dataset,
    model_version=model_version,
    path_model=path_results,
)

trainer.train(param_distributions, cv_settings)

upload = False
if upload:
    registry = ModelRegistry(bucket_name=settings.BUCKET_NAME)
    registry.upload_folder(trainer.folder_name)
