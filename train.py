import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
#from sklearn.externals import joblib
import pickle

names = [
    "Nearest_Neighbors",
    "Linear_SVM",
    "RBF_SVM",
    "Gaussian_Process",
    "Decision_Tree",
    "Random_Forest",
    "Neural_Net",
    "AdaBoost",
    "Naive_Bayes",
    "QDA",
]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis(),
]

f = open('dataset', 'r', encoding='utf-8')
lines = f.readlines()
features, target = [], []
for ll in lines:
    if ll.find('##') != -1:
        continue
    l = ll.strip().split(' ')
    if len(l)>0:
        features.append(l[1:-1])
        target.append(l[-1])
X = np.asarray(features)
y = np.asarray(target)
#print(features[212:215]+features[190:206])
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42)
X_exam = StandardScaler().fit_transform(np.asarray(features[213:215]+features[190:206]))
y_exam = np.asarray(target[213:215]+target[190:206])
for name, clf in zip(names, classifiers):
        clf.fit(X_train, y_train)
        score = cross_val_score(clf, X_test, y_test, cv=5, scoring='accuracy').mean()
        print('privacy of '+name+': '+str(score))
        print(clf.get_params())
        print(clf.predict(X_exam))
        print(y_exam)
        with open('save/'+name+'.pickle', 'wb') as fm:
            pickle.dump(clf, fm)