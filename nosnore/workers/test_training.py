import numpy as np
from sklearn import linear_model
from sklearn.preprocessing.label import LabelEncoder

from nosnore.storage.db import SnoreDatabase
from nosnore.storage.jsonio import LogisticRegressionJsonIO

# restore logistic regression object
logreg = linear_model.LogisticRegression()
io = LogisticRegressionJsonIO("nosnore/data/logistic_regression.json")
state = io.get_state()

logreg.coef_ = np.array([state["coefs"]])
logreg.intercept_ = np.array(state["intercept"])
logreg._enc = LabelEncoder()
logreg._enc.classes_ = np.array(state["classes"])

# extract testing samples
db = SnoreDatabase("pcp_features.db")
samples_pos = db.get_features()[2500:]
samples_pos = [list(i[2:]) for i in samples_pos]
db.db.close()

db = SnoreDatabase("negative_features.db")
samples_neg = db.get_features()[2500:]
samples_neg = [list(i[2:]) for i in samples_neg]
db.db.close()

samples = samples_pos + samples_neg
print "Total of {0} samples".format(len(samples))
true_labels = [1]*len(samples_pos) + [0]*len(samples_neg)

predicted_labels = logreg.predict(samples)
predicted_probs = logreg.predict_proba(samples)
accuracy = list(predicted_labels == true_labels)

print "There are {0} correctly labeled samples".format(accuracy.count(True))
print "There are {0} incorrectly labeled samples".format(accuracy.count(False))

print "{0}% accuracy".format(float(accuracy.count(True)) / float(len(samples)) * 100.0)
