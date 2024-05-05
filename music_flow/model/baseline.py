import os

import numpy as np
import pandas as pd
from xgboost import XGBRegressor  # type: ignore

from music_flow.config import dataset_settings
from music_flow.core.features.preprocessing import feature_preprocessing
from music_flow.core.utils import create_folder, path_dataset, path_results
from music_flow.model.dataset import Dataset
from music_flow.model.evaluator import Evaluator
from music_flow.model.file_handler import save_json
from music_flow.train import columns_scope, target_column

path_dataset_file = os.path.join(path_dataset, dataset_settings.FINAL_DATASET)
dataset = pd.read_csv(path_dataset_file, sep=";", index_col=0)  # type: ignore
dataset = feature_preprocessing(dataset)

X: pd.DataFrame = dataset[columns_scope]
y: pd.Series = dataset[target_column]

print(X.describe().T)
print(type(X))

dataset = Dataset(X=X, y=y)
dataset.do_train_test_split()
X_test, y_test = dataset.get_test_data()
X_train, y_train = dataset.get_training_data()

estimator = XGBRegressor()


def baseline_model_constant_value(X_test: np.ndarray):
    """return only ones"""
    shape = (X_test.shape[0],)
    return np.zeros(shape)


def baseline_model_simple_rule(X_test: np.ndarray):
    """_summary_

    Get the popularity of a song and scale it into
    a scale between 0 and 1, then re-scale the values
    to be in the prediction range
    """
    index = columns_scope.index("popularity")
    max_value = 30
    scaled = X_test[:, index] / 100
    scale_to_predictions = scaled * max_value
    return scale_to_predictions


def baseline_model_no_tuning(X_test: np.ndarray):
    """
    Use non fine-tuned estimator to predict the values
    """
    estimator.fit(X_train, y_train)
    return estimator.predict(X_test)


# Baseline - only zeros
folder_name = "Baseline0 - zeros"
path_save = create_folder(os.path.join(path_results, folder_name))

y_pred = baseline_model_constant_value(X_test)
print(y_pred.shape, y_test.shape)
evaluator = Evaluator(y_test=y_test, y_pred=y_pred)
score_dict = evaluator.evaluate()
save_json(name="score_dict.json", data=score_dict, path=path_save)
evaluator.visualize(path_save=path_save)


# Baseline 1 - simple rule
folder_name = "Baseline1 - simple rule"
path_save = create_folder(os.path.join(path_results, folder_name))

y_pred = baseline_model_simple_rule(X_test)
evaluator = Evaluator(y_test=y_test, y_pred=y_pred)
score_dict = evaluator.evaluate()
save_json(name="score_dict.json", data=score_dict, path=path_save)
evaluator.visualize(path_save=path_save)

# Baseline 2 - no-hyperparamter tuning
folder_name = "Baseline2 - no hyperparamter tuning"
path_save = create_folder(os.path.join(path_results, folder_name))

y_pred = baseline_model_no_tuning(X_test)
evaluator = Evaluator(y_test=y_test, y_pred=y_pred)
score_dict = evaluator.evaluate()
save_json(name="score_dict.json", data=score_dict, path=path_save)
evaluator.visualize(path_save=path_save)
