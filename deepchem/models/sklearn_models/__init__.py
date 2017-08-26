"""
Code for processing datasets using scikit-learn.
"""
import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import LassoLarsCV
from deepchem.models import Model
from deepchem.utils.save import load_from_disk
from deepchem.utils.save import save_to_disk

NON_WEIGHTED_MODELS = {LogisticRegression, PLSRegression, GaussianProcessRegressor, ElasticNetCV, LassoCV}


class SklearnModel(Model):
  """
  Abstract base class for different ML models.
  """

  def fit(self, dataset, **kwargs):
    """
    Fits SKLearn model to data.
    """
    X = dataset.X
    y = np.squeeze(dataset.y)
    w = np.squeeze(dataset.w)
    # Logistic regression doesn't support weights
    for model_instance in NON_WEIGHTED_MODELS:
      if not isinstance(self.model_instance, model_instance):
        continue
      self.model_instance.fit(X, y)
      return
    self.model_instance.fit(X, y, w)

  def predict_on_batch(self, X, pad_batch=False):
    """
    Makes predictions on batch of data.

    Parameters
    ----------
    X: np.ndarray
      Features
    pad_batch: bool, optional
      Ignored for Sklearn Model. Only used for Tensorflow models
      with rigid batch-size requirements.
    """
    return self.model_instance.predict(X)

  def predict_proba_on_batch(self, X, pad_batch=False):
    """
    Makes per-class predictions on batch of data.

    Parameters
    ----------
    X: np.ndarray
      Features
    pad_batch: bool, optional
      Ignored for Sklearn Model. Only used for Tensorflow models
      with rigid batch-size requirements.
    """
    return self.model_instance.predict_proba(X)

  def predict(self, X, transformers=[]):
    """
    Makes predictions on dataset.
    """
    return super(SklearnModel, self).predict(X, transformers)

  def save(self):
    """Saves sklearn model to disk using joblib."""
    save_to_disk(self.model_instance, self.get_model_filename(self.model_dir))

  def reload(self):
    """Loads sklearn model from joblib file on disk."""
    self.model_instance = load_from_disk(Model.get_model_filename(self.model_dir))

  def get_num_tasks(self):
    """Number of tasks for this model. Defaults to 1"""
    return 1
