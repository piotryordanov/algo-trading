import math

import backtrader as bt

debug = False
debug = True


class EdgeFractal(bt.Indicator):
    lines = ("hh", "ll", "hline", "lline", "oph", "opl", "p33", "p66", "ref", "refu")

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        hh=dict(marker="$-$", color="black", markersize=15, fillstyle="full", ls=""),
        ll=dict(marker="$-$", color="black", markersize=15, fillstyle="full", ls=""),
        ref=dict(marker="$-$", color="red", markersize=10, fillstyle="full", ls=""),
        refu=dict(marker="$-$", color="lime", markersize=10, fillstyle="full", ls=""),
        oph=dict(marker="$OPH$", color="black", markersize=10, _plotskip=debug),
        opl=dict(marker="$OPL$", color="black", markersize=10, _plotskip=debug),
        lline=dict(_plotskip=debug),
        hline=dict(_plotskip=debug),
        p33=dict(color="green", _plotskip=debug),
        p66=dict(color="green", _plotskip=debug),
    )

    def _plotinit(self):
        pass

    params = dict(initial=2)

    def __init__(self):
        self.high = 0
        self.low = 0
        self.idx_low = 1
        self.idx_high = 1

    def next(self):
        if len(self.data.close) < self.p.initial:
            return

        (hh, ll) = self.l.hh, self.l.ll
        (high, low, close) = (self.data.high, self.data.low, self.data.close)

        if len(self.data.close) == self.p.initial:
            self.high = high[0]
            self.low = low[0]

        if self.high < high[0]:
            self.idx = self.idx_high
            last_lows = low.get(size=self.idx)
            min_val = min(last_lows)
            last_low_indx = last_lows.index(min_val)
            idx = self.idx - last_low_indx
            if self.idx > 3:
                if high[-self.idx] == self.high and min_val < low[-self.idx]:
                    if math.isnan(hh[-self.idx]):
                        hh[-self.idx] = max(self.high, high[-self.idx])
                        ll[-idx + 1] = min_val
                        self.low = min_val
                        self.oph[0] = high[0]

                        self.l.refu[0] = hh[-self.idx]
                        self.l.ref[0] = min_val
                else:
                    if self.high == high[-self.idx_high]:
                        hh[-self.idx_high] = self.high

                        self.l.refu[0] = self.high

            # Used when a trend reverses
            if (low[-self.idx_low] == self.low) and (math.isnan(ll[-self.idx_low])):
                ll[-self.idx_low] = self.low
                self.l.ref[0] = self.low

            self.high = high[0]
            self.idx_high = 0

        elif self.low > low[0]:
            self.idx = self.idx_low
            last_highs = high.get(size=self.idx)
            max_val = max(last_highs)
            max_val_indx = last_highs.index(max_val)
            idx = self.idx - max_val_indx
            if self.idx > 3:
                if low[-self.idx] == self.low and max_val > high[-self.idx]:
                    if math.isnan(ll[-self.idx]):
                        hh[-idx + 1] = max_val
                        ll[-self.idx] = min(self.low, low[-self.idx])
                        self.high = max_val
                        # self.opl[0] = low[0]

                        self.l.refu[0] = max_val
                        self.l.ref[0] = ll[-self.idx]
                else:
                    if self.low == low[-self.idx_low]:
                        ll[-self.idx_low] = self.low

                        self.l.ref[0] = self.low

            # Used when a trend reverses
            if (high[-self.idx_high] == self.high) and (math.isnan(hh[-self.idx_high])):
                hh[-self.idx_high] = self.high

                self.l.refu[0] = self.high

            self.low = low[0]
            self.idx_low = 0

        self.lline[0] = self.low
        self.hline[0] = self.high
        self.idx_high += 1
        self.idx_low += 1

        r = self.high - self.low
        self.l.p33[0] = self.high - r * 0.33
        self.l.p66[0] = self.high - r * 0.66
