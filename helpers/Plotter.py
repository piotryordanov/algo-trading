import backtrader.plot as plt

class Plotter(plt.Plot):
    def __init__(self):
        #super().__init__(volup='#60cc73',  plotdist= 0.3, style='bar')  # custom color for volume up bars 
        super().__init__(fmt_x_data = ('%Y-%m-%d %H:%M:%S'), volume=False, style='bar',  bardown='0.4', width=0.2)  # custom color for volume up bars 

    def show(self):
        mng = self.mpyplot.get_current_fig_manager()
        mng.full_screen_toggle()
        self.mpyplot.show()
