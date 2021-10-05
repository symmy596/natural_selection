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
    return gdB_nearest
