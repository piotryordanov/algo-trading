from datetime import datetime, timedelta

from backtrader import Analyzer
from backtrader.utils import AutoOrderedDict


def analysis(closed_trades, active_trades, cash, initial_cash, data, info):
    pnllong = 0
    pnlshort = 0
    active_pnllong = 0
    active_pnlshort = 0
    long_won = 0
    short_won = 0
    long_lost = 0
    short_lost = 0

    lowest_rr = 0
    highest_rr = 0
    average_rr = 0
    stopped_at_scratch = 0
    pips = 0

    for t in closed_trades:
        entry = t["entry"]
        sl = t["exit"]
        size = t["size"]
        pips = pips + t["pips"]

        if t["rr"] == 0:
            stopped_at_scratch = stopped_at_scratch + 1
        else:
            average_rr = round((average_rr + t["rr"]) / 2, 2)
            lowest_rr = min(lowest_rr, t["rr"])
            highest_rr = round(max(highest_rr, t["max_rr"]), 2)

        if t["direction"] == "Long":
            rr = sl - entry
            pnllong = pnllong + rr * size
            if rr > 0:
                long_won = long_won + 1
            else:
                long_lost = long_lost + 1
        else:
            rr = entry - sl
            pnlshort = pnlshort + rr * size
            if rr > 0:
                short_won = short_won + 1
            else:
                short_lost = short_lost + 1

    for t in active_trades:
        entry = t["entry"]
        sl = t["sl"]
        size = t["size"]
        if t["direction"] == "Long":
            rr = sl - entry
            active_pnllong = active_pnllong + rr * size
        else:
            rr = entry - sl
            active_pnlshort = active_pnlshort + rr * size
    total_positions = len(active_trades) + len(closed_trades)
    closed_positions = len(closed_trades)
    open_positions = total_positions - closed_positions

    total_won = long_won + short_won
    total_lost = long_lost + short_lost

    win_rate = 0
    if total_positions > 0:
        win_rate = (long_won + short_won) / total_positions
    info.pnlshort = round(pnlshort, 2)
    info.pnllong = round(pnllong, 2)
    info.pnl = round(pnllong + pnlshort, 2)
    info.active_pnlshort = round(active_pnlshort, 2)
    info.active_pnllong = round(active_pnllong, 2)
    info.active_pnl = round(active_pnllong + active_pnlshort, 2)
    info.net_pnl = round(info.active_pnl + info.pnl, 2)
    info.wins = total_won
    info.losses = total_lost
    info.winrate = round(win_rate * 100, 2)
    info.preturn = round((cash / initial_cash - 1) * 100, 2)
    info.net_preturn = round(((cash + info.active_pnl) / initial_cash - 1) * 100, 2)
    info.initial_cash = initial_cash

    info.lowest_rr = lowest_rr
    info.highest_rr = highest_rr
    info.average_rr = average_rr
    info.pips = int(pips)

    t1 = data.num2date(data.datetime[(len(data) - 1) * -1])
    t2 = data.num2date()
    info.duration = str(t2 - t1)
    return info


class MyAnalyzer(Analyzer):
    def __init__(self):
        self.rets = AutoOrderedDict()
        self.info = AutoOrderedDict()
        self.info.signals = 0

    def get_analysis(self):
        return dict(self.info)

    def stop(self):
        s = self.strategy
        self.info = analysis(
            s.closed_trades,
            s.active_trades,
            s.cash,
            s.p.initial_cash,
            self.data,
            self.info,
        )
        self.rets._close()

    def next(self):
        if self.strategy.new_trade:
            self.info.signals += 1
