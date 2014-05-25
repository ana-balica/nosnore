import numpy as np
from sklearn import linear_model
from sklearn.preprocessing.label import LabelEncoder

from nosnore.io.db import SnoreDatabase
from nosnore.io.jsonio import LogisticRegressionJsonIO


db = SnoreDatabase("pcp_features.db")
samples_pos = db.get_features()
samples_pos = [list(i[2:]) for i in samples_pos]
db.db.close()

db= SnoreDatabase("negative_features.db")
samples_neg = db.get_features(len(samples_pos))
samples_neg = [list(i[2:]) for i in samples_neg]

samples = samples_pos + samples_neg
labels = [1]*len(samples_pos) + [0]*len(samples_neg)

logreg = linear_model.LogisticRegression()
logreg.fit(samples, labels)

io = LogisticRegressionJsonIO("nosnore/data/logistic_regression.json")
io.save_state(logreg.coef_[0], logreg.intercept_, logreg._enc.classes_)
