
from pyqtgraph import PlotWidget
import pyqtgraph as pg
class Widget():
    def __init__(self , Widget_Obj , x_label= 'Time', y_label='Amplitude') :
       
        self.widget=Widget_Obj
       
        self.pen=pg.mkPen(color=(86, 140, 249), width=2)
        self.plot=Widget_Obj.plot(pen=self.pen)        
        
        self.widget.setLabel('left', y_label)  
        self.widget.setLabel('bottom', x_label) 
        self.widget.setBackground('w')
 
        self.scatter_plot=None



        




    def clear_Widget(self):
        self.plot.setData([] , [])
        self.widget.setTitle("")
        if self.scatter_plot:
            self.widget.removeItem(self.scatter_plot)
        
    def Scatter_Plot_func(self , plot):
        self.scatter_plot=plot
        self.widget.addItem(self.scatter_plot)

    def set_Range_Limits(self, xmin , xmax , ymin , ymax):
        self.widget.getAxis('bottom').setTickSpacing(major=0.1, minor=0.05)
        self.widget.setXRange(xmin , xmax)
        self.widget.setYRange(ymin , ymax)







     




        
