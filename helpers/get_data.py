import backtrader as bt
from Settings import Asset, FromDate, ToDate

'''
Fetches Data from CSV
'''
OHLC_DIR = "./OHLC_DATA/"

default_settings = dict(
    fromdate=FromDate,
    todate=ToDate,
    nullvalue=0.0,
    datetime=0,
    time=-1,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    # separator=";",
    openinterest=-1,
)

def get_data(dataname):
    timeframe = bt.TimeFrame.Minutes
    compression = 240
    # compression = 60
    data = bt.feeds.GenericCSVData(
        dataname=OHLC_DIR + dataname,
        timeframe=timeframe,
        compression=compression,
        **default_settings
    )
    # data.plotinfo.plotlog = True
    # data.plotinfo.plotylimited = True
    return data
    # if compression == 240:
    #     timeframe = bt.TimeFrame.Minutes
    # if provider == 'MT4':
    #     return bt.feeds.MT4CSVData(
    #         dataname=dataname,
    #         fromdate=FromDate,
    #         todate=ToDate,
    #         timeframe=timeframe,
    #         compression=compression
    #     )
    # else:
    #     if provider == 'etoro':
    #         settings = dict(
    #             dtformat='%Y-%m-%d %H:%M:%S+00:00',
    #             datetime=0,
    #             time=-1,
    #             open=1,
    #             close=2,
    #             high=3,
    #             low=4,
    #             volume=-1,
    #             openinterest=-1
    #         )
    #     elif provider == 'FX':
    #         settings = dict(
    #             datetime=0,
    #             time=-1,
    #             open=1,
    #             high=2,
    #             low=3,
    #             close=4,
    #             volume=5,
    #             # separator=";",
    #             openinterest=-1,
    #         )
    #     elif provider == 'cryptocompare':
    #         settings = dict(
    #             datetime=8,
    #             time=-1,
    #             open=4,
    #             close=1,
    #             high=2,
    #             low=3,
    #             volume=6,
    #             openinterest=-1,
    #         )
    #     elif provider == '188':
    #         ## Reference: https://www.backtrader.com/docu/dataautoref.html?highlight=unix
    #         settings = dict(
    #             dtformat=2,
    #             datetime=0,
    #             time=-1,
    #             open=1,
    #             close=4,
    #             high=2,
    #             low=3,
    #             volume=5,
    #             openinterest=-1,
    #         )
    #     timeframe = bt.TimeFrame.Minutes
    #     data = bt.feeds.GenericCSVData(
    #         dataname=dataname,
    #         fromdate=FromDate,
    #         todate=ToDate,
    #         nullvalue=0.0,
    #         timeframe=timeframe,
    #         compression=compression,
    #         **settings
    #     )
    #     return data
