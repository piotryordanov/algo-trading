import math

import backtrader as bt


class Lines_161(bt.Indicator):
    lines = ("ll", "hh", "rlz", "direction")

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict()

    params = dict(shift=10)

    def __init__(self):
        f = self.data1.l
        self.ll = f.fractal_bullish_ll
        self.hh = f.fractal_bearish_hh
        self.inter_up = f.intermediates_up
        self.inter_down = f.intermediates_down
        self.intermediates = list()

    def next(self):
        shift = -self.p.shift
        ll = self.ll[shift]
        hh = self.hh[shift]
        (low, high) = (self.data.low[0], self.data.high[0])
        (prev_ll, prev_hh) = (self.l.ll[-1], self.l.hh[-1])

        ## Init
        if math.isnan(prev_ll):
            prev_ll = low
        if math.isnan(ll) > 0:
            ll = low
        if math.isnan(prev_hh):
            prev_hh = high
        if math.isnan(hh) > 0:
            hh = high

        ## Set new Boundaries
        self.l.ll[0] = min(ll, low, prev_ll)
        self.l.hh[0] = max(hh, high, prev_hh)
        curr_ll = self.l.ll[0]
        curr_hh = self.l.hh[0]

        a = self.inter_down[0]
        if a > 0:
            self.intermediates.append(a)
            self.intermediates = list(set(self.intermediates))
            self.intermediates.sort()
            self.l.ll[0] = a
            # print(self.l.ll[0])

        self.l.direction[0] = 1

        inter = self.intermediates

        # if low < self.l.ll[-1] and len(inter) > 2:
        #     for a in inter:
        #         if a > low:
        #             inter.remove(a)
        #     self.l.ll[0] = inter[len(inter) - 1]
        #
        r = abs(curr_hh - curr_ll)
        p66 = curr_ll + r * 0.33
        if low < p66 and len(inter) > 1:
            print("====")
            print(low)
            print(p66)
            print(curr_ll)
            print(inter)
            print(inter.pop())
            print(inter)
            self.intermediates = inter
            self.l.ll[0] = inter[len(inter) - 1]
            print(self.l.ll[0])

        # p33 = a + range * 0.66
        # if low < p33:
        #     self.l.ll[0] = a
        #     return

        if len(inter) > 4:
            self.l.ll[0] = inter[2]

        Range = self.l.hh[0] - self.l.ll[0]
        self.l.rlz[0] = self.l.hh[0] - Range * 0.786
        #
        # # for a in inter:
        # #     if low < a:
        # #         inter.remove(a)
        # if len(inter) > 2:
        #     # self.l.ll[0] = inter[len(inter) - 2]
        #     for a in inter:
        #         range = self.l.hh[0] - a
        #         p33 = a + range * 0.66
        #         if low < p33:
        #             self.l.ll[0] = a
        #             return
