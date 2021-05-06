import math

import backtrader as bt
import backtrader.indicators as btind

lines = tuple()
plotlines = dict()
for i in range(0, 100):
    name = "support_line%d" % (i)
    lines = lines + tuple([name])
    plotlines[name] = dict(color="lime", ls="-")
    name = "resistance_line%d" % (i)
    lines = lines + tuple([name])
    plotlines[name] = dict(color="red", ls="-")


class SNP(bt.Indicator):
    _mindatas = 3
    lines = lines
    params = dict()

    plotinfo = dict(subplot=False)

    plotlines = plotlines

    def __init__(self):
        self.ups = self.data.l.intermediates_up
        self.downs = self.data.l.intermediates_down
        self.idx_dwn = 0
        self.idx_up = 0

    def extend_lines(self):
        for line in self.l.lines:
            if line[-1] > 0:
                line[0] = line[-1]
                pass

    def next(self):
        self.extend_lines()
        if self.ups[0] > 0:
            name = "resistance_line%d" % (self.idx_up)
            getattr(self.lines, name)[0] = self.ups[0]
            self.idx_up += 1
        elif self.downs[0] > 0:
            name = "support_line%d" % (self.idx_dwn)
            getattr(self.lines, name)[0] = self.downs[0]
            self.idx_dwn += 1
