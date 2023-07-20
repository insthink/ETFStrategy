import math

import numpy as np


def calculate(*args):
    factor_name, df, n = args
    df[factor_name] = df['close'].rolling(n).apply(_cal_score)
    return df


def _cal_score(close_arr):
    y = np.log(close_arr)
    x = np.arange(y.size)
    slope, intercept = np.polyfit(x, y, 1)
    annualized_returns = math.pow(math.exp(slope), 250) - 1
    r_squared = 1 - (sum((y - (slope * x + intercept)) ** 2) / ((len(y) - 1) * np.var(y, ddof=1)))
    score = annualized_returns * r_squared
    return score
