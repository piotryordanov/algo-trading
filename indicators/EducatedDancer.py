import backtrader as bt
import backtrader.indicators as btind

class EducatedDancer(bt.Indicator):
    _mindatas = 3
    lines = ('upper', 'lower', 'p33', 'p66', 't66', 'target', 'signal_short', 'signal_long')
    params = dict(
        shift=4
    )
    plotinfo = dict(
        subplot=False,
        plotlinelabels=True,
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[2.0, -2.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[2.0, -2.0])

    plotlines = dict(
        lower=dict(marker='$-$', markersize=14.0, color='black', fillstyle='full', ls=''),
        upper=dict(marker='$-$', markersize=14.0, color='black', fillstyle='full', ls=''),
        p33=dict(marker='$-$', markersize=14.0, color='lime', fillstyle='full', ls=''),
        p66=dict(marker='$-$', markersize=14.0, color='lime', fillstyle='full', ls=''),
        target=dict(marker='$-$', markersize=14.0, color='orange', fillstyle='full', ls=''),
        t66=dict(marker='$-$', markersize=14.0, color='blue', fillstyle='full', ls=''),
        signal_short=dict(marker='v', markersize=14.0, color='red', fillstyle='full', ls=''),
        signal_long=dict(marker='^', markersize=14.0, color='lime', fillstyle='full', ls=''),
    )


    def __init__(self):
        self.data = self.data
        self.fractal = self.data1
        self.gambler = self.data2
        self.shift = self.p.shift

        self.range = dict(high=0, low=0)
        self.ranges = list()

    def is_range_valid(self, Range):
        return not (self.data.high[0] > Range['upper'] or self.data.low[0] < Range['lower'])

    def find_signal(self, Range):
        close = self.data.close[0]
        high = Range['upper']
        low = Range['lower']
        r = high - low
        p33 = low + r / 3
        p66 = low + r * 2 / 3
        if (close - p33) * (close - p66) < 0:
            Type = Range['Type']
            if Type == 'll_hh' or Type == 'hh_continuation':
                self.lines.signal_long[0] = close
                self.lines.target[0] = self.data.high[0] + r
                self.lines.t66[0] = self.data.high[0] + r * 0.66
            else:
                self.lines.signal_short[0] = close
                self.lines.target[0] = self.data.high[0] - r
                self.lines.t66[0] = self.data.high[0] - r * 0.66


    def add_new_range(self, upper, lower, Type):
        r=upper - lower
        NewRange = dict(
            upper=upper,
            lower=lower,
            r=upper - lower,
            p33=lower + r / 3,
            p66=lower + r * 2 / 3,
            Type=Type
        )
        self.ranges.append(NewRange)
        self.paint_range(NewRange)

    def paint_range(self, Range):
        if Range:
            self.lines.upper[0] = Range['upper']
            self.lines.lower[0] = Range['lower']
            self.lines.p33[0] = Range['p33']
            self.lines.p66[0] = Range['p66']

    def next(self):
        for r in self.ranges:
            if not self.is_range_valid(r):
                self.ranges.remove(r)
        if len(self.ranges) > 0:
            latestRange = self.ranges[-1]
            self.paint_range(latestRange)
            self.find_signal(latestRange)


        if self.gambler.lines.ll_hh[0] == 2:
            upper = self.data.high[-1 * self.shift]
            lower = self.gambler.l.sibling_ll_hh[0]
            self.add_new_range(upper, lower, 'll_hh')

        if self.gambler.lines.hh_ll[0] == 2:
            lower = self.data.low[-1 * self.shift]
            upper = self.gambler.l.sibling_hh_ll[0]
            self.add_new_range(upper, lower, 'hh_ll')

        if self.gambler.lines.hh_continuation[0] == 2:
            upper = self.data.high[-1 * self.shift]
            lower = self.gambler.l.sibling_hh_continuation[0]
            self.add_new_range(upper, lower, 'hh_continuation')

        if self.gambler.lines.ll_continuation[0] == -2:
            upper = self.gambler.l.sibling_ll_continuation[0]
            lower = self.data.low[-1 * self.shift]
            self.add_new_range(upper, lower, 'll_continuation')
