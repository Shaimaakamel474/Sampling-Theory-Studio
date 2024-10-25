
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
        self.widget.getAxis('bottom').setTickSpacing(major=0.1, minor=0.05)
        # self.widget.setXRange(0 , 2.2)
        # self.widget.setLimits(xMin=0, xMax=2.2, yMin=-1, yMax=1)
    

    def clear_Widget(self):
        self.plot.clear()
        self.widget.setTitle("")
        


     




        
