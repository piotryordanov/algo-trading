import math

import backtrader as bt
from scipy import stats


class LinearRegression(bt.Indicator):
    lines = ("slope", "line")

    plotinfo = dict(subplot=False)

    plotlines = dict(line=dict(color="black"), slope=dict(_plotskip=True))

    def __init__(self):
        self.prz = self.data1.l
        self.count = 0
        self.tranches = 100

    def find_slope(self, X, Y, start):
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        self.l.slope[0] = abs(slope * 100000)
        for i in range(start, start + self.tranches):
            self.l.line[-i] = (start + self.tranches - i) * slope + intercept

    def next(self):
        if self.prz.ll[0] == self.prz.ll[-1] and self.prz.hh[0] == self.prz.hh[-1]:
            self.count += 1
        else:
            self.count = 0

        if self.count > 50:
            count = self.count
            X = list()
            for i in range(1, count + 1):
                X.append(i)
            # X = self.data.datetime.get(size=count)
            Y = self.data.close.get(size=count)
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
            self.l.slope[0] = abs(slope * 100000)
            for i in range(0, count):
                self.l.line[-i] = (count - i) * slope + intercept

            # f = lambda A, n=self.tranches: [A[i : i + n] for i in range(0, len(A), n)]
            # X = f(X)
            # Y = f(Y)
            # for i in range(0, len(X)):
            #     self.find_slope(X[i], Y[i], i * self.tranches)
        else:
            self.l.slope[0] = 40
