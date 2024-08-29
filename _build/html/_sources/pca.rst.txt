PCA vs KernelPCA
=================
Principal Component Analysis (PCA)
-----------------------------------
Principal Component Analysis (PCA) is a linear dimensionality reduction technique that projects high-dimensional data onto a lower-dimensional subspace, maximizing variance along the principal components. Steps of PCA analysis involve standardizing the data, computing the covariance matrix, and performing eigenvalue decomposition. PCA is efficient and interpretable in terms of computation and is ideal for linearly separable data. It is commonly used for image compression, noise reduction, and exploratory data analysis.

Kernel Principal Component Analysis (Kernel PCA)
--------------------------------------------------
Kernel Principal Component Analysis (Kernel PCA) extends PCA to handle non-linear dimensionality reduction by mapping data into a higher-dimensional feature space using kernel functions. This allows Kernel PCA to capture complex, non-linear relationships. The process includes choosing a kernel function, computing the kernel matrix, and performing eigenvalue decomposition. Though more computationally intensive, Kernel PCA is highly flexible and suitable for tasks such as pattern recognition and non-linear data analysis, effectively uncovering intricate structures in complex datasets.

Kernels allow the separation of non-linear data and are thus commonly used for non-linear data sets. Kernels available for the KernelPCA function with Scikit-Learn include Linear(Normal PCA), poly, RBF, sigmoid, cosine, and precomputed. More fine-tunning parameters are also available for certain kernels including gamma, degree, and coef0(all initially set to the default values), for more information on those parameters, click `here <https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.KernelPCA.html>`_

.. image:: mineralAI_images/document/pcakpca.png
   :width: 100%