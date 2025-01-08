import numpy as np

class Signal:
    def __init__(self ,   time, amplitude , name ):
     #    list of components
        
        self.Components=[] 
        self.amplitude =amplitude 
        self.time=time
        self.amplitude_one_cycle=[]
        self.name=name
        self.maxfrequancy=0
        self.time_interval=time[3]-time[2]
        self.sampling_rate_freq=0
        self.Resampled_data=[]
        self.Resampled_time=[]
        self.Amplitude_rep=[]
        self.noise=np.zeros(1000)
        self.time_rep=[]
        self.noise_power=0

    def Remove_component(self , component):
        self.Components.remove(component)
        phase_rad = np.deg2rad(component.phase)
        component_data = component.amplitude * np.cos(2 * np.pi * component.frequancy * self.time + phase_rad)
        self.amplitude -= component_data 
        self.maxfrequancy=0
        self.Update_max_Frequancy()
        self.Update_Sampling_rate(self.maxfrequancy)


    def Update_max_Frequancy(self):
        for component in self.Components:
            if component.frequancy > self.maxfrequancy:
                self.maxfrequancy=component.frequancy
    
    def Update_Sampling_rate(self, value):
        self.sampling_rate_freq=value


    def Generate_Signal(self,time):
        amplitude=np.zeros_like(time)
        for comp in self.Components:
            amplitude += comp.amplitude * np.cos(2 * np.pi * comp.frequancy * time + comp.phase)
        return amplitude







