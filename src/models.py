"""
models.py
Helper functions for clustering (Phase 2) and regression modelling (Phase 3).
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# Phase 2 — Clustering

def normalise_profiles(profiles: pd.DataFrame) -> np.ndarray:
    """L2-normalise each site profile row."""
    scaler = StandardScaler()
    return scaler.fit_transform(profiles)


def find_optimal_k(X: np.ndarray, k_range=range(2, 9), random_state: int = 42):
    """
    Return inertia and silhouette scores for a range of k values.
    Use elbow + silhouette to pick k.
    """
    inertias, silhouettes = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = km.fit_predict(X)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X, labels))
    return list(k_range), inertias, silhouettes


def cluster_sites(X: np.ndarray, k: int, random_state: int = 42) -> np.ndarray:
    """Fit KMeans with chosen k and return cluster labels."""
    km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    return km.fit_predict(X)


# Phase 3 — Modelling

def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(np.mean((np.array(y_true) - np.array(y_pred)) ** 2)))


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.array(y_true) - np.array(y_pred))))
