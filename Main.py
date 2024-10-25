from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from Signal import Signal

from scipy.fft import fft
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog ,QApplication , QMainWindow,QColorDialog , QLabel
import sys
import pandas as pd 
import math
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QPushButton, QWidget, QVBoxLayout , QHBoxLayout
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from PyQt5 import uic


from Component import Component
from Widget import Widget

Ui_MainWindow, QtBaseClass = uic.loadUiType("Task02.ui")


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        # self.combined_signal=np.zeros(1000)
        self.PushButton_AddComponent.clicked.connect(self.addCompnent)
        
        
        self.PushButton_UploadSignal.clicked.connect(self.Upload_Signal) 
        
        self.graph_1=Widget(self.Widget_1)
        self.graph_2=Widget(self.Widget_2)
        self.graph_3=Widget(self.Widget_3)
        self.graph_4=Widget(self.Widget_4, 'frequancy' , 'Amplitude')
      
        self.Current_Signal=None

        

    
        





    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;CSV Files (*.csv);;DAT Files (*.dat);;XLSX Files (*.xlsx);;TXT Files (*.txt)", options=options)
        
        if fileName:
            print(f"Selected file: {fileName}")
            try:
                return fileName
            except Exception as e:
                print(f"Error opening file: {e}")
                return None
        else:
            print("No file selected")
            return None


    def read_file(self, fileName):
        if fileName.endswith('.csv'):
            df = pd.read_csv(fileName)
        elif fileName.endswith('.xlsx'):
            df = pd.read_excel(fileName)
        elif fileName.endswith('.dat') or fileName.endswith('.txt'):
            df = pd.read_csv(fileName, sep='\t')
        time = df.iloc[:, 0].to_numpy()
        amplitude =df.iloc[:, 1].to_numpy()        
        return time, amplitude 
    

    def addCompnent(self):
        frequancy=self.SpinBox_Frequency.value()
        amplitude=self.SpinBox_Amplitude.value()
        phase=self.SpinBox_Phase.value()
        Component_tst=Component(frequancy , phase , amplitude)
        time=np.linspace(0 , 3, 1000)
        
        phase_rad = np.deg2rad(phase)  
        signal_data = amplitude * np.sin(2 * np.pi * frequancy * time + phase_rad)  # Generate signal
        
        # self.combined_signal += signal
        # # pen=pg.mkPen(width=3)
        # self.Widget_1.plot(time , self.combined_signal  )
        # self.Add_ComponentList(Component_tst)
        signal=Signal(time , signal_data , "tesst")
        self.Get_MaxFrequancy(signal)
        self.Add_SignalList(signal)


        
   

    def Upload_Signal(self):
        fileName=self.browse_file()
        if fileName :
            time , amplitude = self.read_file(fileName)
            name=fileName.split('/')[-1].split('.')[0] 
            signal=Signal(time[:1000], amplitude[:1000], name )
            self.Get_MaxFrequancy(signal)
            print(f"signal max frequency: {signal.maxfrequancy} Hz , len:{len(time[:1000])}")
            self.Add_SignalList(signal)



     
    def Get_MaxFrequancy(self , signal):
        fft_result = fft(signal.amplitude)
        frequencies = np.fft.fftfreq(len(fft_result), d=signal.time_interval)
        magnitude = np.abs(fft_result)
        fmax_index = np.argmax(magnitude)
        fmax = np.abs(frequencies[fmax_index])
        signal.maxfrequancy=fmax
        print(f"max frequancy : {signal.maxfrequancy}")



    # here create a widget , layout >> add label , button to layout , add layout to widget >> add the widget as item to widgetlist
    def Add_SignalList(self, signal):
        text = signal.name

        # Create custom widget
        custom_widget = QWidget()
        layout = QHBoxLayout()

        # Create and style the label for the signal name
        label = QLabel(text)
        label.setStyleSheet("""
            color: black;
            background-color: rgba(0, 0, 0, 0);
            font-family: opensans;
            font-weight: 500;
            padding: 5px;
            margin-left: 10px;
        """)

        # Create the delete button with an icon
        icon_button = QPushButton()
        icon_button.setIcon(QIcon("DeleteIcon.png"))
        icon_button.setFixedSize(20, 20)
        icon_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(200, 0, 0, 0.3);  /* Red hover effect */
                border-radius: 10px;
            }
        """)

        layout.addWidget(icon_button)
        layout.addWidget(label)
        layout.setContentsMargins(5, 5, 5, 5) 
        layout.setSpacing(10)

        custom_widget.setLayout(layout)
        custom_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 10px;
            }
        """)
   
    #    create a item
        item = QListWidgetItem()
        item.setSizeHint(custom_widget.sizeHint())
        self.ListWidget_Signals.addItem(item)
        self.ListWidget_Signals.setItemWidget(item, custom_widget)

        
        
        item.setData(Qt.UserRole, signal)    
        custom_widget.mousePressEvent = lambda event: self.Plot_OriginalSignal(signal)     
        icon_button.clicked.connect(lambda: self.Remove_Signal(item))


        # call the plotfunction for new signal
        self.Plot_OriginalSignal(signal)


    def Remove_Signal(self, item):
        index = self.ListWidget_Signals.row(item) 
        deleted_signal = item.data(Qt.UserRole) 
        self.ListWidget_Signals.takeItem(index)   
        if deleted_signal == self.Current_Signal:
            length = self.ListWidget_Signals.count() 
            # set the new signal the last signal in the listt
            item = self.ListWidget_Signals.item(length-1)  
            signal=None
            if item : signal = item.data(Qt.UserRole)               
             
            # call ploting function to plot new sidnal shifted 
            self.Plot_OriginalSignal(signal)



    def Plot_OriginalSignal(self , Signal):
        self.graph_1.clear_Widget()
        if Signal :
            self.Current_Signal=Signal
            self.graph_1.plot.setData(self.Current_Signal.time , self.Current_Signal.amplitude )
            self.graph_1.widget.setTitle(self.Current_Signal.name)

            # self.Current_Signal.sampling_rate=2*self.Current_Signal.maxfrequancy
            # sampled_time = np.arange(
            # self.Current_Signal.time[0], self.Current_Signal.time[-1]+ 2*self.Current_Signal.time_interval, 1/self.Current_Signal.sampling_rate)  
            # sampled_data = np.interp(sampled_time, self.Current_Signal.time, self.Current_Signal.amplitude)
            # # marking the samples at graph1 plot
            # scatter_plot = pg.ScatterPlotItem(
            #     x=sampled_time, y=sampled_data, pen='r', symbol='x', size=10)
            # self.graph_1.widget.addItem(scatter_plot)










        

        




if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    MainWindow_ = MainWindow()
    MainWindow_.show()
    sys.exit(app.exec_())