import backtrader as bt
import backtrader.indicators as btind

from indicators.Divergence import Divergence

class Willy(bt.Indicator):
    params = dict(shift=7, period=14)
    lines = ("willy", "ema", "signal", "divergence")
    plotlines = dict(
        willy=dict(color="gray"),
        ema=dict(color="black", _fill_lt=(-80, "lime"), _fill_gt=(-20, "red")),
        signal=dict(_plotskip=True),
        divergence=dict(_plotskip=True)
    )
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[-20.0, -80.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[-20.0, -80.0],
    )

    def __init__(self):
        self.willy = btind.WilliamsR(period=21)
        self.l.willy = self.willy.l.percR
        self.l.ema = btind.EMA(self.willy, period=13)

        self.shift = -1 * self.p.shift

        self.l.divergence = Divergence(
            self.data, self.data1, self.l.ema, shift=self.p.shift
        )

    def next(self):
        self.l.signal[0] = 0
        ind = self.l.ema
        points = (ind[self.shift -1], ind[self.shift], ind[self.shift + 1])
        if max(points) > -20:
            self.l.signal[0] = -1
        elif min(points) < -80:
            self.l.signal[0] = 1
