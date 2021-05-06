import backtrader as bt

from indicators.MACD import MACD
from indicators.RSI import RSI
from indicators.Willy import Willy


class Internals(bt.Indicator):
    params = dict(shift=7, threshold=3, show_indicators=False)
    lines = ("signal", "sum", "rsi", "macd", "willy")
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[3.0, -3.0],
    )

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(
        signal=dict(color="black", ls="-"),
        sum=dict(color="gray"),
        rsi=dict(_plotskip=True),
        macd=dict(_plotskip=True),
        willy=dict(_plotskip=True),
    )

    def _plotinit(self):
        if self.p.show_indicators:
            self.plotlines.rsi._plotskip = False
            self.plotlines.macd._plotskip = False
            self.plotlines.willy._plotskip = False

    def __init__(self):
        (d, f, s) = (self.data, self.data1, self.p.shift)
        rsi = RSI(d, f, shift=s)
        macd = MACD(d, f, shift=s)
        willy = Willy(d, f, shift=s)

        self.rsi = rsi.l.signal
        self.macd = macd.l.signal
        self.willy = willy.l.signal

        self.rsi_divergence = rsi.l.divergence
        self.willy_divergence = willy.l.divergence

        (self.ll, self.hh, self.shift) = (0, 0, -1 * self.p.shift)

    def compute_sum(self):
        self.l.rsi[0] = self.rsi[0] + self.rsi_divergence[0]
        self.l.willy[0] = self.willy[0] + self.willy_divergence[0]
        self.l.macd[0] = self.macd[0]

        self.l.sum[0] = self.l.rsi[0] + self.l.willy[0] + self.l.macd[0]
        # self.l.sum[0] = self.l.willy[0] + self.l.macd[0]
        # self.l.sum[0] = self.l.macd[0]
        # self.l.sum[0] = self.l.rsi[0]
        if self.l.sum[0] >= 3:
            self.ll = self.data.low[self.shift]
        elif self.l.sum[0] <= -3:
            self.hh = self.data.high[self.shift]

    def normalize_signal(self, th):
        if self.l.signal[0] > th:
            self.l.signal[0] = th
        elif self.l.signal[0] < -th:
            self.l.signal[0] = -th

    def next(self):
        self.compute_sum()
        self.l.signal[0] = self.l.sum[0]

        th = self.p.threshold

        if self.ll > 0 and self.l.signal[-1] >= th:
            if (self.data.low[0] < self.ll) or (self.sum[0] <= -th):
                self.ll = 0
            else:
                self.l.signal[0] = self.l.signal[-1]
        elif self.hh > 0 and self.l.signal[-1] <= -th:
            if (self.data.high[0] > self.hh) or (self.sum[0] >= th):
                self.hh = 0
            else:
                self.l.signal[0] = self.l.signal[-1]

        self.normalize_signal(th)
