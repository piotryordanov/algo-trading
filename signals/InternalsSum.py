import math
import backtrader as bt

class InternalsSum(bt.Indicator):
    params = dict(threshold=3)
    lines = ("signal", )
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[3.0, -3.0],
    )

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(
        signal=dict(color="black", ls="-"),
    )

    def __init__(self):
        self.short = self.data.l.signal
        self.long = self.data1.l.signal

    def next(self):
        (prev, l, short, th) = (self.l.signal[-1], self.long[0], self.short[0], self.p.threshold)

        longflip = self.long[-1] != l and abs(l) == th
        shortflip = self.short[-1] != short and abs(short) == th

        if math.isnan(prev):
            self.l.signal[0] = 0
        else:
            self.l.signal[0] = self.l.signal[-1]

        if longflip:
            self.l.signal[0] = l
        elif shortflip:
            self.l.signal[0] = short

        if abs(short) != th and abs(l) == th:
            self.l.signal[0] = l
        elif abs(l) != th and abs(short) == th:
            self.l.signal[0] = short
        # if prev != short:
        #     self.l.signal[0] = short
        # if self.long[0] == 3 or self.short[0] == 3:
        #     self.l.signal[0] = 1
        # elif self.long[0] == -3 or self.short[0] == -3:
        #     self.l.signal[0] = -1
