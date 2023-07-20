import time

import akshare as ak
import pandas as pd


def get_latest_all_etf():
    """
    获取最新所有etf基金数据
    :return:
    """
    etf_df = ak.fund_etf_category_sina("ETF基金")
    print(etf_df)
    return etf_df


def get_hist_etf_by_codes(etfs, time_period=1):
    """
    批量获取etfs历史数据
    :param etfs:
    :param time_period:
    :return:
    """
    symbol_df = dict()
    for etf in etfs:
        etf_hist_df = get_hist_etf_by_code(etf, time_period)
        symbol_df[etf] = etf_hist_df
        time.sleep(1)
    return symbol_df


def get_hist_etf_by_code(etf, time_period=1):
    """
    获取etf历史数据
    :param etf:
    :param time_period:
    :return:
    """
    etf_hist_df = ak.fund_etf_hist_sina(symbol=etf)
    etf_hist_df['date'] = pd.to_datetime(etf_hist_df['date'])
    min_date = pd.Timestamp.now() - pd.DateOffset(months=time_period)
    etf_hist_df = etf_hist_df[etf_hist_df['date'] >= min_date]
    etf_hist_df['symbol'] = etf
    etf_hist_df.drop_duplicates(inplace=True)
    etf_hist_df.sort_values(by=['date'], ascending=True, inplace=True)
    etf_hist_df.reset_index(inplace=True, drop=True)
    return etf_hist_df


if __name__ == '__main__':
    get_hist_etf_by_codes(
        [
            'sh518880',  # 黄金ETF
            'sh513100',  # 纳指100
            'sz159915',  # 创业板100（成长股，科技股，中小盘）
            'sh510300',  # 沪深300（价值股，蓝筹股，中大盘）
        ],
        1
    )
