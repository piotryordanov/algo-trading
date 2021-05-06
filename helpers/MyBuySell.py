import backtrader as bt

'''
Custom Buy Sell Arrows
'''
class MyBuySell(bt.observer.Observer): #pylint: disable=too-many-ancestors
    lines = ('long_buy', 'long_sl', 'short_sl', 'short_sell', 'rr', 'sl')

    plotinfo = dict(plot=True, subplot=False, plotlinelabels=True)
    plotlines = dict(
        long_buy=dict(marker='^', markersize=14.0, color='lime', fillstyle='full', ls=''),
        long_sl=dict(marker='v', markersize=14.0, color='red', fillstyle='full', ls=''),
        sl=dict(marker='$-$', markersize=14.0, color='red', fillstyle='full', ls=''),

        short_sell=dict(marker='v', markersize=14.0, color='blue', fillstyle='full', ls=''),
        short_sl=dict(marker='^', markersize=14.0, color='orange', fillstyle='full', ls=''),
        # rr=dict(color="black", fillstyle="full", ls="-"),
    )

    params = (
        ('barplot', False),  # plot above/below max/min for clarity in bar plot
        ('bardist', 0.003),  # distance to max/min in absolute perc
    )

    def next(self):
        t = self._owner.new_trade
        if t:
            if t['direction'] == 'Long':
                # self.lines.long_buy[1] = self.data.low[1] * (1 - self.p.bardist) #pylint: disable=no-member
                self.lines.long_buy[0] = t['entry']
            else:
                # self.lines.short_sell[1] = self.data.high[1] * (1 + self.p.bardist) #pylint: disable=no-member
                self.lines.short_sell[0] = t['entry']
            self.l.sl[0] = t['original_sl']
            self._owner.new_trade = 0

        t = self._owner.closed_trade
        if t:
            if t['direction'] == 'Long':
                self.lines.long_sl[0] = t['exit']
            else:
                self.lines.short_sl[0] = t['exit']
            self._owner.closed_trade = 0

        # t = self._owner.active_trades
        # if len(t) > 0:
        #     self.l.rr[0] = t[0]['sl']
