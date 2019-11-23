from sklearn.cluster import KMeans
import numpy as np


def clust(img,n=0):
  data=img
  d=np.reshape(data,(data.shape[0]*data.shape[1], 3))
  clf = KMeans(n_clusters=n)
  clf.fit(d)
  newd={i:clf.cluster_centers_[i] for i in range(n)}
  rez = np.copy(d)
  for i in range(len(d)):
    rez[i]=newd[clf.labels_[i]]
  return rez.reshape(data.shape[0], data.shape[1], 3)
