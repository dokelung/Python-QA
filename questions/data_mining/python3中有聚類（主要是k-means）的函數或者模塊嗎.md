# python3 中有聚類（主要是k-means）的函數或者模塊嗎

## 問題

最經在做用戶畫像，需要對數據進行聚類，發現python貌似沒有現成的聚類函數。不知道是不是我沒有找到，還是真的沒有，如果沒有，大夥有什麼好的軟件推薦去完成聚類分析。

謝謝各位了~~

問題出自 [segmentfault](https://segmentfault.com/q/1010000006057925/a-1020000006057999), by [EchoJnn](https://segmentfault.com/u/echojnn)

## 回答

> k-means clustering aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean, serving as a prototype of the cluster.

* [sklearn.cluster.KMeans](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

* [scipy-cluster](http://docs.scipy.org/doc/scipy/reference/cluster.html)
