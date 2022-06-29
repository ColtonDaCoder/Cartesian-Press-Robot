from vector import vector
import time
import numpy as np
import trapezoidal_profile as tp
#import RPi.GPIO as GPIO

class Cartesian:
    avg_time = 1.0
    def __init__(self, disable_event):
        self.x_motor = Motor(12, 16, 'x')
        self.y_motor = Motor(8, 10, 'y')
        self.x = 0
        self.y = 0
        self.disable_event = disable_event
        self.CW = 1
        self.CCW = 0
        self.a = 0.000005
        self.vmin = 0.001
        self.vmax = 0.0001
    def move_steps(self, steps):
        self.move(self.x_motor, steps.x, self.a, self.vmin, self.vmax)
        self.move(self.y_motor, steps.y, self.a, self.vmin, self.vmax)

    def move(self, motor, steps, a, vmin, vmax):
        profile = tp.profile(a, vmin, vmax, abs(steps))
        #change direction if needed
        if steps < 0 and motor.dir == self.CCW:
            motor.set_dir(self.CW)
        elif steps > 0 and motor.dir == self.CW:
            motor.set_dir(self.CCW)
        #iterate through steps
        for step in range(abs(steps)):
            #break if a disable event is set
            if self.disable_event.isSet(): break
            #calculate period with trapezoidal profile
            motor.move(profile.calculate(step))
            #update coordinates
            sign = np.sign(steps)
            new_vector = vector(sign, 0) if motor.name == 'x' else vector(0, sign)
            self.set_cords(self.get_cords().add(new_vector))

    def get_steps(self, cords):
        return cords.subtract(self.get_cords())

    def set_cords(self, cords):
        self.x = cords.x
        self.y = cords.y
    def get_cords(self):
        return vector(self.x, self.y)
    
    def cleanup(self):
        self.x_motor.cleanup()
        self.y_motor.cleanup()

class Pneumatic:
    def __init__(self, port, disable_event):
        self.port = port
        self.disable_event = disable_event
        # GPIO.setup(self.port, GPIO.OUT)
        self.open = False
    def set_on(self):
        if not self.disable_event.isSet():
            #GPIO.output(self.port, GPIO.HIGH)
            self.open = True
    def set_off(self):
        if not self.disable_event.isSet():
            #GPIO.output(self.port, GPIO.LOW)
            self.open = False
        
class Motor:
    def __init__(self, STEP, DIR, name):
        self.name = name
        self.DIR = DIR
        self.STEP = STEP
        self.CW = 1#down
        self.CCW = 0#up
        self.dir = self.CCW
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(self.DIR, GPIO.OUT)
        # GPIO.setup(self.STEP, GPIO.OUT)
        # GPIO.output(self.DIR, self.CCW)

    def move(self, period):
        #GPIO.output(self.STEP,GPIO.HIGH)
        time.sleep(period)
        #GPIO.output(self.STEP,GPIO.LOW)
        time.sleep(period)
        
    def set_dir(self, direction):
        #GPIO.output(self.DIR,direction)
        self.dir = direction
        time.sleep(0.1)
        print("Ready")

    def cleanup(self):
        print("cleanup")
        #GPIO.cleanup()
            
        
