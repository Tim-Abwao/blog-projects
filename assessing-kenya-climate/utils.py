import pandas as pd
import numpy as np


def aggregate_region_data(data, variable):
    return (
        data.mean()
        .reset_index()
        .rename(columns={"index": "region", 0: f"avg {variable}"})
    )


def get_extremes(series: pd.Series) -> pd.Series:
    """Get the minimum and maximum values of the `series`.

    Arguments:
        series (pandas.Series): Data array.

    Returns:
        pandas.Series: An array of maximum and minimum values.
    """
    extremes = series.agg([min, max])
    return series[series.isin(extremes)]


def get_extremes_style(
    data: pd.Series, text_for_max: str = "Max", text_for_min: str = "Min"
) -> np.ndarray:
    return np.where(data == data.max(), text_for_max, text_for_min)
