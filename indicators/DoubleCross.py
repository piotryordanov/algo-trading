import backtrader as bt
import backtrader.indicators as btind


class DoubleCross(bt.Indicator):
    _mindatas = 4
    lines = ("overunder", "MA", "sar")
    params = dict(use_bb=True)

    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        plotymargin=0.15,
        # Plot a reference horizontal line at 1.0 and -1.0
        plothlines=[2.0, 0, -2.0],
        # Simplify the y scale to 1.0 and -1.0
        plotyticks=[2.0, -2.0],
    )

    # Plot the line "overunder" (the only one) with dash style
    # ls stands for linestyle and is directly passed to matplotlib
    plotlines = dict(
        overunder=dict(color="black", ls="--"), MA=dict(color="blue", ls="-")
    )

    # def _plotlabel(self):
    #     # This method returns a list of labels that will be displayed
    #     # behind the name of the indicator on the plot
    #
    #     # The period must always be there
    #     plabels = [self.p.period]
    #
    #     # Put only the moving average if it's not the default one
    #     plabels += [self.p.movav] * self.p.notdefault('movav')
    #
    #     return plabels

    def __init__(self):
        self.ma_signal = 0
        self.sar_signal = 0

        self.MA = self.data1
        self.sar = self.data2
        self.bb = self.data3

        self.ma_cross = btind.CrossOver(self.data, self.MA)
        self.sar_cross = btind.CrossOver(self.data, self.sar)
        self.bb_status = self.bb > self.data

    def next(self):
        if self.ma_cross[0] == 1:
            self.ma_signal = 1
        elif self.ma_cross[0] == -1:
            self.ma_signal = -1

        if self.sar_cross[0] == 1:
            self.sar_signal = 1
        elif self.sar_cross[0] == -1:
            self.sar_signal = -1

        combo = self.ma_signal + self.sar_signal

        if self.p.use_bb:
            if combo == 2 and self.bb_status[0] == 0:
                self.l.overunder[0] = 2
            elif combo == -2 and self.bb_status[0] == 1:
                self.l.overunder[0] = -2
            else:
                self.l.overunder[0] = 0
        else:
            if combo == 2:
                self.l.overunder[0] = 2
            elif combo == -2:
                self.l.overunder[0] = -2
            else:
                self.l.overunder[0] = 0

        # self.l.MA[0] = self.ma_signal
        # self.l.sar[0] = self.sar_signal
        # if combo == 2 or combo == -2:
        #     self.sar_signal = 0
        #     self.ma_signal = 0
        # if combo == 2:
        #     if self.sar[0] > self.data.close[0]:
        #         self.sar_signal = 0
        #     if self.MA[0] < self.data.close[0]:
        #         self.ma_signal = 0
        # elif combo == -2:
        #     if self.sar[0] < self.data.close[0]:
        #         self.sar_signal = 0
        #     if self.MA[0] > self.data.close[0]:
        #         self.ma_signal = 0
