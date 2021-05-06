import math

import backtrader as bt
import backtrader.indicators as btind


class Ranging(bt.Indicator):
    params = dict(shift=10, threshold=15)
    lines = ("hh", "ll", "higher", "lower")
    plotinfo = dict(subplot=False)

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(
        higher=dict(color="black"),
        lower=dict(color="black"),
        ll=dict(_plotskip=True),
        hh=dict(_plotskip=True),
    )

    def __init__(self):
        self.fractal = self.data1
        self.reset()

    def reset(self):
        try:
            self.l.hh[0] = float("nan")
            self.l.ll[0] = float("nan")
        except:
            pass
        self.hh1 = 0
        self.hh2 = 0
        self.ll1 = 0
        self.ll2 = 0
        self.idxhh = 0
        self.idxll = 0

    def find_doublebottom(self):
        (l1, l2) = (self.data.low[0], self.data.low[-self.idxll])
        if self.l.hh[0] > 0:
            max_val = self.l.hh[0]
        else:
            last_highs = self.data.high.get(size=self.idxll)
            max_val = max(last_highs)
        min_val = min(l1, l2)
        r = max_val - min_val
        diff = abs(l1 - l2)
        if diff * 100 / r < self.p.threshold:
            if math.isnan(self.l.ll[0]) or min_val < self.l.ll[0]:
                for i in range(-self.idxll, 1):
                    self.l.ll[i] = min_val
        self.idxll = 0

    def find_doubletop(self):
        (h1, h2) = (self.data.high[0], self.data.high[-self.idxhh])
        if self.l.ll[0] > 0:
            min_val = self.l.ll[0]
        else:
            last_lows = self.data.low.get(size=self.idxhh)
            min_val = min(last_lows)

        max_val = max(h1, h2)
        r = max_val - min_val
        diff = abs(h1 - h2)
        if diff * 100 / r < self.p.threshold:
            if math.isnan(self.l.hh[0]) or max_val > self.l.hh[0]:
                for i in range(-self.idxhh, 1):
                    self.l.hh[i] = max_val
        self.idxhh = 0

    def draw_range(self):
        if (
            self.l.hh[0] > 0
            and self.l.ll[0] > 0
            and self.idxll < 400
            and self.idxhh < 400
        ):
            self.l.higher[0] = self.l.hh[0]
            self.l.lower[0] = self.l.ll[0]
            self.idxll = 0
            self.idxhh = 0

    def next(self):
        hh = self.fractal.l.fractal_bearish_hh[0]
        ll = self.fractal.l.fractal_bullish_ll[0]

        self.l.hh[0] = self.l.hh[-1]
        self.l.ll[0] = self.l.ll[-1]

        if self.l.hh[0] > 0:
            if self.data.high[0] > self.l.hh[0]:
                self.reset()
        if self.l.ll[0] > 0:
            if self.data.low[0] < self.l.ll[0]:
                self.reset()

        if hh > 0:
            if self.hh2 == 0:
                self.hh2 = hh
                self.idxhh = 0
            else:
                if hh > self.hh2:
                    self.hh1 = self.hh2
                    self.hh2 = hh
                    self.find_doubletop()
        if ll > 0:
            if self.ll2 == 0:
                self.ll2 = ll
                self.idxll = 0
            else:
                self.ll1 = self.ll2
                self.ll2 = ll
                self.find_doublebottom()

        self.idxll += 1
        self.idxhh += 1

        self.draw_range()
