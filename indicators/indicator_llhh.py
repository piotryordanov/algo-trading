import backtrader as bt


class indicator_llhh(bt.Indicator):
    _mindatas = 2
    lines = ("lower", "upper", "sl", "e1", "p33", "p66", "target")
    params = dict(shift=4)

    plotinfo = dict(
        subplot=False,
        plotlinelabels=True,
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[2.0, -2.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[2.0, -2.0],
    )

    plotlines = dict(
        lower=dict( color="black", fillstyle="full", ls="-"),
        upper=dict( color="black", fillstyle="full", ls="-"),
        sl=dict(marker="$-$", markersize=12.0, color="pink", fillstyle="full", ls=""),
        e1=dict(marker="$-$", markersize=12.0, color="red", fillstyle="full", ls=""),
        p33=dict(color="lime", fillstyle="full", ls="-"),
        p66=dict(color="lime", fillstyle="full", ls="-"),
        target=dict(
            marker="$-$", markersize=12.0, color="blue", fillstyle="full", ls=""
        ),
    )

    def __init__(self):
        self.data = self.data
        self.fractal = self.data1
        self.shift = self.p.shift

        self.sl = 0
        self.reset()

    def draw_range(self):
        if self.ll > 0 and self.hh > 0:
            r = self.hh - self.ll

            close = self.data.close[0]
            p33 = self.ll + r / 3
            p66 = self.ll + r * 2 / 3

            self.l.upper[0] = self.hh
            self.l.lower[0] = self.ll
            self.l.p33[0] = p33
            self.l.p66[0] = p66

            if (close - p33) * (close - p66) < 0:
                if self.sl == 0 or self.sl > self.data.low[0]:
                    self.sl = self.data.low[0]

                self.l.sl[0] = self.sl
                self.l.target[0] = self.sl + r
                self.l.e1[0] = self.sl + r * 0.0625
            else:
                self.sl = 0
        else:
            self.sl = 0
        self.l.lower[0] = self.ll

    def reset(self):
        self.hh = 0
        self.ll = 0

    def next(self):
        hh = self.fractal.fractal_bearish_hh[-1 * self.shift]
        ll = self.fractal.fractal_bullish_ll[-1 * self.shift]

        ## State 1: Found first ll
        if self.ll == 0 and ll > 0:
            self.ll = ll

        if self.ll > 0:
            if self.data.low[0] < self.ll:
                self.ll = self.data.low[0]


        ## State 2: Found first hh after first ll
        if hh > 0 and self.ll > 0 and self.hh == 0:
            self.hh = hh

        ## LL broken
        if self.ll > 0 and self.data.low[0] < self.ll:
            self.ll = ll

        # ## Retrace > 66% of range
        if self.hh > 0 and self.ll > 0:
            r = self.hh - self.ll
            p66 = self.hh - r * 2 / 3
            if self.data.close[0] < p66:
                self.hh = self.data.high[0]
                self.ll = self.data.low[0]

        # ## Found a higher high
        if hh > self.hh and self.hh > 0:
            self.hh = hh

        if self.data.high[0] > self.hh and self.hh != 0:
            self.hh = self.data.high[0]

        # Found a new ll within a range. Break previous range, start new range
        # if self.hh > 0 and self.ll > 0 and ll > 0:
        #     self.reset()
        #     self.ll = ll

        self.draw_range()
