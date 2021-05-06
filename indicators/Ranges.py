import math

import backtrader as bt


class Ranges(bt.Indicator):
    lines = ("lower", "higher")
    params = dict()
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.edges = self.data1
        self.hh = self.edges.l.refu
        self.ll = self.edges.l.ref

        self.edges_high = []
        self.edges_low = []

    def next(self):
        (hh, ll) = (self.hh, self.ll)
        (high, low, close) = (self.data.high, self.data.low, self.data.close)

        if hh[0] > 0:
            self.l.higher[0] = hh[0]
            self.edges_high.append(hh[0])
        else:
            self.l.higher[0] = self.l.higher[-1]
            # self.l.lower[0] = self.l.lower[-1]
        if high[0] > self.l.higher[0]:
            self.edges_high = []

        if ll[0] > 0:
            self.l.lower[0] = ll[0]
            self.edges_low.append(ll[0])
        else:
            self.l.lower[0] = self.l.lower[-1]
        if low[0] < self.l.lower[0]:
            # print(self.edges_low)
            self.edges_low = []





        # # if math.isnan(hh[0]) and math.isnan(ll[0]):
        # count = len(close) - 1
        #
        # arr = self.edges.edges_high
        # val = [edge for edge in arr if edge['index'] == count]

        # if len(val) > 0:
        #     curr = val[0]
        #     idx = arr.index(curr)
        #     prev = arr[idx - 1]
        #     if prev['value'] > curr['value']:
        #         self.l.higher[0] = prev['value']
        #         print(self.edges.edges_high)
        # print(count)
        # edges = [edge for edge in self.edges.edges_high if edge["index"] < count]
        # print(edges)

        # for i in range(-1, -count, -1):
        #     if ll[i] > 0 and ll[i] < low[i]:
        #         for j in range(i - 1, -count, -1):
        #             if hh[j] > 0:
        #                 print(hh[j])
        #                 for r in range(j, 0):
        #                     self.l.lower[r] = ll[i]
        #                     self.l.higher[r] = hh[j]
        #                 return
        #                 # print(hh[j])
        #                 # print(ll[i])
