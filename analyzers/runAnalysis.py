import backtrader as bt
# import texttable as Texttable
from texttable import Texttable

from analyzers.MyAnalyzer import MyAnalyzer


# def printTradeAnalysis(analyzer):
#     #Get the results we are interested in
#     total_open = analyzer.total.get('open', 0)
#     total_closed = analyzer.total.get('closed', 0)
#     if analyzer.get('won'):
#         total_won = analyzer.won.total
#     else:
#         total_won = 0
#
#     if analyzer.get('lost'):
#         total_lost = analyzer.lost.total
#     else:
#         total_lost = 0
#
#     if analyzer.get('streak'):
#         win_streak = analyzer.streak.won.longest
#         lose_streak = analyzer.streak.lost.longest
#     else:
#         win_streak = 0
#         lose_streak = 0
#
#     if analyzer.get('pnl'):
#         pnl_net = round(analyzer.pnl.net.total,2)
#     else:
#         pnl_net = 0
#
#     if total_closed == 0:
#         win_rate = 0
#     else:
#         win_rate = (total_won / total_closed) * 100
#
#     #Designate the rows
#     h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
#     h2 = ['PnL Net','Win Streak', 'Losing Streak', 'Win Rate']
#     r1 = [total_open, total_closed,total_won,total_lost]
#     r2 = [pnl_net, win_streak, lose_streak, win_rate]
#
#     #Check which set of headers is the longest.
#     if len(h1) > len(h2):
#         header_length = len(h1)
#     else:
#         header_length = len(h2)
#     #Print the rows
#     print_list = [h1,r1,h2,r2]
#     row_format ="{:<15}" * (header_length + 1)
#     print("Trade Analysis Results:")
#     for row in print_list:
#         print(row_format.format('',*row))
#
# def printSQN(analyzer):
#     sqn = round(analyzer.sqn,2)
#     print('SQN: {}'.format(sqn))
#
def printAnalysis(analyzer):
    signals = analyzer.get("signals")
    pnlshort = analyzer.get("pnlshort")
    pnllong = analyzer.get("pnllong")
    pnl = analyzer.get("pnl")
    active_pnlshort = analyzer.get("active_pnlshort")
    active_pnllong = analyzer.get("active_pnllong")
    active_pnl = analyzer.get("active_pnl")
    net_pnl = analyzer.get("net_pnl")
    wins = analyzer.get("wins")
    losses = analyzer.get("losses")
    winrate = str(round(analyzer.get("winrate"), 2)) + "%"
    preturn = analyzer.get("preturn")
    net_preturn = analyzer.get("net_preturn")
    duration = analyzer.get("duration")
    initial_cash = analyzer.get("initial_cash")
    lowest_rr = analyzer.get("lowest_rr")
    highest_rr = analyzer.get("highest_rr")
    average_rr = analyzer.get("average_rr")
    pips = analyzer.get("pips")
    # print(preturn)
    # print(net_preturn)

    rows = [
        [
            "Signals",
            "Closed Short",
            "Closed Long",
            "Closed PNL",
            "Active Short",
            "Active Long",
            "Active PNL",
            "Net PNL",
            "Net Return (%)",
        ],
        [
            signals,
            pnlshort,
            pnllong,
            pnl,
            active_pnlshort,
            active_pnllong,
            active_pnl,
            net_pnl,
            net_preturn,
        ],
        [
            "Wins",
            "Loss",
            "Win Rate",
            "Duration",
            "Pips",
            "Initial Cash",
            "Lowest RR",
            "Highest RR",
            "Average RR",
        ],
        [
            wins,
            losses,
            winrate,
            duration,
            pips,
            initial_cash,
            lowest_rr,
            highest_rr,
            average_rr,
        ],
    ]

    table = Texttable(max_width=200)
    table.set_chars(["-", "|", "+", "-"])
    # for i in range(0, len(headers)):
    # table.set_deco(Texttable.HEADER)
    # table.add_rows([headers[i], rows[i]])
    table.add_rows(rows)
    print(table.draw() + "\n")

    return net_pnl


def runAnalysis(cerebro):
    # # Add the analyzers we are interested in
    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    # cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    cerebro.addanalyzer(MyAnalyzer, _name="mine")

    strategies = cerebro.run()
    # # firstStrat = strategies[0]
    # # printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
    # # printSQN(firstStrat.analyzers.sqn.get_analysis())
    # # printAnalysis(firstStrat.analyzers.mine.get_analysis())
    # for strat in strategies:
    #     # printTradeAnalysis(strat.analyzers.ta.get_analysis())
    #     # printSQN(strat.analyzers.sqn.get_analysis())
    #     return printAnalysis(strat.analyzers.mine.get_analysis())
    #
    #
    # # Get final portfolio Value
    # portvalue = cerebro.broker.getvalue()
    #
    # #Print out the final result
    # print('Final Portfolio Value: ${}'.format(portvalue))
