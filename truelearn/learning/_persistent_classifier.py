from __future__ import annotations

from ._base_classifier import BaseClassifier
from truelearn.models import EventModel


class PersistentClassifier(BaseClassifier):
    """A classifier that makes predictions based on whether the learner has engaged with the last learnable unit.

    Methods
    -------
    fit(x, y)
        Train the model based on the given event and label.
    predict(x)
        Predict whether the learner will engage in the given learning event.
    predict_proba(x)
        Predict the probability of learner engagement in the given learning event.

    Properties
    ----------
    engage_with_last

    """

    def __init__(self) -> None:
        super().__init__()

        self.__engage_with_last = False

    def fit(self, _x: EventModel, y: bool) -> PersistentClassifier:
        """Train the model based on the given event and labels.

        Parameters
        ----------
        _x : EventModel
            A representation of a learning event.
        y: bool
            A label that is either True or False.

        Returns
        -------
        PersistentClassifier
            The updated model.

        Notes
        -----
        Given the nature of this classifier, the input _x is not used.

        """
        self.__engage_with_last = y
        return self

    def predict(self, _x: EventModel) -> bool:
        """Predict whether the learner will engage in the given learning event.

        Parameters
        ----------
        _x : EventModel
            A representation of a learning event.

        Returns
        -------
        bool
            Whether the learner will engage in the given learning event.

        Notes
        -----
        Given the nature of this classifier, the input _x is not used.

        """
        return self.__engage_with_last

    def predict_proba(self, _x: EventModel) -> float:
        """Predict the probability of learner engagement.

        Parameters
        ----------
        _x : EventModel
            A representation of a learning event.

        Returns
        -------
        float
            The probability that the learner will engage in the given learning event.

        Notes
        -----
        Given the nature of this classifier, the input _x is not used.

        """
        return float(self.__engage_with_last)

    @property
    def engage_with_last(self) -> bool:
        """Return whether the learner engage with the last learnable unit.

        Returns
        -------
        bool
            Whether the learner engage with the last learnable unit.

        """
        return self.__engage_with_last
