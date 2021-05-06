from datetime import datetime

import backtrader as bt
from Settings import Fractal_Right_Shift, Fractal_Left_Shift


color = 'red'
marker = '$-$'

class FillFractal(bt.Indicator):
    lines = (
        "fractal_bearish",
        "fractal_bullish",
    )

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        fractal_bearish=dict(
            marker=marker, markersize=12.0, color=color, fillstyle="full"
        ),
        fractal_bullish=dict(
            marker=marker, markersize=12, color=color, fillstyle="full"
        ),
    )

    params = dict(bardist=0.0003, left_shift=Fractal_Left_Shift, right_shift=Fractal_Right_Shift)

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

        last_lows = self.data.low.get(size=self.shift)
        min_val = min(last_lows)
        min_idx = self.shift - last_lows.index(min_val) - 1
        if min_idx == self.p.right_shift:
            self.l.fractal_bullish[-1 * min_idx] = min_val
