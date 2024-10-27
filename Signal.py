import numpy as np

class Signal:
    def __init__(self ,   time, amplitude , name ):
     #    list of components
        
        self.Components=[] 
        self.amplitude =amplitude 
        self.time=time
        self.noise=[]
        self.name=name
        self.maxfrequancy=0
        self.time_interval=time[3]-time[2]
        self.sampling_rate_freq=0
        self.Resampled_data=[]




    def Remove_component(self , component):
        self.Components.remove(component)
        phase_rad = np.deg2rad(component.phase)
        component_data = component.amplitude * np.sin(2 * np.pi * component.frequancy * self.time + phase_rad)
        self.amplitude -= component_data 
        self.maxfrequancy=0
        self.Update_max_Frequancy()


    def Update_max_Frequancy(self):
        for component in self.Components:
            if component.frequancy > self.maxfrequancy:
                self.maxfrequancy=component.frequancy











