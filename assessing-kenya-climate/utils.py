import numpy as np
import pandas as pd


def get_extremes(data: pd.Series) -> pd.Series:
    """Get the minimum and maximum values of the `data`.

    Args:
        data (pandas.Series): Data array.

    Returns:
        pandas.Series: An array of maximum and minimum values.
    """
    extremes = data.agg([min, max])
    return data[data.isin(extremes)]


def get_extremes_style(
    data: pd.Series, if_max: str = "Max", if_min: str = "Min"
) -> np.ndarray:
    """Get an array of styles/colors/text based on if values in `data` are the
    maximum or minimum.

    Args:
        data (pd.Series): Values to classify.
        if_max (str, optional): Value for maximums. Defaults to "Max".
        if_min (str, optional): Value for minimums. Defaults to "Min".

    Returns:
        np.ndarray: Array of values.
    """
    return np.where(data == data.max(), if_max, if_min)
