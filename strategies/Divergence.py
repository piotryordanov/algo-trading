import backtrader as bt
import backtrader.indicators as btind

from indicators.WilliamAlligator import WilliamAlligator
from indicators.Direction import Direction
from indicators.Fractal import Fractal
from indicators.FillFractal import FillFractal
from indicators.RSI_divergence import RSI_divergence
from indicators.Ranging import Ranging
from indicators.Trend import Trend
from Settings import Fractal_Right_Shift
from strategies.BaseStrategy import BaseStrategy


class Divergence(BaseStrategy):
    params = dict(right_shift=1, left_shift=20)

    def __init__(self):
        super(Divergence, self).__init__()
        # direction = Direction(self.data, self.fractal)
        FillFractal(left_shift=2, right_shift=2)
        # self.trend = trend(self.data, self.fractal, direction)

        # self.ranging = Ranging(self.data, btind.SMA(period=5), btind.SMA(period=8), btind.SMA(period=13))
        # mafunc = btind.EMA
        # self.ranging = Ranging(self.data, mafunc(period=5), mafunc(period=8), mafunc(period=13))
        # mafunc = btind.WMA
        # self.ranging = Ranging(self.data, mafunc(period=5), mafunc(period=8), mafunc(period=13))
        # mafunc = btind.HullMA
        # self.ranging = Ranging(self.data, WilliamAlligator())

        self.rsi = btind.RSI_Safe(period=5)
        self.div = RSI_divergence(self.data, self.rsi, self.fractal, fractal_shift=1)
        self.rsi = btind.RSI_Safe(period=8)
        self.div = RSI_divergence(self.data, self.rsi, self.fractal, fractal_shift=1)
        self.rsi = btind.RSI_Safe(period=13)
        self.div = RSI_divergence(self.data, self.rsi, self.fractal, fractal_shift=1)

    def next(self):
        if len(self.data.close) < 30:
            return

        self.update_trades()
        # entry = self.trend.lines.e1[0]
        # sl = self.trend.lines.sl[0]
        # target = self.trend.lines.target[0]
        # if entry > 0:
        #     if entry > sl:
        #         self.create_trade(
        #             direction="Long", entry=entry, Type="order", sl=sl, target=target
        #         )
        #     else:
        #         self.create_trade(
        #             direction="Short", entry=entry, Type="order", sl=sl, target=target
        #         )
