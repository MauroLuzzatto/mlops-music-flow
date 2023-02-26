import os

import pandas as pd
from xgboost import XGBRegressor  # type: ignore

from music_flow.core.utils import path, path_dataset
from music_flow.model.preprocessing import feature_preprocessing
from music_flow.model.TrainingClass import TrainingClass

path_model = os.path.join(path, "results")
path_reports = os.path.join(path, "reports")
dataset = pd.read_csv(os.path.join(path_dataset, "dataset.csv"), sep=";", index_col=0)


def limit_max_plays(max_value: int = 30) -> pd.DataFrame:
    """limit the max value of plays to max_value"""
    dataset["plays"] = dataset["plays"].apply(
        lambda row: row if row < max_value else max_value
    )
    return dataset


dataset = limit_max_plays()
dataset, columns_scope = feature_preprocessing(dataset)


columns_scope.remove("plays")
X = dataset[columns_scope]
y = dataset["plays"]

print(list(X))
print(X.describe().T)


# train model
estimator = XGBRegressor()
trainer = TrainingClass(estimator, X, y, path_model)


param_distributions = {
    "learning_rate": [0.001, 0.01, 0.1, 0.25],
    "max_depth": [3, 5, 7, 9, 11, 13, 15, 18],
    "min_child_weight": [1, 3, 5, 7, 9],
    "subsample": [0.25, 0.5, 0.8, 1.0],
    "colsample_bytree": [0.25, 0.5, 0.7],
    "n_estimators": [100, 200, 300],
    "objective": ["reg:squarederror"],
}

cv_settings = {
    "n_iter": 100,  # total combinations testes
    "scoring": "neg_mean_squared_error",
    "cv": 3,
    "random_state": 0,
    "n_jobs": -1,
    "verbose": 3,
}

trainer.train(param_distributions, cv_settings)
