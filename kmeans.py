import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

"""
[9.77075874 3.27621022] 1
"""
(X, Y) = make_blobs(n_samples=200, centers=3, cluster_std=2.75, random_state=42)

scaled_features = StandardScaler().fit_transform(X)

model = KMeans(
    n_clusters=3,
    max_iter=10,
)
model.fit(X)

x = []
y = []
cx = []
cy = []
for i in X:
    x += [round(i[0], 2)]
    y += [round(i[1], 2)]

for i in model.cluster_centers_:
    cx += [round(i[0], 2)]
    cy += [round(i[1], 2)]

plt.plot(x, y, c="green")
plt.plot(cx, cy, c="red")
plt.show()
