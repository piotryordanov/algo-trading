import backtrader as bt
import backtrader.indicators as btind

from indicators.Fractal import Fractal
from indicators.MACD import MACD
from indicators.Regression import Regression
from indicators.RSI import RSI
from indicators.Trend import Trend
from indicators.WilliamAlligator import WilliamAlligator
from indicators.Willy import Willy
from signals.Direction import Direction
from signals.Internals import Internals
from signals.InternalsSum import InternalsSum
from signals.Structure import Structure
from signals.WilliamSignal import WilliamSignal
from strategies.BaseStrategy import BaseStrategy

from Settings import Use_Bounce

threshold = 3

long_fractal_shift = 5
short_fractal_shift = 2


class EducatedGambler(BaseStrategy):
    params = dict(left_shift=7, right_shift=5)

    def __init__(self):
        # Regression()

        ## Fractals
        self.long_fractal = Fractal(
            left_shift=10, right_shift=long_fractal_shift, plot=True
        )
        self.short_fractal = Fractal(
            marker="$-$",
            marker_color="black",
            left_shift=2,
            right_shift=short_fractal_shift,
            plot=True,
        )
        # ## Signals
        l = Internals(
            self.data, self.long_fractal, shift=long_fractal_shift, threshold=threshold
        )
        s = Internals(
            self.data,
            self.short_fractal,
            shift=short_fractal_shift,
            threshold=threshold,
        )
        self.Internals = InternalsSum(s, l, threshold=threshold)
        #
        self.rsi = RSI(self.data, self.short_fractal)
        self.macd = MACD(self.data, self.short_fractal)
        self.willy = Willy(self.data, self.short_fractal)
        #
        self.Location = WilliamSignal(self.data, WilliamAlligator(), plot=True)
        #
        self.structure_fractal = Fractal(
            marker="$-$", marker_color="orange", left_shift=30, right_shift=4, plot=True
        )
        self.Structure = Structure(
            self.data, self.structure_fractal, shift=2, plot=True
        )
        #
        ## Direction
        self.Direction = Direction(
            self.data, self.Structure, self.Internals, self.Location
        )
        
        self.Trend = Trend(self.data, self.Direction)
        #
        super(EducatedGambler, self).__init__()

    def next(self):
        if len(self.data.close) < 30:
            return

        self.update_trades()
        entry = self.Trend.lines.e1[0]
        sl = self.Trend.lines.sl[0]
        target = self.Trend.lines.target[0]
        if entry > 0:
            if entry > sl:
                self.create_trade(
                    direction="Long", entry=entry, Type="order", sl=sl, target=target
                )
            else:
                self.create_trade(
                    direction="Short", entry=entry, Type="order", sl=sl, target=target
                )

        if self.rsi[0] > 0:
            if len(self.active_trades) > 0 and Use_Bounce:
                t = self.active_trades[0]
                t["sl"] = self.close[0]
            sl_index = 0
            sl = self.close[0] - (self.close[0] - self.low[sl_index]) / 2
            sl = self.low[sl_index]
            self.create_trade(
                direction="Long",
                entry=self.close[0],
                Type="market",
                sl=sl,
                target=10000000,
            )
        
        elif self.rsi[0] < 0:
            if len(self.active_trades) > 0 and Use_Bounce:
                t = self.active_trades[0]
                t["sl"] = self.close[0]
            sl_index = 0
            sl = self.close[0] + abs(self.close[0] - self.high[sl_index]) / 2
            sl = self.high[sl_index]
            self.create_trade(
                direction="Short", entry=self.close[0], Type="market", sl=sl
            )
