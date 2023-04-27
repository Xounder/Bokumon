import time

class Timer:
    def __init__(self, dt):
        self.start_time = 0
        self.current_time = 0
        self.dt = dt
        self.run = False
    
    def active(self):
        self.run = True
        self.start_time = time.time()

    def update(self):
        if self.run:
            self.current_time = time.time()
            if (self.current_time - self.start_time) >= self.dt:
                self.run = False
                    