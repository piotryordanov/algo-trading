import backtrader as bt
import backtrader.indicators as btind

from strategies.BaseStrategy import BaseStrategy
from indicators.Trend import Trend
from indicators.Edges import Edges
from indicators.Fractal import Fractal
from indicators.EdgeFractal import EdgeFractal


class Bold(BaseStrategy):
    params = dict()

    def __init__(self):
        super(Bold, self).__init__()
        # Edges()
        # Fractal(left_shift=5, right_shift=3, marker="$-$")
        EdgeFractal()

    def next(self):
        self.update_trades()
