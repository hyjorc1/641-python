#%%
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

def get_iris():
    data = load_iris()
    df = pd.DataFrame(np.column_stack((data.data, data.target)), 
        columns = ['sepal length','sepal width','petal length','petal width']+['target'])
    df['label'] = df.target.replace(dict(enumerate(data.target_names)))
    return df.drop(['target'], axis=1)

def dot(K, L):
   if len(K) != len(L):
      return 0
   return sum(i[0] * i[1] for i in zip(K, L))

# %%

