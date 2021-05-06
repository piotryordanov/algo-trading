import backtrader as bt
from backtrader.utils.autodict import AutoOrderedDict

from indicators.Trail import Trail
from indicators.Fractal import Fractal
from indicators.Trail_Fractal import Trail_Fractal
from trades.update_trades import update_trades
from trades.close_trade import close_trade
from trades.check_pending_orders import check_pending_orders
from trades.create_trade import create_trade
from analyzers.MyAnalyzer import analysis
from analyzers.runAnalysis import printAnalysis
from Settings import AssetClass, Trades_Direction, Compound, Max_Loss, Initial_Cash, PlotTrail, Use_Trail_Stop
from Settings import Fractal_Right_Shift, Fractal_Left_Shift

class BaseStrategy(bt.Strategy):
    params = dict(
        assetClass=AssetClass,
        trades_direction=Trades_Direction,
        compound=Compound,
        max_loss=Max_Loss,
        initial_cash=Initial_Cash,
        left_shift=Fractal_Left_Shift,
        right_shift=Fractal_Right_Shift,
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        time = self.datas[0].datetime.time(0)
        print('%s, %s, %s' % (dt.isoformat(), time, txt))
        # print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.open = self.data.open
        self.close = self.data.close
        self.low = self.data.low
        self.high = self.data.high
        self.signals = 0

        self.init_trades()
        self.cash = self.p.initial_cash
        if Use_Trail_Stop:
            self.fractal = Fractal(left_shift=self.p.left_shift, right_shift=self.p.right_shift, plot=PlotTrail)
            self.Trail = Trail(self.data, self.fractal, LineColor='gray', plot=PlotTrail)

    def init_trades(self):
        self.pending_orders = list()
        self.active_trades = list()
        self.closed_trades = list()

        self.new_trade = list()
        self.closed_trade = list()

    def update_trades(self):
        check_pending_orders(self)
        update_trades(self)

    def close_trade(self, t, amount):
        close_trade(self, t, amount)

    def update_cash(self, amount):
        self.cash = self.cash + amount

    def create_trade(self, direction='Long', entry=0, Type='market', sl=0, target=0):
        if entry == sl:
            return

        if direction == 'Long':
            if sl >= entry:
                return
        else:
            if sl <= entry:
                return

        if direction == 'Long' and entry < self.data.close[0]:
            entry = self.data.close[0]
        elif direction == 'Short' and entry > self.data.close[0]:
            entry = self.data.close[0]

        create_trade(self, direction=direction, entry=entry, Type=Type, sl=sl, target=target)
        self.signals += 1

    def stop(self):
        s = self
        self.info = analysis(
            s.closed_trades,
            s.active_trades,
            s.cash,
            s.p.initial_cash,
            self.data,
            AutoOrderedDict(),
        )
        self.info.signals = self.signals
        printAnalysis(dict(self.info))
