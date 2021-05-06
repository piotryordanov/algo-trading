import math
from datetime import datetime

import backtrader as bt

from Settings import Fractal_Left_Shift, Fractal_Right_Shift
from indicators.ATR import ATR


class Fractal_161(bt.Indicator):
    lines = (
        "fractal_bearish",
        "fractal_bullish",
        "fractal_bearish_lh",
        "fractal_bearish_hh",
        "fractal_bullish_ll",
        "fractal_bullish_hl",
        "intermediates_up",
        "intermediates_down",
        "double_top",
        "double_bottom",
    )

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        fractal_bearish_hh=dict(
            marker="$HH$", markersize=12.0, color="red", fillstyle="full", ls=""
        ),
        fractal_bearish_lh=dict(
            marker="$-$", markersize=10, color="gray", fillstyle="full", ls="", _plotskip=False
        ),
        fractal_bullish_ll=dict(
            marker="$LL$", markersize=12, color="lime", fillstyle="full", ls=""
        ),
        fractal_bullish_hl=dict(
            marker="$-$", markersize=10, color="gray", fillstyle="full", ls="", _plotskip=True
        ),
        intermediates_up=dict(
            marker="$-$", markersize=10, color="red", fillstyle="full"
        ),
        intermediates_down=dict(
            marker="$-$", markersize=10, color="lime", fillstyle="full"
        ),
        double_top=dict( color="black", fillstyle="full"),
        double_bottom=dict( color="black", fillstyle="full"),
    )

    params = dict(
        bardist=0.0003,
        left_shift=Fractal_Left_Shift,
        right_shift=Fractal_Right_Shift,
        filter_doubles=False
    )

    def __init__(self):
        self.shift = self.p.left_shift + self.p.right_shift + 1
        self.addminperiod(self.shift)
        self.inter = dict()
        self.ll = list()
        self.hh = list()
        self.ATR = ATR(period=self.p.left_shift)

    def find_intermediates(self, t):
        if t == "ll":
            s = self.ll
            if len(s) > 1:
                for i in range(0, len(s) - 1):
                    (a, b) = (s[i], s[len(s) - 1])

                    if a["val"] > b["val"]:
                        (a, b) = (a['idx'], b['idx'])
                        count = abs(a - b) + self.p.right_shift
                        last_highs = self.data.high.get(size=count)
                        max_val = max(last_highs)
                        max_idx = last_highs.index(max_val) - count
                        # self.l.intermediates_up[max_idx + 1] = max_val
                        self.l.intermediates_up[0] = max_val
        else:
            s = self.hh
            if len(s) > 1:
                for i in range(0, len(s) - 1):
                    (a, b) = (s[i], s[len(s) - 1])

                    if a["val"] < b["val"]:
                        (a, b) = (a['idx'], b['idx'])
                        count = abs(a - b) + self.p.right_shift
                        last_lows = self.data.low.get(size=count)
                        min_val = min(last_lows)
                        min_idx = last_lows.index(min_val) - count
                        # self.l.intermediates_down[min_idx + 1] = min_val
                        self.l.intermediates_down[0] = min_val

    def update_intermediates_idx(self):
        for i in self.ll:
            i["idx"] -= 1
        for i in self.hh:
            i["idx"] -= 1

    def next(self):
        # A bearish turning point occurs when there is a pattern with the
        # highest high in the middle and two lower highs on each side. [Ref 1]
        # size = self.p.left_shift + self.p.right_shift
        self.update_intermediates_idx()
        last_highs = self.data.high.get(size=self.shift)
        max_val = max(last_highs)
        max_idx = self.shift - last_highs.index(max_val) - 1
        if max_idx == self.p.right_shift:
            self.lines.fractal_bearish[-max_idx] = max_val

            if self.p.filter_doubles:
                for i in range(max_idx + 1, len(self.data.close)):
                    previous = self.lines.fractal_bearish_hh[-i]
                    if previous > 0:
                        threshold = min(self.ATR[self.p.right_shift], 0.002)
                        if abs(max_val - previous) < threshold:
                            for j in range(max_idx + 1, i):
                                self.double_top[-j] = max(max_val, previous)
                            self.l.fractal_bearish_hh[-i] = 0
                        break

            for i in range(max_idx + 1, len(self.data.close)):
                previous = self.lines.fractal_bearish[-1 * i]
                val = max_val
                if previous > 0:
                    if previous < max_val:
                        self.lines.fractal_bearish_hh[-1 * max_idx] = val
                        self.hh.append(dict(idx=(-max_idx), val=max_val))
                        self.find_intermediates("hh")
                        break
                    else:
                        self.lines.fractal_bearish_lh[-1 * max_idx] = val
                        return
                elif i == len(self.data.high) - 1:
                    self.lines.fractal_bearish_hh[-1 * max_idx] = val
                    self.hh.append(dict(idx=(-max_idx), val=max_val))
                    self.find_intermediates("hh")


        last_lows = self.data.low.get(size=self.shift)
        min_val = min(last_lows)
        min_idx = self.shift - last_lows.index(min_val) - 1
        if min_idx == self.p.right_shift:
            self.l.fractal_bullish[-1 * min_idx] = min_val

            if self.p.filter_doubles:
                for i in range(min_idx + 1, len(self.data.close)):
                    previous = self.lines.fractal_bullish_ll[-i]
                    if previous > 0:
                        # if previous > min_val:
                        #     if abs(min_val - previous) < self.ATR[-self.p.right_shift]:
                        #         self.l.fractal_bullish_ll[-i] = 0
                        threshold = min(self.ATR[self.p.right_shift], 0.002)
                        if abs(previous - min_val) < threshold:
                            for j in range(min_idx, i):
                                self.double_bottom[-j] = min(min_val, previous)
                            self.l.fractal_bullish_ll[-i] = 0
                        break

            for i in range(min_idx + 1, len(self.data.close)):
                previous = self.lines.fractal_bullish[-1 * i]
                val = min_val
                if previous > 0:
                    if previous > min_val:
                        self.lines.fractal_bullish_ll[-1 * min_idx] = val
                        self.ll.append(dict(idx=(-1 * min_idx), val=min_val))
                        self.find_intermediates("ll")
                        break
                    else:
                        self.lines.fractal_bullish_hl[-1 * min_idx] = val
                        break
                elif i == len(self.data.high) - 1:
                    self.lines.fractal_bullish_ll[-1 * min_idx] = val
                    self.ll.append(dict(idx=(-1 * min_idx), val=min_val))
                    self.find_intermediates("ll")
