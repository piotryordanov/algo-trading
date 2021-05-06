import backtrader as bt
import backtrader.indicators as btind

class Trail_ATR(bt.ind.PeriodN):
    _mindatas = 1
    lines = ('lowest', 'highest', 'atr_lower_ref', 'atr_upper_ref')

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        highest=dict(color='black', fillstyle='full', ls='-'),
        atr_upper_ref=dict(color='gray', fillstyle='full', ls='-'),
        lowest=dict(color='black', fillstyle='full', ls='-'),
        atr_lower_ref=dict(color='gray', fillstyle='full', ls='-'),
    )

    params = (
        ('period', 14),
        ('multiplier', 2),
        ('showReference', False),
    )
    def __init__(self):
        self.atr_base = btind.ATR(period=self.p.period)

    def next(self):
        # close = self.data.close[0]
        low = self.data.low[0]
        high = self.data.high[0]

        # ### Upper Reference
        highest = self.atr_base[0] * self.p.multiplier
        upper = high + highest

        if self.highest[-1] != self.highest[-1]:
            self.highest[0] = upper
        elif upper > high and upper < self.highest[-1]:
            self.highest[0] = upper
        elif self.highest[-1] < high:
            self.highest[0] = upper
        else:
            self.highest[0] = self.highest[-1]
        
        ### Lower Reference
        lowest = self.atr_base[0] * self.p.multiplier
        lower = low - lowest

        if self.lowest[-1] != self.lowest[-1]:
            self.lowest[0] = lower
        elif lower < low and lower > self.lowest[-1]:
            self.lowest[0] = lower
        elif self.lowest[-1] > low:
            self.lowest[0] = lower
        else:
            self.lowest[0] = self.lowest[-1]

        ## Reference
        if self.p.showReference:
            self.atr_upper_ref[0] = upper
            self.atr_lower_ref[0] = lower
