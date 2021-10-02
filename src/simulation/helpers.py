from scipy.spatial import cKDTree
import pandas as pd

def nearest_nieghbour(df1, df2):
    nA = list(zip(df1['x'], df1['y']))
    nB = list(zip(df2['x'], df2['y']))
    btree = cKDTree(nA)
    dist, idx = btree.query(nB, k=1)
    df1.index = df1.index.set_names(['plants'])
    gdB_nearest = df1.iloc[idx].reset_index()
    gdB_nearest['dist'] = dist
    gdB_nearest = gdB_nearest.loc[gdB_nearest['dist'] < 50.0]
    return gdB_nearest.index, gdB_nearest['plants'], gdB_nearest['size']
