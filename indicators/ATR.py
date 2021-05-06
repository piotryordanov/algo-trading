import backtrader as bt
import backtrader.indicators as btind


class ATR(bt.Indicator):
    params = dict(period=30)
    lines = ("ATR", "SMMA")
    plotlines = dict(ATR=dict(color="black"))
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[0],
    )

    def __init__(self):
        ATR = btind.ATR()
        self.l.ATR = ATR
        self.l.SMMA = btind.SMMA(self.l.ATR, period=self.p.period)
