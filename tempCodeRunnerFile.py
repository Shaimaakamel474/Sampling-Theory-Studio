self.Current_Signal.sampling_rate=2*self.Current_Signal.maxfrequancy
            # sampled_time = np.arange(
            # self.Current_Signal.time[0], self.Current_Signal.time[-1]+ 2*self.Current_Signal.time_interval, 1/self.Current_Signal.sampling_rate)  
            # sampled_data = np.interp(sampled_time, self.Current_Signal.time, self.Current_Signal.amplitude)
            # # marking the samples at graph1 plot
            # scatter_plot = pg.ScatterPlotItem(
            #     x=sampled_time, y=sampled_data, pen='r', symbol='x', size=10)
            # self.graph_1.widget.addItem(scatter_plot)