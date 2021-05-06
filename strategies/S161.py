import backtrader as bt
import backtrader.indicators as btind

from strategies.BaseStrategy import BaseStrategy
from indicators.Fractal_161 import Fractal_161
from indicators.ATR import ATR
from indicators.Lines_161 import Lines_161
from indicators.Trend import Trend
from indicators.SupportAndResistance import SNP
from indicators.Ranging import Ranging
from Settings import Fractal_Right_Shift


class S161(BaseStrategy):
    params = dict(period=500, MA=btind.EMA)

    def __init__(self):
        super(S161, self).__init__()
        self.Fractal = Fractal_161(plot=True)
        # self.Lines = Lines_161(self.data, self.Fractal, shift=10)
        # self.Trend = Trend(self.data, self.Lines)
        # SNP(self.Fractal)
        Ranging(self.data, self.Fractal, shift=Fractal_Right_Shift)

    def next(self):
        self.update_trades()
