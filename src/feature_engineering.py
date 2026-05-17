import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif


def apply_log_transform(df: pd.DataFrame, columns=None) -> pd.DataFrame:
    """Apply log1p transform to specified skewed numeric columns."""
    df = df.copy()
    if columns is None:
        columns = []

    for column in columns:
        if column in df.columns:
            df[column] = np.log1p(df[column].clip(lower=0).astype(float))

    return df


def remove_high_correlation(df: pd.DataFrame, threshold: float = 0.90):
    """Drop features with absolute correlation strictly higher than threshold."""
    if df.shape[1] == 0:
        return df.copy(), []

    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    return df.drop(columns=to_drop), to_drop


def select_top_features(X, y, k: int = 10):
    """Select the top k features using univariate ANOVA F-test."""
    selector = SelectKBest(score_func=f_classif, k=k)
    X_selected = selector.fit_transform(X, y)
    return X_selected, selector
