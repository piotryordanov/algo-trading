def close_trade(self, t, amount):
    t["dateclose"] = self.data.datetime[0]
    self.closed_trade = t
    self.update_cash(amount)
    self.closed_trades.append(t)

    risk = t["entry"] - t["original_sl"]
    reward = t["exit"] - t["entry"]
    rr = reward / risk
    t["rr"] = rr
    if rr == 0:
        t["stop_trigger"] = "Stop to scratch"
    t["pips"] = abs((t["exit"] - t["entry"]) * 10000)

    self.log(
        "RR: %.2f | Max RR: %.2f | Lots: %.2f | Return: $%.2f | Pips: %.1f"
        % (rr, t["max_rr"], t["size"] / 100000, amount, t["pips"])
    )

    # self.log(t['size'] / 100000)
    # self.log('Stop Trigger:  %s' % (t['stop_trigger']))
    # print()
    # self.log(t)
    # self.log(amount)
