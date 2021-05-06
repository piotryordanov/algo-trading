import backtrader as bt
import backtrader.indicators as btind


class WilliamAlligator(bt.Indicator):
    lines = ("jaw", "teeth", "lips")
    params = dict()

    plotlines = dict(
        jaw=dict(color="black", fillstyle="full", ls="-"),
        teeth=dict(color="blue", fillstyle="full", ls="-"),
        lips=dict(color="lime", fillstyle="full", ls="-"),
    )
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.jaw = btind.SMMA(period=13)
        self.teeth = btind.SMMA(period=8)
        self.lips = btind.SMMA(period=5)

    def next(self):
        self.l.jaw[0] = self.jaw[-8]
        self.l.teeth[0] = self.teeth[-5]
        self.l.lips[0] = self.lips[-3]
