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
        self.sampling_rate=0
