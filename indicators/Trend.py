import math
import backtrader as bt
import backtrader.indicators as btind

from Settings import Fractal_Right_Shift, Fractal_Left_Shift


class Trend(bt.Indicator):
    _mindatas = 3
    lines = ("lower", "upper", "p50", "p33", "p66", "p786", 'sl', 'e1', 'target')
    params = dict()

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
        lower=dict(color="black", fillstyle="full", ls="-"),
        upper=dict(color="black", fillstyle="full", ls="-"),
        p33=dict(color="lime", fillstyle="full", ls="-"),
        p50=dict(color="cyan", fillstyle="full", ls="-"),
        p66=dict(color="lime", fillstyle="full", ls="-"),
        p786=dict(color="purple", fillstyle="full", ls="-"),
        sl=dict(marker="$-$", markersize=12.0, color="pink", fillstyle="full", ls=""),
        e1=dict(marker="$-$", markersize=12.0, color="red", fillstyle="full", ls=""),
        target=dict(marker="$-$", markersize=12.0, color="blue", fillstyle="full", ls=""),
    )

    def __init__(self):
        self.data = self.data
        self.Direction = self.data1
        self.sl = 0

    def draw_range(self, direction, rlz):
        if self.ll > 0 and self.hh > 0:
            r = self.hh - self.ll

            close = self.data.close[0]
            open = self.data.open[0]
            if direction == 1:
                p33 = self.hh - r / 3
                p66 = self.hh - r * 2 / 3
            else:
                p33 = self.ll + r / 3
                p66 = self.ll + r * 2 / 3
            p50 = self.ll + r/2

            self.l.upper[0] = self.hh
            self.l.lower[0] = self.ll
            self.l.p33[0] = min(p33, p66)
            self.l.p50[0] = p50
            self.l.p66[0] = max(p33, p66)
            self.l.p786[0] = rlz
            if ((close - p33) * (close - rlz) < 0) or ((open - p33) * (open -rlz) < 0 ):
                if direction == 1:
                    prev = self.sl
                    if self.sl == 0 or self.sl > self.data.low[0]:
                        self.sl = self.data.low[0]
                    if prev != self.sl:
                        self.l.sl[0] = self.sl
                        self.l.e1[0] = self.sl + r * 0.0625
                        self.l.target[0] = self.sl + r
                else:
                    prev = self.sl
                    self.sl = max(self.sl, self.data.high[0])
                    if prev != self.sl:
                        self.l.sl[0] = self.sl
                        self.l.e1[0] = self.sl - r * 0.0625
                        self.l.target[0] = self.sl - r
            if (close - p33) * (close - rlz) > 0:
                self.sl = 0

    def next(self):
        direction = self.Direction.l.direction[0]
        if math.isnan(direction) or direction == 0:
            return

        self.hh = self.Direction.l.hh[0]
        self.ll = self.Direction.l.ll[0]
        self.draw_range(direction, self.Direction.l.rlz[0])
