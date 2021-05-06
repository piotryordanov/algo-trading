import backtrader as bt
import backtrader.indicators as btind


class Regression(bt.Indicator):
    params = dict(period=30)
    lines = ("regression",)
    # plotlines = dict(
    #     rsi=dict(color="black", _fill_gt=(70, "red"), _fill_lt=(30, "lime")),
    #     signal=dict(_plotskip=True),
    #     divergence=dict(_plotskip=True),
    #     edge_levels=dict(_plotskip=True),
    # )
    plotinfo = dict(subplot=True)
    # plotinfo = dict(
    #     # Add extra margins above and below the 1s and -1s
    #     plotymargin=0.15,
    #     # Plot a reference horizontal line at 1.0 and -1.0
    #     plothlines=[30.0, 70.0],
    #     # Simplify the y scale to 1.0 and -1.0
    #     plotyticks=[30.0, 70.0],
    # )

    def __init__(self):
        # self.ind = btind.OLS_Slope_InterceptN()
        self.l.regression = bt.talib.LINEARREG_SLOPE(self.data, timeperiod=self.p.period)
