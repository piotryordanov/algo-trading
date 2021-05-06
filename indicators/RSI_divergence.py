import backtrader as bt
import backtrader.indicators as btind

from indicators.Fractal import Fractal
from Settings import Fractal_Right_Shift


class RSI_divergence(bt.Indicator):
    _mindatas = 2
    params = dict(fractal_shift=Fractal_Right_Shift, max_window=500, rsi_period=14)
    lines = ("divergence", "threshold_cross", "signal")
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[2.0, 0, -2.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[2.0, -2.0],
    )

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(
        divergence=dict(color="orange", ls="--"),
        threshold_cross=dict(color="lime", ls="--"),
        signal=dict(color="black"),
    )

    def __init__(self):
        self.Fractal = self.data1
        # self.RSI = btind.RSI_Safe(period=self.p.rsi_period)
        self.RSI = btind.MACDHisto()
        self.reset()
        self.shift = -1 * self.p.fractal_shift
        self.max_window = self.p.max_window
        self.hh = dict(edge=0, ind=0, window=0, func=max, direction=-1)
        self.ll = dict(edge=0, ind=0, window=0, func=min, direction=1)

    def reset(self):
        self.count = 0

    def adjust_window(self, info):
        window = info["window"]
        if window > self.max_window:
            return dict(
                edge=0, ind=0, window=0, func=info["func"], direction=info["direction"]
            )
        else:
            return dict(
                edge=info["edge"],
                ind=info["ind"],
                window=window + 1,
                func=info["func"],
                direction=info["direction"],
            )

    def compute(self, info, curr):
        func = info["func"]
        edge = info["edge"]
        ind = info["ind"]
        rsi = func(
            func(self.RSI[self.shift], self.RSI[self.shift - 1]),
            self.RSI[self.shift + 1],
        )
        if (edge - curr) * (ind - rsi) < 0 or abs(ind - rsi) < 0.786:
            self.l.divergence[0] = info["direction"]

        if (ind < 30 or ind > 70) or (rsi < 30 or rsi > 70):
            self.l.threshold_cross[0] = info["direction"]

        return dict(
            edge=curr, ind=rsi, window=0, func=func, direction=info["direction"]
        )

    def next(self):
        hh = self.Fractal.fractal_bearish_hh[self.shift]
        ll = self.Fractal.fractal_bullish_ll[self.shift]

        self.l.divergence[0] = 0
        self.l.threshold_cross[0] = 0

        if hh == hh:
            self.hh = self.compute(self.hh, hh)
        else:
            self.hh = self.adjust_window(self.hh)

        if ll == ll:
            self.ll = self.compute(self.ll, ll)
        else:
            self.ll = self.adjust_window(self.ll)

        self.l.signal[0] = self.l.threshold_cross[0] + self.l.divergence[0]
