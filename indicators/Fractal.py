from datetime import datetime

import backtrader as bt

from Settings import Fractal_Left_Shift, Fractal_Right_Shift


class Fractal(bt.Indicator):
    lines = (
        "fractal_bearish",
        "fractal_bullish",
        "fractal_bearish_lh",
        "fractal_bearish_hh",
        "fractal_bullish_ll",
        "fractal_bullish_hl",
        "fractal_bearish_lh_draw",
        "fractal_bearish_hh_draw",
        "fractal_bullish_ll_draw",
        "fractal_bullish_hl_draw",
        "dot",
    )

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        # fractal_bearish=dict(marker='^', markersize=6.0, color='black', fillstyle='full', ls=''),
        fractal_bearish_hh_draw=dict(
            marker="$HH$", markersize=12.0, color="red", fillstyle="full", ls=""
        ),
        fractal_bearish_lh_draw=dict(
            marker="$LH$", markersize=10, color="orange", fillstyle="full", ls=""
        ),
        fractal_bullish_ll_draw=dict(
            marker="$LL$", markersize=12, color="lime", fillstyle="full", ls=""
        ),
        fractal_bullish_hl_draw=dict(
            marker="$HL$", markersize=10, color="green", fillstyle="full", ls=""
        ),
        dot=dict(marker="v", markersize=4, color="gray", fillstyle="full"),
        fractal_bearish=dict(_plotshow=False),
        fractal_bullish=dict(_plotshow=False),
        fractal_bearish_hh=dict(_plotshow=False),
        fractal_bearish_lh=dict(_plotshow=False),
        fractal_bullish_ll=dict(_plotshow=False),
        fractal_bullish_hl=dict(_plotshow=False),
    )

    def _plotinit(self):
        if self.p.marker != "":
            self.plotlines.fractal_bearish_hh_draw.marker = self.p.marker
            self.plotlines.fractal_bearish_lh_draw.marker = self.p.marker
            self.plotlines.fractal_bullish_ll_draw.marker = self.p.marker
            self.plotlines.fractal_bullish_hl_draw.marker = self.p.marker

            color = self.p.marker_color
            self.plotlines.fractal_bearish_hh_draw.color = color
            self.plotlines.fractal_bearish_lh_draw.color = color
            self.plotlines.fractal_bullish_ll_draw.color = color
            self.plotlines.fractal_bullish_hl_draw.color = color

    params = dict(
        bardist=0.0003,
        left_shift=Fractal_Left_Shift,
        right_shift=Fractal_Right_Shift,
        marker="",
        marker_color="black",
        show_dot=False,
    )

    def __init__(self):
        self.shift = self.p.left_shift + self.p.right_shift + 1
        self.addminperiod(self.shift)

    def next(self):
        # A bearish turning point occurs when there is a pattern with the
        # highest high in the middle and two lower highs on each side. [Ref 1]
        # size = self.p.left_shift + self.p.right_shift
        last_highs = self.data.high.get(size=self.shift)
        max_val = max(last_highs)
        max_idx = self.shift - last_highs.index(max_val) - 1
        if max_idx == self.p.right_shift:
            self.lines.fractal_bearish[-1 * max_idx] = max_val
            if self.p.show_dot:
                self.l.dot[0] = self.data.high[0] * (1 + 0.0007)

            for i in range(max_idx + 1, len(self.data.close)):
                previous = self.lines.fractal_bearish[-1 * i]
                val = max_val
                if previous > 0:
                    if previous < max_val:
                        self.lines.fractal_bearish_hh[-1 * max_idx] = val
                        break
                    else:
                        self.lines.fractal_bearish_lh[-1 * max_idx] = val
                        break
                elif i == len(self.data.high) - 1:
                    self.lines.fractal_bearish_hh[-1 * max_idx] = val

        last_lows = self.data.low.get(size=self.shift)
        min_val = min(last_lows)
        min_idx = self.shift - last_lows.index(min_val) - 1
        if min_idx == self.p.right_shift:
            self.l.fractal_bullish[-1 * min_idx] = min_val
            if self.p.show_dot:
                self.l.dot[0] = self.data.low[0] * (1 - 0.0007)

            for i in range(min_idx + 1, len(self.data.close)):
                previous = self.lines.fractal_bullish[-1 * i]
                val = min_val
                if previous > 0:
                    if previous > min_val:
                        self.lines.fractal_bullish_ll[-1 * min_idx] = val
                        break
                    else:
                        self.lines.fractal_bullish_hl[-1 * min_idx] = val
                        break
                elif i == len(self.data.high) - 1:
                    self.lines.fractal_bullish_ll[-1 * min_idx] = val

        i = -1 * self.p.right_shift
        self.l.fractal_bearish_hh_draw[i] = self.l.fractal_bearish_hh[i] * (
            1 + self.p.bardist
        )
        self.l.fractal_bearish_lh_draw[i] = self.l.fractal_bearish_lh[i] * (
            1 + self.p.bardist
        )
        self.l.fractal_bullish_ll_draw[i] = self.l.fractal_bullish_ll[i] * (
            1 - self.p.bardist
        )
        self.l.fractal_bullish_hl_draw[i] = self.l.fractal_bullish_hl[i] * (
            1 - self.p.bardist
        )
