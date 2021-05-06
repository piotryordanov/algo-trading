import math

import backtrader as bt


class PRZ(bt.Indicator):
    lines = ("hh", "p66H", "przH", "ll", "przL", "p66L")
    params = dict()
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.edges = self.data1
        self.hh = self.edges.l.refu
        self.ll = self.edges.l.ref
        self.direction = 0
        self.count = 0

    def next(self):
        (hh, ll, direction) = (self.hh, self.ll, self.direction)
        (high, low, close) = (self.data.high, self.data.low, self.data.close)

        for line in self.l.lines:
            line[0] = line[-1]

        (h, l) = (self.l.hh[0], self.l.ll[0])
        if low[0] < l:
            self.direction = -1
        if high[0] > h:
            self.direction = 1
        self.l.hh[0] = max(high[0], self.l.hh[0], hh[0])
        self.l.ll[0] = min(low[0], self.l.ll[0], ll[0])

        r = h - l
        przH = l + r * 0.786
        p66H = l + r * 0.66
        przL = h - r * 0.786
        p66L = h - r * 0.66
        if direction == 1:
            if low[0] < self.l.przL[-1]:
                self.l.przH[0] = przH
                self.l.przL[0] = float("nan")
                self.l.p66H[0] = p66H
                self.l.p66L[0] = float("nan")
                self.l.ll[0] = low[0]
            else:
                self.l.przH[0] = float("nan")
                self.l.przL[0] = przL
                self.l.p66H[0] = float("nan")
                self.l.p66L[0] = p66L
        else:
            if high[0] > self.l.przH[-1]:
                self.l.przH[0] = float("nan")
                self.l.przL[0] = przL
                self.l.p66H[0] = float("nan")
                self.l.p66L[0] = p66L
                self.l.hh[0] = high[0]
            else:
                self.l.przH[0] = przH
                self.l.przL[0] = float("nan")
                self.l.p66H[0] = p66H
                self.l.p66L[0] = float("nan")

