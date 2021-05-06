import math

import backtrader as bt


class Direction(bt.Indicator):
    params = dict()
    lines = ("direction", "intermediate", "ll", "hh", "rlz")
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[1.0, 0, -1.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[1.0, -1.0],
    )

    plotlines = dict(
        direction=dict(
            color="black", ls="-", _fill_gt=(0, "green"), _fill_lt=(0, "red")
        ),
        intermediate=dict(color="gray", _plotskip=False),
        hh=dict(_plotskip=True),
        ll=dict(_plotskip=True),
        rlz=dict(_plotskip=True),
    )

    def __init__(self):
        self.Structure = self.data1.l.signal
        self.Internals = self.data2.l.signal
        self.Location = self.data3.l.price_location

        self.l.intermediate = self.Structure + self.Internals + self.Location

    def next(self):
        if math.isnan(self.hh[-1]):
            self.hh[0] = self.data.high[0]
            self.ll[0] = self.data.low[0]

        self.l.direction[0] = self.l.direction[-1]
        if self.l.intermediate[0] == 5:
            self.l.direction[0] = 1
        elif self.l.intermediate[0] == -5:
            self.l.direction[0] = -1

        curr = self.direction[0]

        if curr == 1:
            self.hh[0] = max(self.hh[-1], self.data.high[0])
            self.ll[0] = min(self.ll[-1], self.data.low[0])

            r = self.hh[0] - self.ll[0]
            self.l.rlz[0] = self.hh[0] - r * 0.786
            if self.data.close[0] < self.l.rlz[0]:
                self.direction[0] = -1

        elif curr == -1:
            self.hh[0] = max(self.hh[-1], self.data.high[0])
            self.ll[0] = min(self.ll[-1], self.data.low[0])

            r = self.hh[0] - self.ll[0]
            self.l.rlz[0] = self.ll[0] + r * 0.786
            if self.data.close[0] > self.l.rlz[0]:
                self.hh[0] = self.data.high[0]
                self.direction[0] = 1

        curr = self.direction[0]
        if curr != self.direction[-1]:
            if curr == 1:
                self.hh[0] = self.data.high[0]
            elif curr == -1:
                self.ll[0] = self.data.low[0]
                self.hh[0] = self.hh[-1]
