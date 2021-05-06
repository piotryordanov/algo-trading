from datetime import datetime
import backtrader as bt

class SpecialFractal(bt.Indicator):
    lines = ('fractal_bearish', 'fractal_bullish', 'fractal_bearish_lh', 'fractal_bearish_hh', 'fractal_bullish_ll', 'fractal_bullish_hl')

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        # fractal_bearish=dict(marker='^', markersize=6.0, color='black', fillstyle='full', ls=''),
        fractal_bearish_hh=dict(marker='$HH$', markersize=12.0, color='black', fillstyle='full', ls=''),
        fractal_bearish_lh=dict(marker='$LH$', markersize=12, color='black', fillstyle='full', ls=''),
        fractal_bullish_ll=dict(marker='$LL$', markersize=12, color='black', fillstyle='full', ls=''),
        fractal_bullish_hl=dict(marker='$HL$', markersize=12, color='black', fillstyle='full', ls=''),
    )

    params = dict(
        bardist=0.0003,
        left_shift=10,
        right_shift=4
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
            self.lines.fractal_bearish[-1 * max_idx] = max_val * (1 + self.p.bardist)
            for i in range(max_idx + 1, len(self.data.high)):
                previous = self.lines.fractal_bearish[-1 * i]
                if previous > 0:
                    if previous < max_val:
                        self.lines.fractal_bearish_hh[-1 * max_idx] = max_val * (1 + self.p.bardist)
                        break
                    else:
                        self.lines.fractal_bearish_lh[-1 * max_idx] = max_val * (1 + self.p.bardist)
                        break
                elif i == len(self.data.high) - 1:
                    self.lines.fractal_bearish_hh[-1 * max_idx] = max_val * (1 + self.p.bardist)

        last_lows = self.data.low.get(size=self.shift)
        min_val = min(last_lows)
        min_idx = self.shift - last_lows.index(min_val) - 1
        if min_idx == self.p.right_shift:
            self.l.fractal_bullish[-1 * min_idx] = min_val * (1 - self.p.bardist)
            for i in range(min_idx + 1, len(self.data.high)):
                previous = self.lines.fractal_bullish[-1 * i]
                if previous > 0:
                    if previous > min_val:
                        self.lines.fractal_bullish_ll[-1 * min_idx] = min_val * (1 - self.p.bardist)
                        break
                    else:
                        self.lines.fractal_bullish_hl[-1 * min_idx] = min_val * (1 - self.p.bardist)
                        break
                elif i == len(self.data.high) - 1:
                    self.lines.fractal_bullish_ll[-1 * min_idx] = min_val * (1 - self.p.bardist)
