import os
import json


class JsonIO(object):
    """Helper class to work with json stored in a file
    """
    def __init__(self, filename):
        """Class initializer

        :param filename: string filename where from json is or will be stored
        """
        self.filename = filename

    def load(self):
        """Load and deserialize json data from the file

        :return: data object
        """
        with open(self.filename, "rb") as f:
            data = json.load(f)
        return data

    def dumps(self, data):
        """Serialize json object and save to a file

        :param data: data object
        """
        with open(self.filename, "wb") as f:
            f.write(json.dumps(data, indent=4, separators=(',', ': ')))



class LogisticRegressionJsonIO(object):
    """Helper class to work with settings stored as a json
    """
    def __init__(self, filename):
        """Class initializer

        :param filename: string filename where from json is or will be stored
        """
        self.filename = filename
        self.jsonio = JsonIO(filename)

    def save_state(self, coefs, intercept, classes):
        """Save relevant data from trained Logistic Regression object

        :param coefs: list of float coefficients
        :param intercept: list of intercept params
        :param classes: list of classes involved in training
        :return: the current instance
        """
        state = dict()
        state["coefs"] = list(coefs)
        state["intercept"] = list(intercept)
        state["classes"] = list(classes)
        self.jsonio.dumps(state)
        return self

    def get_state(self):
        """Retrieve the state of a trained Logistic Regression object

        :return: dict of 3 lists - coefs, intercept, classes
        """
        return self.jsonio.load()
