import os
import pandas as pd


def load_raw_data(project_root: str):
    """Load train.csv and test.csv from the project root directory.

    Parameters
    ----------
    project_root : str
        Path to the folder containing train.csv and test.csv.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
        train_df, test_df, sample_submission_df
    """
    if not project_root:
        project_root = os.getcwd()

    project_root = os.path.abspath(project_root)
    train_path = os.path.join(project_root, "train.csv")
    test_path = os.path.join(project_root, "test.csv")
    submission_path = os.path.join(project_root, "sample_submission.csv")

    if not os.path.exists(train_path):
        raise FileNotFoundError(f"train.csv not found in project root: {project_root}")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"test.csv not found in project root: {project_root}")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    if os.path.exists(submission_path):
        sample_submission_df = pd.read_csv(submission_path)
    else:
        sample_submission_df = pd.DataFrame()

    return train_df, test_df, sample_submission_df


def handle_missing_values(df: pd.DataFrame, reference_medians: pd.Series = None) -> pd.DataFrame:
    """Fill missing values using median imputation.

    If `reference_medians` is provided, this function uses the training median
    values to impute the target dataframe. Otherwise, it uses the median of the
    provided dataframe.
    """
    if reference_medians is None:
        reference_medians = df.median()

    return df.fillna(reference_medians)
