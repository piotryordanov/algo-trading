import backtrader as bt
import backtrader.indicators as btind

from Settings import Fractal_Right_Shift


class Divergence(bt.Indicator):
    _mindatas = 2
    params = dict(shift=Fractal_Right_Shift, max_window=50)
    lines = ("divergence", "")
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
    plotlines = dict(divergence=dict(color="orange", ls="--"))

    def __init__(self):
        self.Fractal = self.data1
        self.Indicator = self.data2
        self.reset()
        self.shift = -1 * self.p.shift
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
        prev_ind = info["ind"]
        ind = func(
            func(self.Indicator[self.shift], self.Indicator[self.shift - 1]),
            self.Indicator[self.shift + 1],
        )
        if (edge - curr) * (prev_ind - ind) < 0:
            self.l.divergence[0] = info["direction"]

        return dict(
            edge=curr, ind=ind, window=0, func=func, direction=info["direction"]
        )

    def next(self):
        hh = self.Fractal.fractal_bearish[self.shift]
        ll = self.Fractal.fractal_bullish[self.shift]

        self.l.divergence[0] = 0

        if hh == hh:
            self.hh = self.compute(self.hh, hh)
        else:
            self.hh = self.adjust_window(self.hh)

        if ll == ll:
            self.ll = self.compute(self.ll, ll)
        else:
            self.ll = self.adjust_window(self.ll)
