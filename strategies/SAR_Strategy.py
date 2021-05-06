import backtrader as bt
import backtrader.indicators as btind

from strategies.BaseStrategy import BaseStrategy
from indicators.DoubleCross import DoubleCross


class SARStrategy(BaseStrategy):
    params = dict(
        use_bb=False,
        MA=23,
        period=2,
        af=0.02,
        afmax=0.2)

    def __init__(self):
        super(SARStrategy, self).__init__()

        self.MA = btind.HullMA(period=self.p.MA) #pylint: disable-all
        self.sar = btind.PSAR(period=self.p.period, af=self.p.af, afmax=self.p.afmax) #pylint: disable-all    
        self.bb = btind.BollingerBands(plot=True) #pylint: disable-all
        self.DoubleCross = DoubleCross(self.data, self.MA, self.sar, self.bb, use_bb=self.p.use_bb)

    def next(self):
        self.update_trades()
        if self.DoubleCross[0] == 2:
            self.create_trade(
                direction='Long',
                entry=self.close[0],
                Type='market',
                sl=self.Trail.lowest[0]
            )
        if self.DoubleCross[0] == -2:
            self.create_trade(
                direction='Short',
                entry=self.close[0],
                Type='market',
                sl=self.Trail.highest[0]
            )
