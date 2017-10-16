from sklearn import datasets

import pandas as pd

from sklearn.naive_bayes import BernoulliNB
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.naive_bayes import MultinomialNB
import operator
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.linear_model import PassiveAggressiveClassifier
#np.random.seed(123)

from sklearn import linear_model


# print('5-fold cross validation:\n')

# for clf, label in zip([clf1, clf2, clf3], ['Logistic Regression', 'Random Forest', 'naive Bayes']):
# 
#     scores = cross_validation.cross_val_score(clf, X, y, cv=5, scoring='accuracy')
#     print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
data = pd.read_csv('/tmp/lixo99922', header=None)
  
X = data.values[:, 1:10]
y = data.iloc[:, 11]
print (y)




class EnsembleClassifier(BaseEstimator, ClassifierMixin):
         
        
    """
    Ensemble classifier for scikit-learn estimators.

    Parameters
    ----------

    clf : `iterable`
      A list of scikit-learn classifier objects.
    weights : `list` (default: `None`)
      If `None`, the majority rule voting will be applied to the predicted class labels.
        If a list of weights (`float` or `int`) is provided, the averaged raw probabilities (via `predict_proba`)
        will be used to determine the most confident class label.

    """
    def __init__(self, weights=None):
        
        self.weights = weights
        self.clf1 =ExtraTreesClassifier()
        self.clf2 =PassiveAggressiveClassifier()
        self.clf3=SVC(probability=True, kernel='linear')
#         self.clf1 = LogisticRegression()
#         self.clf2 = ExtraTreesClassifier()
#         self.clf3 = SVC(probability=True, kernel='rbf')
        self.clfs = [self.clf1,self.clf2,self.clf3]
   
    
    def fit(self, X, y):
        """
        Fit the scikit-learn estimators.

        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]
            Training data
        y : list or numpy array, shape = [n_samples]
            Class labels

        """
        for clf in self.clfs:
            clf.fit(X, y)
           # print("fitting classifier")

    def predict(self, X):
        """
        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]

        Returns
        ----------

        maj : list or numpy array, shape = [n_samples]
            Predicted class labels by majority rule

        """
        maj=[0]*len(X)
        final=[0]*len(X)
        self.classes_ = np.asarray([clf.predict(X) for clf in self.clfs])
        if self.weights:
            avg = self.predict_proba(X)
            
            #maj = np.apply_along_axis(lambda x: max(enumerate(x), key=operator.itemgetter(1))[0], axis=1, arr=avg)

        else:
            maj = np.asarray([np.argmax(np.bincount(self.classes_[:,c])) for c in range(self.classes_.shape[1])])
        #print [sum(x) for x in zip(*a)]
        
        #maj.sum(axis=1)
        return avg,self.probas_

    def predict_proba(self, X):

        """
        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]

        Returns
        ----------

        avg : list or numpy array, shape = [n_samples, n_probabilities]
            Weighted average probability for each class per sample.

        """
        self.probas_ = [clf.predict(X) for clf in self.clfs]
        avg = np.average(self.probas_, axis=0, weights=self.weights)
        #print ("assemble avg" + str(avg));
        return avg

#np.random.seed(123)

#for clf, label in zip([clf1, clf2, clf3, eclf], ['Logistic Regression', 'Random Forest', 'naive Bayes', 'Ensemble']):

#    scores = cross_validation.cross_val_score(clf, X, y, cv=5, scoring='f1')
#    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))


