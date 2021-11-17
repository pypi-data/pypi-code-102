from arff2pandas import a2p
from idict import idict
from pandas import read_csv, DataFrame
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import fetch_openml


def Dataset(name="wdbc"):
    return idict(dataset(name))


def dataset(name="wdbc"):
    X, y = fetch_openml(name, return_X_y=True)
    return {"X": X, "y": y}


def File(name="iris.arff"):
    return idict(file(name))


def file(name="iris.arff"):
    if name.endswith(".arff"):
        with open(name) as f:
            return {"df": a2p.load(f)}
    elif name.endswith(".csv"):
        return {"df": read_csv(name)}


# def save(name=None):
# DataFrame({
#     'power@NUMERIC':[0.5,0.2],
#     'label@{good,bad}':['good','bad']
# })
# with open('sample.arff','w') as f:
#     a2p.dump(df,f)
#
#
# import pandas as pd
# df = pd.DataFrame({
#     'power@NUMERIC':[0.5,0.2],
#     'label@{good,bad}':['good','bad']
# })
# print(a2p.dumps(df))

def df2np(df):
    """
    >>> from lazyds.learning.supervised.classification.rf import rf
    >>> from idict import let
    >>> d = File() >> df2np >> let(rf, n=1)
    >>> d.model
    RandomForestClassifier(n_estimators=1)
    """
    le = LabelEncoder()
    X = df.drop(df.columns[[-1]], axis=1)
    y = le.fit_transform(df[df.columns[-1]])
    # raise Exception({"X": X, "y": y})
    return {"X": X, "y": y}
