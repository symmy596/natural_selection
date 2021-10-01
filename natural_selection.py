import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from sklearn.neighbors import KDTree
from scipy.spatial import cKDTree

def move(df):
    x_coords = df['x'].tolist()
    y_coords = df['y'].tolist()

    for i in range(len(x_coords)):
        x_move = random.uniform(-0.02, 0.02)
        y_move = random.uniform(-0.02, 0.02)

        x_coords[i] = x_coords[i] + x_move
        y_coords[i] = y_coords[i] + y_move
        if df.iloc[i]['x'] > 1:
            x_coords[i] = x_coords[i] - abs(x_move)
        if df.iloc[i]['x'] < 0:
            x_coords[i] = x_coords[i] + abs(x_move)
        if df.iloc[i]['y'] > 1:
            y_coords[i] = y_coords[i] - abs(y_move)
        if df.iloc[i]['y'] < 0:
            y_coords[i] = y_coords[i] + abs(y_move)
    return pd.DataFrame({'x': x_coords, 'y': y_coords, 'range': df['range'].tolist()})

def initialise_herbivores():
    x = [random.uniform(0, 1) for i in range(50)]
    y = [random.uniform(0, 1) for i in range(50)]
    movement_range = [random.uniform(0, 0.1) for i in range(50)]
    return pd.DataFrame({'x': x, 'y': y, 'range': movement_range})

def initialise_plants(size=50):
    x = [random.uniform(0, 1) for i in range(size)]
    y = [random.uniform(0, 1) for i in range(size)]
    return pd.DataFrame({'x': x, 'y': y})

def grow_plant(df):
    x = random.randint(0,10)
    if x > 5:
        new_plant = initialise_plants(size=1)
        return pd.concat([df, new_plant]).reset_index(drop=True)
    else:
        return df

def nearest_nieghbour(df_1, df_2):
    nA = list(zip(df_1['x'], df_1['y']))
    nB = list(zip(df_2['x'], df_2['y']))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    print(dist)
    gdB_nearest = df_2.iloc[idx]
    print(gdB_nearest)
    gdf = pd.concat(
        [
            df_1.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf

def eat_plant(herbivore, plant):
    df = nearest_nieghbour(herbivore, plant)

herbivores = initialise_herbivores()


plants = initialise_plants()


#plt.scatter(herbivores['x'], herbivores['y'], color='blue')
#plt.scatter(plants['x'], plants['y'], color='green')
#plt.xlim(0,1)
#plt.ylim(0,1)
#plt.axis('off')
for i in range(1000):
    #plt.clf()
    #plt.scatter(herbivores['x'], herbivores['y'],  color='blue')  
    #plt.scatter(plants['x'], plants['y'], color='green')
    #plt.xlim(0,1)
    #plt.ylim(0,1)
    #plt.axis('off')
    plants = grow_plant(plants)
    herbivores = move(herbivores)
    eat_plant(herbivores, plants)
    #plt.pause(0.0000000001)

#plt.show()


