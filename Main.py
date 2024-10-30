from PyQt5.QtCore import Qt
from Signal import Signal
from scipy.fft import fft
from PyQt5.QtGui import QIcon
from scipy.interpolate import interp1d
import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog ,QApplication , QMainWindow , QLabel
import sys
import pandas as pd 
import math
import numpy as np
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QPushButton, QWidget, QHBoxLayout
from scipy.interpolate import CubicSpline
from PyQt5 import uic
import pywt

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
        self.PushButton_GenerateSignal.setEnabled(False)

        # create 4 objects from Widget Class
        self.graph_1=Widget(self.Widget_1 )
        self.graph_2=Widget(self.Widget_2)
        self.graph_3=Widget(self.Widget_3 )
        self.graph_4=Widget(self.Widget_4,'frequancy' , 'Amplitude')

      
        
        self.Checkbox_IsNormalizedSampling.stateChanged.connect(self.Change_SamplingRate_Method)
        self.HorizontalSlider_SamplingFrequancy.valueChanged.connect(lambda value: self.Change_samplingRate(value))
        self.Combobox_ReconstructionMethod.currentIndexChanged.connect(lambda item_index : self.Reconstruction_Method(item_index))
        self.HorizontalSlider_SNR.valueChanged.connect(self.update_SNR)
        self.HorizontalSlider_SNR.setEnabled(False)
        self.PushButton_SaveSignal.clicked.connect(self.SaveFile)
        self.Combobox_DefualtSignals.currentTextChanged.connect(lambda text: self.Draw_scenario(self.Combobox_DefualtSignals.currentIndex()))

        
        # Default signalll
        self.Combobox_DefualtSignals.setCurrentIndex(0)
        self.Draw_scenario(0)




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
        self.clear_all_graphs()
       
        # self.Set_YRange_Limits(self.combined_signal)
        self.get_Ranges(self.time , self.combined_signal)
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
        self.HorizontalSlider_SNR.setEnabled(True)
        # self.PushButton_SaveSignal.setEnabled(True)
        num=len(self.Signals)
        signal=Signal(self.time , self.combined_signal , f"Signal_{num+1}" )
        self.Signals.append(signal)
        signal.Components=self.componentsList
        signal.Update_max_Frequancy()
        self.Current_Signal=signal

        
        # print(f" max freq in generation : {signal.maxfrequancy}")
        self.Change_samplingRate(signal.maxfrequancy)
        self.HorizontalSlider_SamplingFrequancy.setValue(signal.maxfrequancy)
        self.update_SNR()
        
        # reset all thing 
        self.combined_signal=np.zeros(1000)
        self.componentsList=[]
        self.ListWidget_SignalGeneration.clear()
        self.SpinBox_Frequency.setValue(0)
        self.SpinBox_Amplitude.setValue(0)
        self.SpinBox_Phase.setValue(0)
        

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
           
           self.Change_samplingRate(None)
        #    print(f" the max freq after delete component : {self.Current_Signal.maxfrequancy}")
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
            time , amplitude  = self.read_file(fileName)
            name=fileName.split('/')[-1].split('.')[0] 
            signal=Signal(time[:1000], amplitude[:1000], name )
            self.Current_Signal=signal     
            self.Get_MaxFrequancy(signal)
            print(f" max freq in generation : {signal.maxfrequancy}")
            self.Change_samplingRate(signal.maxfrequancy)
            self.HorizontalSlider_SamplingFrequancy.setValue(signal.maxfrequancy)
            self.HorizontalSlider_SNR.setEnabled(True)
            self.update_SNR()
            self.Add_SignalList(signal)



     
    def Get_MaxFrequancy(self , signal):
        fft_result = fft(signal.amplitude)
        frequencies = np.fft.fftfreq(len(fft_result), signal.time_interval)
        frequencies = frequencies[:len(fft_result)//2]
        magnitude = np.abs(fft_result[:len(fft_result)//2])
        index_of_max = np.argmax(magnitude)
        dominant_frequency = frequencies[index_of_max]
        signal.maxfrequancy = int(max(frequencies//2))
        print(f"max_frequency: {max(frequencies//2)  }  ")

    
    def show_signalcomponent(self , signal):
        self.ListWidget_Components.clear()
        if signal :
            # self.PushButton_SaveSignal.setEnabled(True)
            for component in signal.Components:
                self.Add_SignalComponents(component)
            self.Current_Signal=signal
            self.Change_SamplingRate_Method()
            self.update_SNR()

            self.Plot_OriginalSignal(signal)
        else:
            # the signals is endedd
            self.Reset_Default_Slider()
            self.clear_all_graphs()
            self.Combobox_DefualtSignals.setCurrentIndex(0)
            self.Draw_scenario(0)
            self.HorizontalSlider_SNR.setEnabled(False)
            # self.PushButton_SaveSignal.setEnabled(False)
            self.PushButton_GenerateSignal.setEnabled(False)

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
        self.graph_4.widget.clear()
        self.graph_1.clear_Widget()
        if Signal :
            self.get_Ranges(Signal.time , Signal.amplitude)

            min=np.min(Signal.time)
            max=np.max(Signal.time)
            # print(min , max)
            self.Current_Signal=Signal
            # self.Set_YRange_Limits( self.Current_Signal.amplitude)
            self.graph_1.plot.setData(self.Current_Signal.time , self.Current_Signal.amplitude )
            self.graph_1.widget.setTitle(self.Current_Signal.name)
            # # create the sampling points 
            time_sampling=np.arange(min,max, 1/self.Current_Signal.sampling_rate_freq ,  dtype=np.float64)
            data_sampling=interp1d(self.Current_Signal.time, self.Current_Signal.amplitude,
                                    kind='linear', fill_value='extrapolate')(time_sampling) 
            # draw a sampling points 
            scatter_plot_curr = pg.ScatterPlotItem(
            x=time_sampling, y=data_sampling, pen='r', symbol='x', size=10)
            self.graph_1.Scatter_Plot_func(scatter_plot_curr)
            
            self.Current_Signal.Resampled_time = time_sampling
            self.Current_Signal.Resampled_data=data_sampling


            item=self.Combobox_ReconstructionMethod.currentIndex()
            self.Reconstruction_Method(item)
            self.Graph4_Plot()

    def Shannon_Method(self):
        Signal=self.Current_Signal
        time_sampling=self.Current_Signal.Resampled_time
        data_sampling=self.Current_Signal.Resampled_data
        
        # print(f"Signal.sampling_rate_freq : {Signal.sampling_rate_freq}")
        sinc_matrix = np.sinc((Signal.time[:, None] - time_sampling[None, :]) / (1/Signal.sampling_rate_freq))
        interpolated_data = sinc_matrix.dot(data_sampling)
        return interpolated_data

    def Cubic_Method(self):
        Signal=self.Current_Signal
        time_sampling=self.Current_Signal.Resampled_time
        data_sampling=self.Current_Signal.Resampled_data
        reconstructed_signal = CubicSpline(time_sampling, data_sampling, bc_type="natural")(Signal.time)
        return reconstructed_signal
     
    def wavelet_reconstruction(self, wavelet='db1'):
        # Retrieve the signal data
        signal = self.Current_Signal
        x_samples = signal.Resampled_data
        time_samples = signal.Resampled_time

        # Perform wavelet decomposition
        coeffs = pywt.wavedec(x_samples, wavelet)
        # Perform wavelet reconstruction
        reconstructed_signal = pywt.waverec(coeffs, wavelet)

        # Interpolate to match the original signal's time points
        interpolated_signal = np.interp(
            signal.time,  # Original time points to interpolate
            np.linspace(time_samples[0], time_samples[-1], len(reconstructed_signal)),  # New time points from reconstruction
            reconstructed_signal  # Reconstructed signal values
        )

        return interpolated_signal

    def Fourier_Method(self):
            Signal=self.Current_Signal
            time_sampling=self.Current_Signal.Resampled_time
            data_sampling=self.Current_Signal.Resampled_data
            yf = np.fft.fft(data_sampling)
            reconstructed_signal = np.fft.ifft(yf).real
            reconstructed_signal_interpolated = np.interp(Signal.time, time_sampling, reconstructed_signal)
            return reconstructed_signal_interpolated

    def Reconstruction_Method(self , item_index):
        if item_index ==0 :
            reconstructed_data =self.Shannon_Method()
        elif item_index ==1:
            reconstructed_data =self.Cubic_Method()
        elif item_index==2:
            reconstructed_data=self.Fourier_Method()
        elif item_index==3:
            reconstructed_data=self.wavelet_reconstruction()

        name=self.Combobox_ReconstructionMethod.currentText()
        self.graph_2.plot.setData(self.Current_Signal.time , reconstructed_data) 
        self.graph_2.widget.setTitle(f"Reconctructed {name} Method")       
        difference_signal=(self.Current_Signal.amplitude - reconstructed_data)
        self.graph_3.plot.setData(self.Current_Signal.time , difference_signal)
        self.graph_3.widget.setTitle(" Difference Signal")
                     
  

    # if the normalize is clickedddd
    def Change_SamplingRate_Method(self):
        if self.Current_Signal:
            max_freq=self.Current_Signal.maxfrequancy
            if self.Checkbox_IsNormalizedSampling.isChecked():
                self.set_silder_limits( 0.5 *max_freq, 4 *max_freq , 0.5*max_freq , 0.5*max_freq )
            else:
                self.set_silder_limits( 1, 20*max_freq , 1 , 5 )
            
            # return to the default values >> 1 fmax
            self.HorizontalSlider_SamplingFrequancy.setValue(self.Current_Signal.maxfrequancy)
            self.Current_Signal.Update_Sampling_rate(self.Current_Signal.maxfrequancy)
            self.Display_labels()

    def Change_samplingRate(self , value):
        # print(f"the value : {value}")
        value_final=value if value is not None else self.HorizontalSlider_SamplingFrequancy.value()
        if self.Current_Signal:
            # print("here")
            self.Current_Signal.Update_Sampling_rate(value_final)
            # to update the limitsss
            self.Display_labels()
            self.Plot_OriginalSignal(self.Current_Signal)
            # print(f"sampling rate is {self.Current_Signal.sampling_rate_freq}")


    def set_silder_limits(self , min , max , step1 , step2):
        # print(f" the max : {max}")
        self.HorizontalSlider_SamplingFrequancy.setMinimum(int(min))      
        self.HorizontalSlider_SamplingFrequancy.setMaximum(int(max))    
        self.HorizontalSlider_SamplingFrequancy.setSingleStep(int(step1)) 
        self.HorizontalSlider_SamplingFrequancy.setPageStep(int(step2))
     
    def Display_labels(self ):
        max_freq=self.Current_Signal.maxfrequancy
        if self.Checkbox_IsNormalizedSampling.isChecked():
            unit="Fmax"
            self.set_silder_limits( 0.5 *max_freq, 4 *max_freq , 0.5*max_freq , 0.5*max_freq )
            value=self.Current_Signal.sampling_rate_freq / self.Current_Signal.maxfrequancy
            # value=math.floor(value)
            value=f"{value:.2f}" 
            # print(f"value : {value} ")
        else:
            unit="HZ"
            value=self.Current_Signal.sampling_rate_freq
            self.set_silder_limits( 1, 20*max_freq , 1 , 5 )
        self.Label_SetSamplingFrequancy.setText(str(unit)) 
        self.LineEdit_SetSamplingFrequancy.setText(str(value)) 
    
    def Reset_Default_Slider(self):
        self.HorizontalSlider_SamplingFrequancy.setValue(1)
        self.Label_SetSamplingFrequancy.setText(str("HZ")) 
        self.LineEdit_SetSamplingFrequancy.setText(str(0))
    
    def clear_all_graphs(self):
        self.graph_1.clear_Widget()
        self.graph_2.clear_Widget()
        self.graph_3.clear_Widget()
        self.graph_4.clear_Widget()
        self.graph_4.widget.clear()

    def update_SNR(self):
        self.HorizontalSlider_SNR.setEnabled(True)
        # delete old noise
        self.Current_Signal.amplitude -= self.Current_Signal.noise
        SNR_Value = self.HorizontalSlider_SNR.value()
        self.LineEdit_SetSNRValue.setText(str(SNR_Value))
        signal_power = np.mean(self.Current_Signal.amplitude ** 2)
        noise_power = signal_power / (10 ** (SNR_Value / 10))
        noise = np.sqrt(noise_power) * np.random.normal(size=self.Current_Signal.amplitude.shape)
        self.Current_Signal.noise=noise
        self.Current_Signal.amplitude +=noise 

        self.Plot_OriginalSignal(self.Current_Signal)

    def SaveFile(self):
        print("heree in save file ")
        if self.Current_Signal:
            # Prepare data for saving
            data = {
                "Time": self.Current_Signal.time,
                "Amplitude": self.Current_Signal.amplitude,
                "Max Frequency": [self.Current_Signal.maxfrequancy] * len(self.Current_Signal.time)
            }
            df = pd.DataFrame(data)
            
            # Set the filename based on signal name
            filename = f"{self.Current_Signal.name}.csv"
            try:
                # Save to CSV
                df.to_csv(filename, index=False)
                print(f"File saved as {filename}")
            except Exception as e:
                print(f"Error saving file: {e}")

    def Graph4_Plot(self):
        #clear the graph
        self.graph_4.widget.clear()
        signal = self.Current_Signal  # Assuming Current_Signal has 'amplitude' and 'sampling_rate_freq' attributes
        amplitude = signal.amplitude
        fft_result = fft(amplitude)

        frequencies = np.fft.fftfreq(len(fft_result),1/ (signal.maxfrequancy))
        magnitude = np.abs(fft_result)
        frequencies = frequencies[:len(fft_result)]
        # negativeee
        neg_rep=frequencies - .5*signal.sampling_rate_freq
        neg_plot=pg.PlotDataItem(neg_rep , magnitude , pen=pg.mkPen('g' , width=2))
        self.graph_4.widget.addItem(neg_plot)
        # postiveee
        pos_rep=frequencies + .5*signal.sampling_rate_freq
        pos_plot=pg.PlotDataItem(pos_rep , magnitude , pen=pg.mkPen('b' , width=2))
        self.graph_4.widget.addItem(pos_plot)
        original_plot=pg.PlotDataItem(frequencies , magnitude , pen=pg.mkPen('r' , width=2))
        self.graph_4.widget.addItem(original_plot)


    def Draw_scenario(self , index):
        if index==0:
            df=pd.read_csv("mixed_signal.csv")
            time = df.iloc[:, 0].to_numpy()
            amplitude =df.iloc[:, 1].to_numpy()    
            name="SEN1"
            signal=Signal(time[:1000] , amplitude[:1000] , name) 
            signal.maxfrequancy=6
        elif index==1:
            df=pd.read_csv("square_signal.csv")
            time = df.iloc[:, 0].to_numpy()
            amplitude =df.iloc[:, 1].to_numpy()    
            name="square_signal"
            signal=Signal(time[:1000] , amplitude[:1000] , name) 
            # self.Get_MaxFrequancy(signal)
            signal.maxfrequancy=3
        elif index==2:
            df=pd.read_csv("triangle_signal.csv")
            time = df.iloc[:, 0].to_numpy()
        # read  the coulmn 1 >> Amplitude
            amplitude =df.iloc[:, 1].to_numpy()    
            name="triangle_signal"
            signal=Signal(time[:1000] , amplitude[:1000] , name) 
            # self.Get_MaxFrequancy(signal)
            signal.maxfrequancy=3

        self.Current_Signal=signal
        self.Change_samplingRate(signal.maxfrequancy)
        self.HorizontalSlider_SamplingFrequancy.setValue(signal.maxfrequancy)
        self.update_SNR()
        self.Plot_OriginalSignal(signal)

    def get_Ranges(self , time , amplitude):
        xmin=time[0] 
        xmax=time[-1]
        
        ymin=np.min(amplitude) 
        ymax=np.max(amplitude) 

        self.graph_1.set_Range_Limits(xmin ,xmax ,ymin , ymax)
        self.graph_2.set_Range_Limits(xmin ,xmax ,ymin , ymax)
        


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    MainWindow_ = MainWindow()
    MainWindow_.show()
    sys.exit(app.exec_())