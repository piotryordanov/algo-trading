import backtrader as bt
import backtrader.indicators as btind

from indicators.Divergence import Divergence
from indicators.Ranging import Ranging


class MACD(bt.Indicator):
    params = dict(shift=7)
    lines = ("histo", "histo_line", "signal")
    plotlines = dict(
        histo=dict(_method="bar", alpha=0.30, width=0.5, color="black"),
        histo_line=dict(color="black"),
        signal=dict(_plotskip=True),
    )
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[0],
    )

    def __init__(self):
        self.MACD = btind.MACDHisto(period_me1=9, period_me2=30, period_signal=9)
        self.l.histo = self.MACD.l.macd - self.MACD.l.signal
        self.l.histo_line = self.l.histo

        fractal = self.data1
        self.l.signal = Divergence(self.data, fractal, self.l.histo, shift=self.p.shift)
