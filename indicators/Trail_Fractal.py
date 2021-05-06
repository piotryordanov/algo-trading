import backtrader as bt
import backtrader.indicators as btind
from Settings import Fractal_Right_Shift

class Trail_Fractal(bt.ind.PeriodN):
    _mindatas = 2
    lines = ('lowest', 'highest', 'fractal_bearish_lh', 'fractal_bearish_hh', 'fractal_bullish_ll', 'fractal_bullish_hl')

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        lowest=dict(color='gray', fillstyle='full', ls='-'),
        highest=dict(color='gray', fillstyle='full', ls='-'),
    )

    def __init__(self):
        self.shift = Fractal_Right_Shift * -1
        self.fractal = self.data1

    def next(self):
        bullish = self.fractal.fractal_bullish[self.shift]
        bearish = self.fractal.fractal_bearish[self.shift]

        low = self.data.low[0]
        high = self.data.high[0]

        ## Lower
        if self.lowest[-1] != self.lowest[-1]:
            self.lowest[0] = self.data.low[self.shift]
        elif bullish > 0:
            self.lowest[0] = self.data.low[self.shift]
        elif low < self.lowest[-1]:
            self.lowest[0] = low
        else:
            self.lowest[0] = self.lowest[-1]

        ## Higher
        if self.highest[-1] != self.highest[-1]:
            self.highest[0] = self.data.high[self.shift]
        elif bearish > 0:
            self.highest[0] = self.data.high[self.shift]
        elif high > self.highest[-1]:
            self.highest[0] = high
        else:
            self.highest[0] = self.highest[-1]
