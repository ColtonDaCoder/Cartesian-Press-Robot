class profile:
    def __init__(self, acceleration, min_velocity, max_velocity, total):
        self.a = acceleration
        self.vmin = min_velocity
        self.vmax = max_velocity
        self.total = total
        self.middle = self.total - (2 * (self.vmin - self.vmax) / self.a)

    #calculate on each new step
    def calculate(self, step):
        #steps for ramp up / ramp down
        ramp = (self.vmin - self.vmax) / self.a
        #acceleration
        #(for trapezoidal: max velocity steps > 0) or (for triangular: max velocity steps < 0)
        if (step < ramp and self.middle > 0) or (step < self.total / 2 and self.middle < 0):
            return (-self.a * step) + self.vmin
        #max velocity
        elif step < self.middle + ramp:
            return self.vmax
        #decceleration
        else:
            return self.a * (step - self.total) + self.vmin