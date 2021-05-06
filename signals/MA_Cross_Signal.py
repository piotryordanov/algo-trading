import backtrader as bt
import backtrader.indicators as btind


class MA_Cross_Signal(bt.Indicator):
    params = dict(min_window=40)
    lines = ("ma_cross",)
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[1.0, 0, -1.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[1.0, -1.0],
    )

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(ma_cross=dict(color="black", ls="--"))

    def __init__(self):
        self.ma = self.data1

    def next(self):
        self.l.ma_cross[0] = 0
        if (self.data.close[0] - self.ma[0]) * (self.data.close[-1] - self.ma[-1]) < 0:
            signals = self.l.ma_cross.get(size=self.p.min_window)

            if self.data.close[0] < self.ma[0]:
                for i in signals:
                    if i == -1:
                        return
                self.l.ma_cross[0] = -1
            else:
                for i in signals:
                    if i == 1:
                        return
                self.l.ma_cross[0] = 1
