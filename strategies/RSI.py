import backtrader.indicators as btind

from strategies.BaseStrategy import BaseStrategy

from indicators.RSI import RSI


class RSI_Strategy(BaseStrategy):
    params = dict(right_shift=1, left_shift=20)

    def __init__(self):
        super(RSI_Strategy, self).__init__()
        self.rsi = btind.RSI(period=2, upperband=95, lowerband=5)
        self.sma = btind.SMA(period=200)
        self.smaa = btind.SMA(period=21)

    def next(self):
        if len(self.data.close) < 30:
            return
        isRSIOverSold =  (self.rsi[0] <= 5 and self.rsi[-1] > 5 and self.rsi[-2] > 5)
        isRSIOverBought =  (self.rsi[0] >= 95 and self.rsi[-1] < 95 and self.rsi[-2] < 95)
        if isRSIOverSold and self.data.close > self.sma:
            self.create_trade(direction="Long", entry=self.data[0], Type="market", sl=0, target=0)
        if isRSIOverBought and self.data.close < self.sma:
            self.create_trade(direction="Short", entry=self.data[0], Type="market", sl=999999999999999, target=0)

        # self.update_trades()
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
