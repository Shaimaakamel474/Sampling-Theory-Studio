
from PyQt5.QtCore import Qt

from Signal import Signal

from scipy.fft import fft
from PyQt5.QtGui import QIcon
from scipy.interpolate import interp1d
import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog ,QApplication , QMainWindow , QLabel
import sys
import pandas as pd 

import numpy as np


from PyQt5.QtWidgets import QApplication, QListWidgetItem, QPushButton, QWidget, QHBoxLayout

from PyQt5 import uic


from Component import Component
from Widget import Widget

Ui_MainWindow, QtBaseClass = uic.loadUiType("Task02.ui")


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)

        self.combined_signal=np.zeros(1000)
        self.time=np.linspace(0 , 2.1, 1000)
        self.componentsList=[]

        self.Signals=[]
        self.Current_Signal=None
        
        self.PushButton_AddComponent.clicked.connect(self.CreateNewComponent)
        self.PushButton_UploadSignal.clicked.connect(self.Upload_Signal) 
        self.PushButton_GenerateSignal.clicked.connect(self.Generate_Mixed_Signal)
        self.HorizontalSlider_SamplingFrequancy.valueChanged.connect(lambda value: self.change_Sampling_Rate(self.Current_Signal, value))
        self.PushButton_GenerateSignal.setEnabled(False)

        # create 4 objects from Widget Class
        self.graph_1=Widget(self.Widget_1)
        self.graph_2=Widget(self.Widget_2)
        self.graph_3=Widget(self.Widget_3)
        self.graph_4=Widget(self.Widget_4, 'frequancy' , 'Amplitude')
      

        
        # t = np.arange(0, 2.1, 1/1000 ,  dtype=np.float64)
        # print(len(t))
        # testSignal=(np.sin(2 * np.pi * 10 * t) + 
        #             2 * np.sin(2 * np.pi * 40 * t) + 
        #             0.25 * np.sin(2 * np.pi * 60 * t))
        # self.CreatedSignal=Signal(t , testSignal , "testSignal")
        # self.CreatedSignal.maxfrequancy=100
        # # set it as default fmax 
        # self.CreatedSignal.sampling_rate_freq= self.CreatedSignal.maxfrequancy
        # self.HorizontalSlider_SamplingFrequancy.setValue(10)
        # self.LineEdit_SetSamplingFrequancy.setText(str(1))
        # self.Current_Signal=self.CreatedSignal
        # self.Plot_OriginalSignal(self.Current_Signal)







    # show Browser , return File path
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

    # read file data : columns (0>Time & 1 >Amplitude)
    def read_file(self, fileName):
        if fileName.endswith('.csv'):
            df = pd.read_csv(fileName)
        elif fileName.endswith('.xlsx'):
            df = pd.read_excel(fileName)
        elif fileName.endswith('.dat') or fileName.endswith('.txt'):
            df = pd.read_csv(fileName, sep='\t')
    #    read the column 0 >> time 
        time = df.iloc[:, 0].to_numpy()
    # read  the coulmn 1 >> Amplitude
        amplitude =df.iloc[:, 1].to_numpy()        
        return time, amplitude 
    

      
    # here create a widget , Hor..layout >> add label , delete button to layout , add layout to widget 
    # >> add the widget as item (create item , connect the widget to it )to widgetlist   
    def Add_ItemLists(self , List , obj):
                # Create custom widget , layout
        custom_widget = QWidget()
        layout = QHBoxLayout()
        # Create and style the label for the signal name
        label = QLabel(obj.name)
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
       
    #    add delete button , label for Hlayout
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
        List.addItem(item)

        # connect the item with the custom widget
        List.setItemWidget(item, custom_widget)
        item.setData(Qt.UserRole, obj) 
        return custom_widget , icon_button , item


   




    def CreateNewComponent(self):
        # get component data 
        frequancy=self.SpinBox_Frequency.value()
        amplitude=self.SpinBox_Amplitude.value()
        phase=self.SpinBox_Phase.value()
        
        Curr_Component=Component(frequancy , phase , amplitude)
        
        
        phase_rad = np.deg2rad(phase)  
        Component_data = amplitude * np.sin(2 * np.pi * frequancy * self.time + phase_rad)  # Generate signal
        self.combined_signal += Component_data
       
        self.componentsList.append(Curr_Component)
        self.graph_1.plot.setData(self.time , self.combined_signal)
        self.graph_1.widget.setTitle("Generate New Signal")
        self.AddComop_ListGeneration(Curr_Component)
        self.PushButton_GenerateSignal.setEnabled(True)

   
    
    

    def AddComop_ListGeneration(self , component):
        _ , icon_button , item= self.Add_ItemLists(self.ListWidget_SignalGeneration ,component )
        icon_button.clicked.connect(lambda event : self.Remove_NewComponent(item))

    
      
    def Remove_NewComponent(self, item):
        component_to_remove = item.data(Qt.UserRole)
        # Remove its data from the combined signal
        phase_rad = np.deg2rad(component_to_remove.phase)
        component_data = component_to_remove.amplitude * np.sin(2 * np.pi * component_to_remove.frequancy * self.time + phase_rad)
        self.combined_signal -= component_data  # Subtract component signal data

        # Remove the component from componentsList
        self.componentsList.remove(component_to_remove)

        # Remove the item from the ListWidget_SignalGeneration
        index = self.ListWidget_SignalGeneration.row(item)
        self.ListWidget_SignalGeneration.takeItem(index)
        length = self.ListWidget_SignalGeneration.count() 

        # Update the combined signal graph to reflect removal
        if length >0:       
           self.graph_1.plot.setData(self.time, self.combined_signal)
        else:
            self.graph_1.clear_Widget()
            # reset all thing 
            self.PushButton_GenerateSignal.setEnabled(False)
            self.combined_signal=np.zeros(1000)
            self.componentsList=[]
            self.ListWidget_SignalGeneration.clear()
            self.SpinBox_Frequency.setValue(0)
            self.SpinBox_Amplitude.setValue(0)
            self.SpinBox_Phase.setValue(0)
            if len(self.Signals)>0:
                # print("entered here")
                self.Current_Signal=self.Signals[len(self.Signals) - 1]
                self.show_signalcomponent(self.Current_Signal)



    


    def Generate_Mixed_Signal(self):
        num=len(self.Signals)
        signal=Signal(self.time , self.combined_signal , f"Signal_{num+1}" )
        self.Signals.append(signal)
        signal.Components=self.componentsList
        signal.Update_max_Frequancy()
        print(f" max freq in generation : {signal.maxfrequancy}")
        
        # reset all thing 
        self.combined_signal=np.zeros(1000)
        self.componentsList=[]
        self.ListWidget_SignalGeneration.clear()
        self.SpinBox_Frequency.setValue(0)
        self.SpinBox_Amplitude.setValue(0)
        self.SpinBox_Phase.setValue(0)
        
        self.Current_Signal=signal
        self.Add_SignalList(signal)
        

    


    def Add_SignalList(self, signal):
        custom_widget ,icon_button , item= self.Add_ItemLists(self.ListWidget_Signals , signal)
      
       # click on the widget >> plot 
        custom_widget.mousePressEvent = lambda event : self.show_signalcomponent(signal)     
        # when click on delete 
        icon_button.clicked.connect(lambda: self.Remove_Signal(item))
        
        # call the plotfunction for new signal
        self.ListWidget_Components.clear() 
        for component in signal.Components:
            self.Add_SignalComponents(component)
        self.Plot_OriginalSignal(signal)
    

    

    def Add_SignalComponents(self , component):
       _ ,icon_button , item= self.Add_ItemLists(self.ListWidget_Components ,component)
       icon_button.clicked.connect(lambda event : self.RemoveSignalComponent(item))

    
    def RemoveSignalComponent(self , item):
        # print("hereeeee in remove ")
        component_to_remove = item.data(Qt.UserRole)
        index = self.ListWidget_Components.row(item)
        self.ListWidget_Components.takeItem(index)
        if len( self.Current_Signal.Components)>1:
        #    print(f"len now is {len( self.Current_Signal.Components)}")
           self.Current_Signal.Remove_component(component_to_remove)
           print(f" the max freq after delete component : {self.Current_Signal.maxfrequancy}")
           self.Plot_OriginalSignal(self.Current_Signal)
        else :
            # last component
            # print("here last comp")
            self.graph_1.clear_Widget()
            self.Signals.remove(self.Current_Signal)
            item=self.find_item_by_data(self.ListWidget_Signals,self.Current_Signal)
            self.Remove_Signal(item)
            

    def find_item_by_data(self, List,data):
        # Iterate over all items in the ListWidget
        for index in range(List.count()):
            item = List.item(index) 
            # Check if the item's data matches the given data
            if item.data(Qt.UserRole) == data:
                return item
   
   
    # add New signal 
    def Upload_Signal(self):
        fileName=self.browse_file()
        if fileName :
            time , amplitude = self.read_file(fileName)
            name=fileName.split('/')[-1].split('.')[0] 
            # take 1000 points onlyy
            signal=Signal(time[:1000], amplitude[:1000], name )
            self.Current_Signal=signal     
            self.Get_MaxFrequancy(signal)
            self.Add_SignalList(signal)



     
    def Get_MaxFrequancy(self , signal):
        fft_result = fft(signal.amplitude)  # Perform FFT
        frequencies = np.fft.fftfreq(len(fft_result), signal.time_interval)  # Frequency bins
        frequencies=frequencies[:(len(fft_result))//2]
        # based on magintude
        # dominant_freq = frequencies[np.argmax(2.0 / 1000* np.abs(fft_result[:1000// 2]))]
        signal.maxfrequancy=np.max(frequencies)
        print(f" max_frequency : {signal.maxfrequancy}")
    


    def show_signalcomponent(self , signal):
        self.ListWidget_Components.clear()
        if signal :
            for component in signal.Components:
                self.Add_SignalComponents(component)
            self.Plot_OriginalSignal(signal)
        else:
            self.graph_1.clear_Widget()



    def Remove_Signal(self, item):        
        index = self.ListWidget_Signals.row(item) 
        deleted_signal = item.data(Qt.UserRole)
        # print(f"here in remove signalll {deleted_signal.name}")
        self.ListWidget_Components.clear()     
        self.ListWidget_Signals.takeItem(index)    
        if deleted_signal == self.Current_Signal:      
            length = self.ListWidget_Signals.count() 
            # set the new signal the last signal in the listt
            item = self.ListWidget_Signals.item(length-1)  
            New_signal=None
            if item : 
                New_signal = item.data(Qt.UserRole)                      
            # call ploting function to plot new sidnal shifted 
            self.show_signalcomponent(New_signal)


    def Plot_OriginalSignal(self , Signal):
        # class method

        self.graph_1.clear_Widget()
        if Signal :
            self.Current_Signal=Signal
            self.graph_1.plot.setData(self.Current_Signal.time , self.Current_Signal.amplitude )
            self.graph_1.widget.setTitle(self.Current_Signal.name)

            # # create the sampling points 
            # time_sampling=np.arange(0,2.1, 1/self.Current_Signal.sampling_rate_freq ,  dtype=np.float64)
            # data_sampling=interp1d(self.Current_Signal.time, self.Current_Signal.amplitude,
            #                         kind='linear', fill_value='extrapolate')(time_sampling) 
            # # draw a sampling points 
            # scatter_plot = pg.ScatterPlotItem(
            # x=time_sampling, y=data_sampling, pen='r', symbol='x', size=10)
            # self.graph_1.widget.addItem(scatter_plot)



            # interpolated_data=self.reconstruct_signal(self.Current_Signal , time_sampling , data_sampling)
            # self.graph_2.plot.setData(self.Current_Signal.time , interpolated_data)
           
            # difference_signal=np.abs(self.Current_Signal.amplitude - interpolated_data)
            # self.graph_3.plot.setData(self.Current_Signal.time , difference_signal)
            

    def reconstruct_signal( self , signal , time_sampling , data_sampling):
        interpolated_data = np.zeros_like(signal.time, dtype=np.float64)
        N=len(signal.time)
        sampling_interval=1/signal.sampling_rate_freq
        for i in range(len(time_sampling)):  # Convolution using sinc
            interpolated_data += data_sampling[i] * np.sinc((signal.time - time_sampling[i]) /sampling_interval )
        return interpolated_data

    def change_Sampling_Rate(self , signal , value ):
      if signal :
        signal.sampling_rate_freq= signal.maxfrequancy  *(value / 10)
        self.LineEdit_SetSamplingFrequancy.setText(str(value / 10))
        

        self.Plot_OriginalSignal(self.Current_Signal)

    





        

        




if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    MainWindow_ = MainWindow()
    MainWindow_.show()
    sys.exit(app.exec_())