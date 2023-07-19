import time
import pandas as pd

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from dara.core import ProgressUpdater, track_progress


@track_progress
def grid_search(data: pd.DataFrame, kernels: list, c_list: list, gamma_list: list, updater: ProgressUpdater):
    """
    Runs a grid search over a set of hyperparameters for a Support Vector Machine.

    :param data: DataFrame hosting the data in question
    :param kernels: list of options for SVM kernel values
    :param c_list: list of options for SVM C values
    :param gamma_list: list of options for SVM gamma values
    :param updater (from @track_progress injection): a ProgressUpdater to send progress updates to the frontend
    :return: tuple of truth and prediction arrays
    """
    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['species']), data['species'], test_size=0.30)
    best_model, best_score = None, 0
    for i, kernel in enumerate(kernels):
        for c in c_list:
            for gamma in gamma_list:
                model = svm.SVC(C=float(c), kernel=kernel, gamma=float(gamma))
                model.fit(X_train, y_train)
                pred = model.predict(X_test)
                score = accuracy_score(y_test, pred)
                if score > best_score:
                    best_score = score
                    best_model = model
        time.sleep(1)
        updater.send_update((i / len(kernels)) * 100, f'Step {i}')
    updater.send_update(100, 'Done')
    return (y_test, best_model.predict(X_test))
