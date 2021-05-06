import backtrader as bt
import backtrader.indicators as btind


class ADX(bt.Indicator):
    params = dict()
    lines = ("adx", "adxr", "MA")
    plotlines = dict(adx=dict(color="black", _fill_lt=(20, "lime")))
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[20.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[20],
    )

    def __init__(self):
        ADX = btind.ADXR()
        self.l.adx = ADX.l.adx
        self.l.adxr = ADX.l.adxr
        # self.l.MA = btind.SMMA(self.l.adx, period=96)
