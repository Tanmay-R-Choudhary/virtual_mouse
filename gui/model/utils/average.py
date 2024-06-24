class Average:
    def __init__(self, lim=7):
        self.x = []
        self.y = []
        self.lim = lim
    
    def get(self, x, y):
        if len(self.x) == self.lim and len(self.y) == self.lim:
            self.x.pop(0)
            self.y.pop(0)
        
        self.x.append(x)
        self.y.append(y)
        
        return sum(self.x) / self.lim, sum(self.y) / self.lim
    