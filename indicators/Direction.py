import math

import backtrader as bt

from indicators.Fractal import Fractal
from Settings import Fractal_Left_Shift, Fractal_Right_Shift


class Direction(bt.Indicator):
    _mindatas = 3
    params = dict()
    lines = ("direction", "")
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[2.0, 0, -2.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[2.0, -2.0],
    )

    plotlines = dict(
        direction=dict(
            color="black", _fill_gt=(3, "red"), _fill_lt=(-3, "lime")
        )
    )

    def __init__(self):
        self.rsi = self.data1.l.signal_continuous
        self.william = self.data2

    def next(self):
        if math.isnan(self.l.direction[-1]):
            self.l.direction[0] = 0
        else:
            self.l.direction[0] = self.l.direction[-1]

        curr = self.l.direction[0]
        self.l.direction[0] = self.rsi[0] + self.william.l.price_location[0]
