import backtrader as bt

from indicators.Trail_ATR import Trail_ATR
from indicators.Trail_Fractal import Trail_Fractal
from Settings import ATRMultiplier, TrailType


class Trail(bt.ind.PeriodN):
    _mindatas = 1
    lines = ("lowest", "highest")

    plotinfo = dict(subplot=False, plotlinelabels=False, plot=True)

    plotlines = dict(
        lowest=dict(color="gray", fillstyle="full", ls="--"),
        highest=dict(color="blue", fillstyle="full", ls="--"),
    )

    params = dict(LineColor="gray")

    def _plotinit(self):
        self.plotlines.lowest.color = self.p.LineColor
        self.plotlines.highest.color = self.p.LineColor

    def __init__(self):
        self.ATR = Trail_ATR(self.data, multiplier=ATRMultiplier)
        self.fractal = self.data1
        self.fractal_trail = Trail_Fractal(self.data, self.fractal)

    def next(self):
        if TrailType == "ATR":
            self.highest[0] = self.ATR.highest[0]
            self.lowest[0] = self.ATR.lowest[0]
        elif TrailType == "Fractal":
            self.highest[0] = self.fractal_trail.highest[0]
            self.lowest[0] = self.fractal_trail.lowest[0]
        elif TrailType == "Combined":
            self.highest[0] = min(self.ATR.highest[0], self.fractal_trail.highest[0])
            self.lowest[0] = max(self.ATR.lowest[0], self.fractal_trail.lowest[0])
