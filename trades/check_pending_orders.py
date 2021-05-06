def check_pending_orders(self):
    for t in self.pending_orders:
        if t['direction'] == 'Long':
            if t['entry'] > self.low[0] and t['entry'] < self.high[0]:
                self.new_trade = t
                self.active_trades.append(t)
                # self.log('Pending order filled')
                self.pending_orders.remove(t)
            elif t['sl'] > self.low[0]:
                self.pending_orders.remove(t)
                # self.log('Pending order discarded')
                # self.log(t)
        else:
            if t['entry'] < self.high[0] and t['entry'] > self.low[0]:
                self.new_trade = t
                self.active_trades.append(t)
                # self.log('Pending order filled')
                self.pending_orders.remove(t)
            elif t['sl'] < self.high[0]:
                self.pending_orders.remove(t)
                # self.log('Pending order discarded')
                # self.log(t)
