What is KElbowVisualizer? 
===============================

The KElbowVisualizer is used in clustering to determine the optimal number of clusters (k) for a given dataset. The "elbow method" selects this number (k) by fitting the model with a range of values for k and then plotting a score (distortion score) for each value.

The distortion score measured how well the clusters have been formed. It is usually the sum of the squared distances between each data point and the centroid of its assigned cluster. Lower distortion scores indicate that the data points are closer to their respective cluster centroids, implying better-defined clusters. 

The elbow method looks for an "elbow" point in the plot where the distortion score starts to decrease more slowly. This point suggests that adding more clusters beyond this value does not significantly improve the clustering quality. 

.. image:: ../images/doc/yellowbrick.png
   :width: 100%


