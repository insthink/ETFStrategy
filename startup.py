import pandas as pd

from market import get_hist_etf_by_codes
from util import cal_factors, cal_ranks

# 设置显示所有列
pd.set_option('display.max_columns', None)

context = dict()


def before_run():
    """
    运行前参数设置
    :return:
    """
    context.update({
        'etf_pool': [
            'sh518880',  # 黄金ETF
            'sh513100',  # 纳指100
            'sz159915',  # 创业板100（成长股，科技股，中小盘）
            'sh510300',  # 沪深300（价值股，蓝筹股，中大盘）
        ],
        'factors': [
            ('mtm_slope', 3, False, 0.5),
            # ('mtm_mean', 3, True, 0.5),
        ]
    })


def running():
    symbol_df = get_hist_etf_by_codes(context.get('etf_pool'), time_period=1)
    df_all = pd.DataFrame()
    for symbol in symbol_df.keys():
        df = symbol_df[symbol]
        df_with_factor = cal_factors(df, context.get('factors'))
        df_all = pd.concat([df_all, df_with_factor])
    df_latest = df_all[df_all['date'] == df_all['date'].max()]  # 筛选出最近数据
    df = cal_ranks(df_latest, context.get('factors'))
    df.sort_values(by=['rank_all'], ascending=True, inplace=True)
    print(df)
    print(f"当前需要下单的标的为{df.head(1)['symbol']}")


def after_run():
    pass


if __name__ == '__main__':
    before_run()
    running()
    after_run()
