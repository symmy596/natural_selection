from scipy.spatial import cKDTree
import pandas as pd


def nearest_nieghbour(plant, herbivore):
    nA = list(zip(plant["x"], plant["y"]))
    nB = list(zip(herbivore["x"], herbivore["y"]))
    btree = cKDTree(nA)
    dist, idx = btree.query(nB, k=1)
    plant.index = plant.index.set_names(["plants"])
    gdB_nearest = plant.iloc[idx].reset_index()
    gdB_nearest["dist"] = dist
    herbivore['nearest_plant_x'] = gdB_nearest['x']
    herbivore['nearest_plant_y'] = gdB_nearest['y']
    herbivore['dist'] = gdB_nearest['dist']
    herbivore['nearest_neighbour_index'] = gdB_nearest['plants']
    herbivore['nearest_neighbour_size'] = gdB_nearest['size']
    return herbivore
