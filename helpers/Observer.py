import backtrader as bt

class Observer(bt.observer.Observer):
    lines = ('cash', 'current',)

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(
        cash=dict(color='black', fillstyle='full'),
        current=dict(color='blue', fillstyle='full'),
    )

    def next(self):
        self.lines.cash[0] = self._owner.cash #pylint: disable-all

        amount = 0
        for t in self._owner.active_trades: #pylint: disable-all
            if t['direction'] == 'Long':
                amount -= (t['entry'] - self.data.close[0]) * t['size']
            else:
                amount += (t['entry'] - self.data.close[0]) * t['size']
        self.lines.current[0] = self._owner.cash + amount #pylint: disable-all
