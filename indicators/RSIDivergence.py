import backtrader as bt

class RSIDivergence(bt.ind.PeriodN):
    lines = ('signal',)
    params = dict(
        rsi_period=30,
        hl_period=100,
        hl_min=25
    )

    def __init__(self):
        self.hfi = bt.ind.FindFirstIndexHighest(self.data.high, period=self.p.hl_period)
        self.lfi = bt.ind.FindFirstIndexLowest(self.data.low, period=self.p.hl_period)
        self.rsi = bt.ind.RSI_Safe(period=self.p.rsi_period)

    def signal_get(self):
        signal = 0
        if self.hfp >= self.hsp:
            if self.rsi[-int(self.hfi[0])] < self.rsi[-int(self.hsi)]:
                signal -= 1

        if self.lfp <= self.lsp:
            if self.rsi[-int(self.lfi[0])] > self.rsi[-int(self.lsi)]:
                signal += 1

        return signal

    def next(self):
        h_iterable = self.data.get(size=self.p.hl_period, ago=-int(self.hfi[0]) - self.p.hl_min)
        l_iterable = self.data.get(size=self.p.hl_period, ago=-int(self.lfi[0]) - self.p.hl_min)

        if len(h_iterable) > 0 and len(l_iterable) > 0:
            m = max(h_iterable)
            self.hsi = next(i for i, v in enumerate(reversed(h_iterable)) if v == m) + int(self.hfi[0]) + self.p.hl_min

            m = min(l_iterable)
            self.lsi = next(i for i, v in enumerate(reversed(l_iterable)) if v == m) + int(self.lfi[0]) + self.p.hl_min

            self.hfp = self.data.high[-int(self.hfi[0])]
            self.hsp = self.data.high[-int(self.hsi)]
            self.lfp = self.data.low[-int(self.lfi[0])]
            self.lsp = self.data.low[-int(self.lsi)]

            self.lines.signal[0] = self.signal_get()
        else:
            self.lines.signal[0] = 0
