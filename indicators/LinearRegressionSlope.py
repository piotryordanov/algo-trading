import backtrader as bt
from scipy import stats
from sklearn import linear_model


class LinearRegressionSlope(bt.Indicator):
    lines = ("slope", )

    plotinfo = dict(
        subplot=True,
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[10.0, 0]
    )
    plotlines = dict(
        slope=dict(color="black", _fill_lt=(10, "red")),
    )

    def __init__(self):
        self.l.slope = self.data.l.slope
