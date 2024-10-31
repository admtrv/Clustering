## Agglomerative Clustering

Agglomerative clustering is a hierarchical clustering method that builds clusters in a bottom-up fashion. The process starts by considering each data point as an individual cluster and then iteratively merges the closest pairs of clusters until a stopping criterion is met or all points are in a single cluster.

## Types

- **Centroid Clustering**: Uses the mean (centroid) of all points within a cluster to represent the cluster's center. The centroid may not correspond to an actual data point.
- **Medoid Clustering**: Uses an actual data point (medoid) as the representative center of the cluster. The medoid is the point in the cluster that minimizes the sum of distances to all other points in the cluster.
