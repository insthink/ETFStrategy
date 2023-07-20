import pandas as pd

from commons.market import get_hist_etf_by_codes
from commons.util import cal_factors, cal_ranks

# 全局设置
pd.set_option('display.max_columns', None)
context = dict()


def before_run():
    """
    运行前参数设置
    :return:
    """
    context.update({

        'etf_pool': [  # 配置ETF池(后续会更新写法)
            'sh518880',  # 黄金ETF
            'sh513100',  # 纳指100
            'sz159915',  # 创业板100（成长股，科技股，中小盘）
            'sh510300',  # 沪深300（价值股，蓝筹股，中大盘）
        ],
        'factors': [  # 配置因子(因子名称， 滚动窗口大小， 是否从小到大排序， 权重)
            ('mtm_slope', 25, False, 0.5),
            # ('mtm_mean', 3, True, 0.5),
        ]
    })


def running():
    """
    运行时计算：排序、选择
    :return:
    """
    symbol_df = get_hist_etf_by_codes(context.get('etf_pool'), time_period=3)
    df_all = pd.DataFrame()
    for symbol in symbol_df.keys():
        df = symbol_df[symbol]
        df_with_factor = cal_factors(df, context.get('factors'))
        df_all = pd.concat([df_all, df_with_factor])
    df_latest = df_all[df_all['date'] == df_all['date'].max()]  # 筛选出最近数据
    df = cal_ranks(df_latest, context.get('factors'))
    df.sort_values(by=['rank_all'], ascending=True, inplace=True)
    df_select = df.head(1)
    context.update({
        'select_etf': {
            'date': df_select.at[0, 'date'],
            'symbol': df_select.at[0, 'symbol'],
            'close': df_select.at[0, 'close'],
        }
    })
    print(context)


def after_run():
    pass


def run():
    before_run()
    running()
    after_run()


if __name__ == '__main__':
    run()
