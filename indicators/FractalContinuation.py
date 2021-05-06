import backtrader as bt
import backtrader.indicators as btind
from indicators.Fractal import Fractal

class FractalContinuation(bt.Indicator):
    _mindatas = 2
    lines = ('retrace', 'll_continuation', 'hh_continuation', 'll_hh', 'hh_ll',
            'sibling_hh_ll', 'sibling_ll_hh', 'sibling_hh_continuation',
             'sibling_ll_continuation')
    params = dict(
        shift=4
    )

    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[2.0, -2.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[2.0, -2.0])

    plotlines = dict(
        ll_continuation=dict(color='red', ls='-'),
        hh_continuation=dict(color='green', ls='-'),
        ll_hh=dict(color='orange', ls='-'),
        hh_ll=dict(color='blue', ls='-'),
        retrace=dict(color='black', ls='--'),
    )


    def __init__(self):
        self.data = self.data
        self.fractal = self.data1
        self.shift = self.p.shift


        self.last = ''
        self.last_hh_sibling = 0
        self.last_ll_sibling = 0

    def find_min(self):
        for i in range(0 + 1, len(self.data.close)):
            current = self.fractal.fractal_bearish_hh[-1* (i + self.shift)]
            if current > 0:
                lows = self.data.low.get(size=i+self.shift)
                low = min(lows[0:len(lows)-self.p.shift])
                return low

    def find_max(self):
        for i in range(0 + 1, len(self.data.close)):
            current = self.fractal.fractal_bullish_ll[-1* (i + self.shift)]
            if current > 0:
                highs = self.data.high.get(size=i+self.shift)
                high = max(highs[0:len(highs)-self.p.shift])
                return high

    def next(self):
        hh = self.fractal.fractal_bearish_hh[-1 * self.shift]
        high = self.data.high[-1 * self.shift]
        ll = self.fractal.fractal_bullish_ll[-1 * self.shift]
        low = self.data.low[-1 * self.shift]
        if hh > 0:
            self.retrace[0] = 1
            if self.last == 'll':
                self.last = 'hh'
                self.lines.hh_continuation[0] = 1
                self.lines.ll_hh[0] = 2
                self.lines.sibling_ll_hh[0] = self.last_ll_sibling
            elif self.last == 'hh':
                self.lines.sibling_hh_continuation[0] = self.find_min()
                self.lines.hh_continuation[0] = 2
            else:
                self.lines.sibling_hh_continuation[0] = self.last_hh_sibling
                self.last = 'hh'
            self.last_hh_sibling = high

        elif ll > 0:
            self.retrace[0] = -1
            if self.last == 'hh':
                self.last = 'll'
                self.lines.ll_continuation[0] = -1
                self.lines.hh_ll[0] = 2
                self.lines.sibling_hh_ll[0] = self.last_hh_sibling
            elif self.last == 'll':
                self.lines.sibling_ll_continuation[0] = self.find_max()
                self.lines.ll_continuation[0] = -2
            else:
                self.last = 'll'
            self.last_ll_sibling = low
        else:
            for line in self.lines:
                line[0] = 0
