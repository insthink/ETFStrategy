def calculate(*args):
    factor_name, df, n = args
    df['mtm'] = df['close'] / df['close'].shift(n) - 1
    df[factor_name] = df['mtm'].rolling(n, min_periods=1).mean()
    del df['mtm']
    return df
