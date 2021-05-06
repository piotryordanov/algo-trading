import math

import backtrader as bt

from indicators.Fractal import Fractal
from Settings import Fractal_Left_Shift, Fractal_Right_Shift


class Structure(bt.Indicator):
    _mindatas = 2
    params = dict(shift=3)
    lines = ("signal", "upstate", "downstate")
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[1.0, -1.0],
    )

    plotlines = dict(
        signal=dict(color="black"),
        upstate=dict(_plotskip=True),
        downstate=dict(_plotskip=True),
    )

    def __init__(self):
        self.Fractal = self.data1
        self.shift = self.p.shift * -1
        self.reset()

    def getdefault(self):
        return dict(ll=0, hh=0, state=0)

    def reset(self):
        self.downstate = self.getdefault()
        self.upstate = self.getdefault()

    def update_upstate(self, close, low, high, s, ll, lh, hl, hh):
        if s["state"] == 0:
            if ll > 0:
                s["state"] = 1
                s["ll"] = ll
        elif s["state"] == 1:
            if low < s["ll"]:
                self.upstate = self.getdefault()
            elif (hh > 0) or (lh > 0):
                s["state"] = 2
                if hh > 0:
                    s["hh"] = hh
                else:
                    s["hh"] = lh
        elif s["state"] == 2:
            if low < s["ll"]:
                self.upstate = self.getdefault()
            elif hl > 0:
                if close > s["hh"]:
                    s["state"] = 4
                else:
                    self.upstate["state"] = 3
            elif high > s["hh"]:
                s["hh"] = high
        elif s["state"] == 3:
            if low < s["ll"]:
                self.upstate = self.getdefault()
            elif high > s["hh"]:
                s["state"] = 4
            elif ll > 0:
                s["state"] = 1
                s["ll"] = ll
        elif s["state"] == 4:
            self.upstate = self.getdefault()

        # if s["state"] > 1 and ll > 0:
        #     self.upstate = self.getdefault()

        self.l.upstate[0] = self.upstate["state"]

    def update_downstate(self, close, low, high, s, ll, lh, hl, hh):
        if s["state"] == 0:
            if hh > 0:
                s["state"] = -1
                s["hh"] = hh
        elif s["state"] == -1:
            if close > s["hh"]:
                self.downstate = self.getdefault()
            elif (ll > 0) or (hl > 0):
                s["state"] = -2
                if ll > 0:
                    s["ll"] = ll
                else:
                    s["ll"] = hl
        elif s["state"] == -2:
            if high > s["hh"]:
                self.downstate = self.getdefault()
            elif lh > 0:
                if close < s["ll"]:
                    s["state"] = -4
                else:
                    s["state"] = -3
            elif close < s["ll"]:
                s["ll"] = low
        elif s["state"] == -3:
            if high > s["hh"]:
                self.downstate = self.getdefault()
            elif low < s["ll"]:
                s["state"] = -4
            elif hh > 0:
                s["state"] = -1
                s["hh"] = hh
        elif s["state"] == -4:
            self.downstate = self.getdefault()

        # if s["state"] < -1 and hh > 0:
        #     self.downstate = self.getdefault()

        self.l.downstate[0] = self.downstate["state"]

    def next(self):
        (hh, lh, ll, hl) = (
            self.Fractal.l.fractal_bearish_hh[self.shift],
            self.Fractal.l.fractal_bearish_lh[self.shift],
            self.Fractal.l.fractal_bullish_ll[self.shift],
            self.Fractal.l.fractal_bullish_hl[self.shift],
        )
        (close, low, high, ups, downs, reset) = (
            self.data.close[0],
            self.data.low[0],
            self.data.high[0],
            self.upstate,
            self.downstate,
            self.reset,
        )

        self.update_upstate(close, low, high, ups, ll, lh, hl, hh)
        self.update_downstate(close, low, high, downs, ll, lh, hl, hh)

        self.l.signal[0] = 0
        if self.upstate["state"] == 4:
            self.l.signal[0] = 1
        elif self.downstate["state"] == -4:
            self.l.signal[0] = -1
        else:
            self.l.signal[0] = self.l.signal[-1]
