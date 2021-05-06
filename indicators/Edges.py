import math

import backtrader as bt


class Edges(bt.Indicator):
    lines = ("upper", "lower", "h", "l", "p33", "p66", "direction")

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        upper=dict(color="black"),
        lower=dict(color="black"),
        h=dict(color="orange"),
        l=dict(color="orange"),
        p33=dict(color="lime"),
        p66=dict(color="lime"),
    )

    def _plotinit(self):
        pass

    params = dict(initial=50)

    def __init__(self):
        pass

    def update(self):
        for line in self.l.lines:
            line[0] = line[-1]

    def next(self):
        if len(self.data.close) < self.p.initial:
            return
        self.update()
        (hh, ll, direction) = self.l.upper, self.l.lower, self.l.direction
        (h, l, p33, p66) = (self.l.h, self.l.l, self.l.p33, self.l.p66)
        (high, low, close) = (self.data.high, self.data.low, self.data.close)

        if math.isnan(hh[0]):
            hh[0] = max(high.get(size=self.p.initial))
            ll[0] = min(low.get(size=self.p.initial))

        if high[0] > hh[0]:
            # h[0] = float("nan")
            hh[0] = high[0]
            direction[0] = 1
        if low[0] < ll[0]:
            l[0] = float("nan")
            ll[0] = low[0]
            direction[0] = -1
            if h[0] > 0:
                hh[0] = h[0]

        r = hh[0] - ll[0]
        p33[0] = ll[0] + r * 0.33
        p66[0] = ll[0] + r * 0.66

        if direction[0] == -1:
            if close[0] > p33[0]:
                if math.isnan(h[-1]):
                    h[-1] = high[-1]
                h[0] = max(h[-1], high[0])
            elif high[0] < p33[0]:
                h[0] = float("nan")
        # h[0] = high[0]
        # if high[0] > p66[0]:
        #     hh[0] = high[0]
        #     h[0] = float("nan")
        #     direction[0] = 1

        elif direction[0] == 1:
            if low[0] < p66[0]:
                if math.isnan(l[-1]):
                    l[-1] = low[-1]
                l[0] = min(l[-1], low[0])
            if low[0] < p33[0]:
                ll[0] = low[0]
                l[0] = float("nan")
                direction[0] = -1
