import backtrader as bt
import backtrader.indicators as btind

from indicators.ADX import ADX
from indicators.Regression import Regression
from indicators.WilliamAlligator import WilliamAlligator
from signals.MA_Cross_Signal import MA_Cross_Signal
from signals.WilliamSignal import WilliamSignal
from strategies.BaseStrategy import BaseStrategy


class MACross(BaseStrategy):
    params = dict(period=500, MA=btind.EMA)

    def __init__(self):
        super(MACross, self).__init__()
        self.Location = WilliamSignal(self.data, WilliamAlligator(), ADX(), plot=True)
        self.Signal = self.Location.l.signal
        self.Cross = self.Location.l.ma_cross
        # MA = self.p.MA(period=self.p.period)
        # btind.CCI()
        # btind.ATR()
        # MA2 = self.p.MA(period=100)
        # self.Signal = MA_Cross_Signal(self.data, MA)
        # Regression(MA, period=14)
        # Regression(MA2, period=14)

    def next(self):
        if len(self.data.close) < 30:
            return

        signal = self.Signal[0]
        cross = self.Cross[0]
        if cross != 0:
            t = self.active_trades
            if cross == 1:
                if len(t) > 0:
                    if t[0]["direction"] == "Short":
                        t[0]["sl"] = self.data.close[0]
            else:
                if len(t) > 0:
                    if t[0]["direction"] == "Long":
                        t[0]["sl"] = self.data.close[0]

        if signal != 0:
            entry = self.data.close[0]
            if signal == 1:
                sl = min(self.data.low.get(size=3))
                self.create_trade(
                    direction="Long", entry=entry, Type="market", sl=sl, target=10000000
                )
            else:
                sl = max(self.data.high.get(size=3))
                self.create_trade(
                    direction="Short", entry=entry, Type="market", sl=sl, target=0
                )
        self.update_trades()

    #     signal = self.Signal[0]
    #     if signal != 0:
    #         entry = self.data.close[0]
    #         if signal == 1:
    #             sl = self.Trail.lowest[0]
    #             sl = self.Trail.lowest[0] + (self.data.close[0] - self.Trail.lowest[0]) / 2
    #             sl = self.data.low[0]
    #             self.create_trade(
    #                 direction="Long", entry=entry, Type="market", sl=sl, target=10000000
    #             )
    #         else:
    #             sl = self.Trail.highest[0]
    #             sl = self.Trail.highest[0] - (self.Trail.highest[0] - self.data.close[0]) / 2
    #             sl = self.data.high[0]
    #             self.create_trade(
    #                 direction="Short", entry=entry, Type="market", sl=sl, target=0
    #             )
    #
    # # #     print("========")
    # # #     print(("Period: %d") %(self.p.period))
