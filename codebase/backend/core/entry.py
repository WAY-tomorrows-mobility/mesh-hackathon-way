import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sklearn as sk
from sklearn.cluster import KMeans

routes = []

clusterCount = 2

should_draw = False


def split_numeric(orders: list):
    table = {
        "ecological": [],
        "time": [],
        "comfort": [],
        # "nr": []
    }
    for i, order in enumerate(orders):
        table["ecological"].append(order["options"]["ecological"])
        table["time"].append(order["options"]["time"])
        table["comfort"].append(order["options"]["comfort"])
        # table["nr"].append(i)

    # print(table)
    # print(table)
    df = pd.DataFrame(table)

    kmeans = KMeans(n_clusters=clusterCount)
    kmeans = kmeans.fit(df)

    labels = kmeans.predict(df)

    if should_draw:
        centroids = kmeans.cluster_centers_

        fig = plt.figure(figsize=(5, 5))

        # set color for each datapoint
        colmap = {1: 'b', 2: 'k', 3: 'r', 4: "g", 5: "y", 6: "c", 7: "m", 8: "w", 9: "orange", 10: "olive", 11: "pink"}
        colors = list(map(lambda x: colmap[x + 1], labels))

        # draw each datapoint
        ax = plt.axes(projection='3d')
        # plt.scatter(df['ecological'], df['time'], df['comfort'], color=colors, alpha=0.5, edgecolor='k')
        ax.scatter(df['ecological'], df['time'], df['comfort'], c=colors, alpha=0.5, edgecolor='k')
        # draw each centroid
        # print(centroids)
        for idx, centroid in enumerate(centroids):
            cent = centroid[0:2]
            ax.scatter(*cent, color=colmap[idx + 1])
        # plt.xlim(0, 80)
        # plt.ylim(0, 80)

        ax.set_xlabel('time')
        ax.set_ylabel('comfort')
        ax.set_zlabel('ecological')

    # plt.show()

    return labels


def get_location_center(orders: list):
    xa = []
    ya = []
    for o in orders:
        x, y = o["location"]
        xa.append(x)
        ya.append(y)

    return sum(xa) / len(xa), sum(ya) / len(ya)


def calculate_pickup(orders, labels):
    centroids = []

    for j in range(clusterCount):
        arr = []

        for i, o in enumerate(orders):
            if labels[i] == j:
                arr.append(o)

        centroids.append(get_location_center(arr))

    if should_draw:
        table = {
            "x": [],
            "y": []
        }
        for o in orders:
            x, y = o["location"]

            table["x"].append(x)
            table["y"].append(y)

        df = pd.DataFrame(table)

        colmap = {1: 'b', 2: 'k', 3: 'r', 4: "g", 5: "y", 6: "c", 7: "m", 8: "w", 9: "orange", 10: "olive", 11: "pink"}
        colors = list(map(lambda x: colmap[x + 1], labels))
        fig = plt.figure(figsize=(5, 5))
        plt.scatter(df['x'], df['y'], color=colors, alpha=0.5, edgecolor='k')

        # print(table)
        # print(centroids)
        axes = plt.axes()
        # axes.set_aspect(1)
        for idx, centroid in enumerate(centroids):
            plt.scatter(*centroid, color=colmap[idx + 1])
            circle = plt.Circle(centroid, 10, color=colmap[idx + 1], alpha=0.3)

            axes.add_artist(circle)

            # Drawing_colored_circle = plt.Circle((0.6, 0.6), 0.2)

        plt.show()

    return centroids


def start(orders: list, n: int, draw=False):
    global should_draw, clusterCount
    should_draw = draw
    clusterCount = n

    labels = split_numeric(orders)

    pickUpPoints = calculate_pickup(orders, labels)

    out = []
    [out.append({
        "order": [],
    }) for i in range(n)]

    for i, o in enumerate(orders):
        cluster_key = labels[i]
        out[cluster_key]["order"].append(o)

    print(out)
    print(pickUpPoints)
    for i, _ in enumerate(out):
        out[i]["centroid"] = pickUpPoints[i]

    return out
