import pandas as pd


def cal_factors(df: pd.DataFrame, factors):
    for factor in factors:
        df = _cal_factor(df, factor)
    return df


def cal_ranks(df: pd.DataFrame, factors):
    df = df.copy()
    df.loc[:, 'rank_all'] = 0.0
    for factor in factors:
        df = _cal_rank(df, factor)
        factor_name, _, _, _ = factor
        df.loc[:, 'rank_all'] = df['rank_all'] + df[f'{factor_name}_rank']
    return df


def _cal_factor(df: pd.DataFrame, factor):
    df = df.copy()
    factor_name, factor_n, _, _ = factor
    _cls = __import__('factors.%s' % factor_name, fromlist=('',))
    df = getattr(_cls, 'calculate')(factor_name, df, factor_n)
    return df


def _cal_rank(df: pd.DataFrame, factor):
    df = df.copy()
    factor_name, _, ascending, weight = factor
    df.drop_duplicates(inplace=True)
    df.sort_values(by=factor_name, ascending=ascending, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.loc[:, f'{factor_name}_rank'] = df.index * weight
    return df
