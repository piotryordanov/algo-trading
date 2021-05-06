import backtrader as bt


class WilliamSignal(bt.Indicator):
    params = dict()
    lines = ("price_location", "ma_direction", "ma_cross", "signal")
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[2.0, 0, -2.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[2.0, -2.0],
    )

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(
        ma_direction=dict(ls="--", _plotskip=True),
        price_location=dict(ls="--", _plotskip=True),
        ma_cross=dict(color="orange", ls="--"),
        signal=dict(color="black"),
    )

    def __init__(self):
        self.jaw = self.data1.l.jaw
        self.teeth = self.data1.l.teeth
        self.lips = self.data1.l.lips
        self.ADX = self.data2.l.adx

    def next(self):
        a = self.jaw[0]
        b = self.teeth[0]
        c = self.lips[0]

        self.l.ma_direction[0] = 0
        self.l.price_location[0] = 0
        self.l.ma_cross[0] = 0
        self.l.signal[0] = 0

        if a < b and b < c and a < c:
            self.l.ma_direction[0] = 1
        elif a > b and b > c and a > c:
            self.l.ma_direction[0] = -1

        close = self.data.close[0]
        if close > a and close > b and close > c:
            self.price_location[0] = 1
        elif close < a and close < b and close < c:
            self.price_location[0] = -1

        if (self.data.close[0] - self.jaw[0]) * (
            self.data.close[-1] - self.jaw[-1]
        ) < 0:
            if self.data.close[0] < self.jaw[0]:
                self.l.ma_cross[0] = -1
            else:
                self.l.ma_cross[0] = 1

        if self.ADX[0] > 20:
            self.l.signal[0] = self.l.ma_cross[0]
