import backtrader as bt
import backtrader.indicators as btind

from indicators.Divergence import Divergence
from indicators.Fractal import Fractal
from indicators.indicator_hhll import indicator_hhll
from indicators.indicator_llhh import indicator_llhh
from Settings import Fractal_Right_Shift
from strategies.BaseStrategy import BaseStrategy


class HHLL_Long_Strategy(BaseStrategy):
    params = dict(
        Fractal_Right_Shift=Fractal_Right_Shift, ShowReference=False, UseTrail=True
    )

    def __init__(self):
        super(HHLL_Long_Strategy, self).__init__()

        # self.shift = self.p.Fractal_Right_Shift
        self.Fractal = Fractal()
        self.ind = indicator_hhll(self.data, self.Fractal)
        self.ind = indicator_llhh(self.data, self.Fractal)
        # self.MA = btind.SMA(btind.HullMA(period=300), period=100)
        btind.HullMA(period=10)
        self.rsi = btind.RSI_Safe()
        # self.div = Divergence()

        # self.range = list()

    def next(self):
        # Simply log the closing price of the series from the reference
        entry = self.ind.lines.e1[0]
        sl = self.ind.lines.sl[0]
        print(self.rsi[0])
        if entry == entry:
            self.log("======")
            self.log(self.data.high[0])
            self.log(entry)
            self.log(sl)

    # def next(self):
    #     self.update_trades()
    #     entry_short = self.hhll.lines.e1[0]
    #     if entry_short > 0:
    #         self.create_trade(
    #             direction="Short", entry=entry_short, Type="Order", sl=self.data.high[0]
    #         )
    
    #     entry_long = self.llhh.lines.e1[0]
    #     if entry_long > 0:
    #         self.create_trade(
    #             direction="Long", entry=entry_long, Type="Order", sl=self.data.low[0]
    #         )
