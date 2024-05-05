from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split  # type: ignore

from music_flow.config import dataset_settings
from music_flow.dataset import __version__ as data_version


class Dataset:
    def __init__(self, X, y) -> None:
        self.column_names = list(X)

        self.X = X.values if isinstance(X, pd.DataFrame) else X
        self.y = y.values if isinstance(y, pd.DataFrame) else y

        self.test_size = dataset_settings.test_size
        self.random_state = dataset_settings.random_state

        # TODO: fix me
        self.data_version = data_version

        self.X_train: np.ndarray
        self.X_test: np.ndarray
        self.y_train: np.ndarray
        self.y_test: np.ndarray

    def do_train_test_split(self) -> None:
        """
        Get the train and test split of the features and target values
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(  # type: ignore
            self.X, self.y, random_state=self.random_state, test_size=self.test_size
        )

    def get_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.X_train, self.y_train

    def get_test_data(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.X_test, self.y_test

    def get_data_log(self) -> dict:
        # rewrite logger statements into a dict
        data_log = {
            "X": self.X.shape,
            "y": self.y.shape,
            "X_train": self.X_train.shape,  # type: ignore
            "y_train": self.y_train.shape,  # type: ignore
            "X_test": self.X_test.shape,  # type: ignore
            "y_test": self.y_test.shape,  # type: ignore
            "test_size": self.test_size,
            "random_state": self.random_state,
            "data_version": self.data_version,
        }
        return data_log

    def get_data_version(self):
        return self.data_version

    def get_column_names(self):
        return self.column_names
