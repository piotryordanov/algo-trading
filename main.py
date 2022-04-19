"""
Main Module
"""
import backtrader as bt
import backtrader.indicators as btind

from analyzers.runAnalysis import runAnalysis
from helpers.get_data import get_data
from helpers.MyBuySell import MyBuySell
from helpers.Observer import Observer
from helpers.Plotter import Plotter

from strategies.HHLL_Long_Strategy import HHLL_Long_Strategy
from strategies.EducatedGambler import EducatedGambler
from strategies.SAR_Strategy import SARStrategy
from strategies.MACross import MACross
from strategies.RSI import RSI_Strategy

### ==================================
### Init
### ==================================
cerebro = bt.Cerebro(stdstats=False, optreturn=False)


### ==================================
### Get the Data
### ==================================
# data0 = get_data("FX/4h/EURUSD.csv", "standard")
data0 = get_data("crypto/Chart.csv", "crypto")
cerebro.adddata(data0)


### ==================================
#### Add the strategies
### ==================================
# cerebro.addstrategy(HHLL_Long_Strategy)
cerebro.addstrategy(RSI_Strategy)
# cerebro.addstrategy(EducatedGambler)
# cerebro.addstrategy(SARStrategy)
# cerebro.addstrategy(MACross, period=50)

### ==================================
### Use this for optimization
### ==================================
# Range = range(50, 60)
# MA=[btind.SMA, btind.EMA, btind.WMA, btind.HullMA, btind.SMMA],
# cerebro.optstrategy(MACross, period=Range, MA=MA)
# cerebro.addstrategy(S161)

### ==================================
### Add observers like PnL and entries
### ==================================
cerebro.addobserver(Observer)
cerebro.addobserver(MyBuySell)

### ==================================
### Run the backtest. Smile. Etc..
### ==================================
opt_runs = cerebro.run()

pnl = runAnalysis(cerebro)
cerebro.plot(start=0, plotter=Plotter(), iplot=False, style='bar')
