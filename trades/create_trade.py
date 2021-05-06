import math

from Settings import One_Position_Per_Time
from trades.get_size import get_size


"""
Decides if we are allowed to go long, short, or both
"""


def allowed_to_create_position(self, direction):
    if not One_Position_Per_Time:
        return True
    elif len(self.active_trades) == 0:
        if len(self.pending_orders) == 0:
            return True
    elif len(self.active_trades) == 1:
        if self.active_trades[0]["direction"] != direction:
            return True
    return False


def parse_trade_direction(self, direction):
    if self.p.trades_direction == 2:
        if direction == "Short":
            return True
    elif self.p.trades_direction == 3:
        if direction == "Long":
            return True
    return False


def create_trade(self, direction="Long", entry=0, Type="market", sl=0, target=0):
    if parse_trade_direction(self, direction):
        return
    if not allowed_to_create_position(self, direction):
        return

    size = get_size(self, math.fabs(sl - entry))

    cash_amount = abs((sl - entry) * size) * -1
    t = dict(
        dateopen=self.data.datetime[0],
        direction=direction,
        entry=entry,
        original_sl=sl,
        sl=sl,
        target=target,
        stop_trigger="",
        max_rr=0,
        size=size,
    )
    if Type == "market":
        self.new_trade = t
        self.active_trades.append(t)
    else:
        self.pending_orders.append(t)
