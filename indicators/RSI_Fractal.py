import math
import backtrader as bt

from indicators.RSI_divergence import RSI_divergence


class RSI_Fractal(bt.Indicator):
    _mindatas = 1
    params = dict(cutoff=3, fractal_shift=7)
    lines = ("signal", "signal_continuous")
    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[3.0, 0, -3.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[6.0, -6.0],
    )

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(signal=dict(color="black", ls="--"))

    def __init__(self):
        self.fractal = self.data1
        self.rsi1 = RSI_divergence(
            self.data, self.fractal, rsi_period=5, fractal_shift=self.p.fractal_shift
        ).l.signal
        self.rsi2 = RSI_divergence(
            self.data, self.fractal, rsi_period=8, fractal_shift=self.p.fractal_shift
        ).l.signal
        self.rsi3 = RSI_divergence(
            self.data, self.fractal, rsi_period=13, fractal_shift=self.p.fractal_shift
        ).l.signal

    def next(self):
        curr = self.rsi1[0] + self.rsi2[0] + self.rsi3[0]
        # self.l.signal[0] = curr
        self.l.signal[0] = 0
        if curr >= self.p.cutoff:
            self.l.signal[0] = curr
        elif curr <= -self.p.cutoff:
            self.l.signal[0] = curr

        if math.isnan(self.l.signal_continuous[-1]):
            self.l.signal_continuous[0] = 0
        else:
            self.l.signal_continuous[0] = self.l.signal_continuous[-1]
            if self.l.signal[0] < 0:
                self.l.signal_continuous[0] = -1
            elif self.l.signal[0] > 0:
                self.l.signal_continuous[0] = 1
