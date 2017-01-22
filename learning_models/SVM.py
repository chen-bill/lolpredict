import dataRepository
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle

from sklearn import svm, preprocessing, cross_validation
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction import DictVectorizer

scaler = MinMaxScaler()

df = dataRepository.getFullDataframe()
dfX = df.drop('bWin', axis=1)

X = scaler.fit_transform(dfX)
y = np.array(df['bWin'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#poly, sigmoid kernel sucks
clf = svm.SVC(kernel='linear', verbose=1, probability=True)
clf.fit(X_train, y_train)

print clf

#used to debugging purposes
def test():
    print ('predict_probaion 0')
    # print (X_test[0])
    print (y_test[0])
    print (clf.predict_proba(X_test[0]))

    print ('predict_probaion 1')
    # print (X_test[1])
    print (y_test[1])
    print (clf.predict_proba(X_test[1]))

    print ('predict_probaion 2')
    # print (X_test[2])
    print (y_test[2])
    print (clf.predict_proba(X_test[2]))

    print ('predict_probaion 3')
    # print (X_test[3])
    print (y_test[3])
    print (clf.predict_proba(X_test[3]))

    print ('predict_probaion 4')
    # print (X_test[4])
    print (y_test[4])
    print (clf.predict_proba(X_test[4]))

    print ('predict_probaion 5')
    # print (X_test[5])
    print (y_test[5])
    print (clf.predict_proba(X_test[5]))

    print ('predict_probaion 6')
    # print (X_test[6])
    print (y_test[6])
    print (clf.predict_proba(X_test[6]))

    print ('predict_probaion 7')
    # print (X_test[7])
    print (y_test[7])
    print (clf.predict_proba(X_test[7]))

print ('Score: ')
print (clf.score(X_test, y_test))
# test()

print ('end of program')

