import backtrader as bt
import backtrader.indicators as btind

from indicators.Divergence import Divergence


class RSI(bt.Indicator):
    params = dict(shift=7, period=2)
    lines = ("rsi", "signal", "divergence")
    plotlines = dict(
        rsi=dict(color="black", _fill_gt=(95, "red"), _fill_lt=(5, "lime")),
        signal=dict(_plotskip=True),
        divergence=dict(_plotskip=True),
        edge_levels=dict(_plotskip=True)
    )
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[5.0, 95.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[5.0, 95.0],
    )

    def __init__(self):
        self.l.rsi = btind.RSI_Safe(period=self.p.period)
        self.l.divergence = Divergence(
            self.data, self.data1, self.rsi, shift=self.p.shift
        )
        self.shift = -1 * self.p.shift

    def next(self):
        self.l.signal[0] = 0
        ind = self.l.rsi
        points = (ind[self.shift -1], ind[self.shift], ind[self.shift + 1])
        if max(points) > 70:
            self.l.signal[0] = -1
        elif min(points) < 30:
            self.l.signal[0] = 1
