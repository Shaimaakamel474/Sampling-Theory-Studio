class Component:
    def __init__(self , frequancy , phase , amplitude):
        self.frequancy=frequancy
        self.amplitude=amplitude
        self.phase=phase
        self.name= f"signal: {self.frequancy} Hz, {self.amplitude} V, {self.phase} degrees"

    def __str__(self):
        return f"signal: {self.frequancy} Hz, {self.amplitude} V, {self.phase} degrees"