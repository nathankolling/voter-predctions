from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import itertools

def clean(df):
    df = df[(df.CC16_364c == 1.0) | (df.CC16_364c == 2.0)] # getting only the people who preferred Trump or Clinton
    df = df.dropna().astype(int).rename(columns={'birthyr': 'age', 'countyfips': 'state'})
    df.age = 2016 - df.age
    df['state'] = df['state'].map(lambda x: f'{x:05}'[:2]) # converting county fips to state ID string
    return df

def corr_heatmap(df):
    plt.figure(figsize=(16, 5))
    corr = df.corr().abs()
    mask = np.tril(np.ones_like(corr, dtype=bool), k=-1)
    corr = corr.where(cond=mask).iloc[1:,:-1]
    sns.heatmap(corr, annot=True, vmin=0, vmax=1);

def plot_confusion_matrix(cm, classes, title):
    fig = plt.figure(figsize=(5, 5))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], '.2f'),horizontalalignment="center",color="white" if cm[i, j] > thresh else "black")
    plt.ylabel('True Class')
    plt.xlabel('Predicted Class')
    plt.tight_layout()
    plt.grid(False)
    