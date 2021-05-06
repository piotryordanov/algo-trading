from Settings import TakeOnTarget, RR_Trail_Amount, RR_Trail_Post_Target, Use_Trail_Stop, Use_RR_Stop, RR_StopToScratch
from trades.close_trade import close_trade


def get_rr(self, t):
    (high, low, entry) = (self.high[0], self.low[0], t['entry'])
    risk = abs(entry - t['original_sl'])

    if t['direction'] == 'Long':
        reward = abs(self.high[0] - entry)
    else:
        reward = abs(self.low[0] - entry)

    rr = reward / risk

    if t['direction'] == 'Long':
        if t['sl'] < t['entry'] and rr > RR_StopToScratch:
            newsl = t['entry']
        else:
            multiplier = RR_Trail_Amount
            if high > t['target']:
                multiplier = RR_Trail_Post_Target
            newsl = max(self.high[0] - risk * multiplier, t['sl'])
    else:
        if t['sl'] > t['entry'] and rr > RR_StopToScratch:
            newsl = t['entry']
        else:
            multiplier = RR_Trail_Amount
            if low < t['target']:
                multiplier = RR_Trail_Post_Target
            newsl = min(self.low[0] + risk * RR_Trail_Amount, t['sl'])
    return (rr, newsl)

def update_trades(self):
    to_keep = list()
    for t in self.active_trades:
        sl = t['sl']
        (rr, newsl) = get_rr(self, t)
        t['max_rr'] = max(t['max_rr'], rr)
        if t['direction'] == 'Long':
            # trail = max(self.Trail.lowest[0], newsl)
            if self.low[0] < sl:
                t['exit'] = t['sl']
                if t['stop_trigger'] == "":
                    t['stop_trigger'] = 'sl'
                close_trade(self, t, (t['sl'] - t['entry']) * t['size'])
            elif TakeOnTarget and self.high[0] >= t['target']:
                t['exit'] = t['target']
                t['stop_trigger'] = 'target'
                close_trade(self, t, (t['target'] - t['entry']) * t['size'])
            elif Use_RR_Stop:
                t['sl'] = newsl
                t['stop_trigger'] = 'rr'
                to_keep.append(t)
            elif Use_Trail_Stop:
                trail = self.Trail.lowest[0]
                if trail > sl:
                    t['sl'] = trail
                    t['stop_trigger'] = 'trail'
                to_keep.append(t)
            else:
                to_keep.append(t)
        if t['direction'] == 'Short':
            if self.high[0] > sl:
                t['exit'] = t['sl']
                if t['stop_trigger'] == "":
                    t['stop_trigger'] = 'sl'
                close_trade(self, t, (t['entry'] - t['sl']) * t['size'])
            elif TakeOnTarget and self.low[0] <= t['target']:
                t['exit'] = t['target']
                t['stop_trigger'] = 'target'
                close_trade(self, t, (t['entry'] - t['target']) * t['size'])
            elif Use_RR_Stop:
                t['sl'] = newsl
                t['stop_trigger'] = 'rr'
                to_keep.append(t)
            elif Use_Trail_Stop:
                trail = self.Trail.highest[0]
                if trail < sl:
                    t['sl'] = trail
                    t['stop_trigger'] = 'trail'
                to_keep.append(t)
            else:
                to_keep.append(t)
    self.active_trades = to_keep
