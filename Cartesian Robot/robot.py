from queue import Queue
from threading import Event
from subsystems import Cartesian, Pneumatic
from collections import deque
from vector import vector
import json
import time
from threading import Thread
import sys
class robot:
    def __init__(self, CONTROL, STEPS):
        self.disable_event = Event()
        self.disable_event.set()
        self.enable_event = Event()
        self.enable_event.clear()
        self.thread_stack = deque()
        self.cartesian = Cartesian(self.disable_event)
        self.y_pneumatic = Pneumatic(1, self.disable_event)  
        self.z_pneumatic = Pneumatic(3, self.disable_event)
        self.rot_pneumatic = Pneumatic(5, self.disable_event)
        self.STEPS = STEPS
        self.CONTROL = CONTROL
        self.thread = Thread(target=self.routine, args=(self.enable_event, self.thread_stack,), daemon=True)


    def loop(self):
        while True:
            self.check_controls(self.CONTROL)
            time.sleep(0.1)


    def check_controls(self, CONTROL):
        command = CONTROL.get()
        if(len(self.thread_stack) == 0 or not command == "idle"):
            self.thread_stack.clear() 
            self.thread_stack.append(command)
        #start thread on first start
        if not self.thread.is_alive(): self.thread.start()
        #if disable command, set disable event
        if command == "disable":
            self.disable_event.set()
            self.enable_event.clear()
        #but if command is not disable and is not priority, clear disable
        elif not command == "idle" and not command == "zero":
            self.disable_event.clear()
            #if priority command is start, set enable_event
            if command == "start":
                self.enable_event.set()
            else:
                self.enable_event.clear()
        #non priority commands
        if command == "zero":
            self.set_cords(vector(0,0))
        self.STEPS.put(self.get_cords())


    def set_part_name(self, part_name):
        self.part_name = part_name
    def get_part_name(self):
        return self.part_name
    
    def to_part(self):
        self.__to_target("part")
    def to_scale1(self):
        self.__to_target("scale1")
    def to_scale2(self):
        self.__to_target("scale2")
    def to_plate(self):
        self.__to_target("plate")
    def to_home(self):
        self.cartesian.move_steps(self.cartesian.get_steps(vector(0,0)))
    def __to_target(self, name):
        self.cartesian.move_steps(self.cartesian.get_steps(self.get_target(name)))
    
    def move_to(self, cords):
        self.cartesian.move_steps(self.cartesian.get_steps(cords))
    def move(self, cords):
        self.cartesian.move_steps(cords)
    def move_x(self, x):
        self.cartesian.move_steps(vector(x, 0))
    def move_y(self, y):
        self.cartesian.move_steps(vector(0, y))
        
    def set_cords(self, cords):
        self.cartesian.set_cords(cords)
    def get_cords(self):
        return self.cartesian.get_cords()

    def get_target(self, target):
        json_file = open("cords.json")
        cords_list = json.load(json_file)
        json_file.close()
        cords = vector(int(cords_list[target].get("x")), int(cords_list[target].get("y")))
        return cords

    def y_actuate(self, open):
        self.actuate(self.y_pneumatic, open)
    def z_actuate(self, open):
        self.actuate(self.z_pneumatic, open)
    def rot_actuate(self, open):
        self.actuate(self.rot_pneumatic, open)
    def actuate(self, pneumatic, open):
        if open: pneumatic.set_on()
        else: pneumatic.set_off()

    def routine(self, enable_event, thread_stack):
        if enable_event.isSet():
            self.to_part()
            self.y_actuate(True)
            self.to_plate()
            self.y_actuate(False)
            #self.routine(disable)
        command = thread_stack.pop()

        if command[0] == "U":
            self.move_y(int(command[1:]))
        elif command[0] == "D":
            self.move_y(-int(command[1:]))
        elif command[0] == "L":
            self.move_x(-int(command[1:]))
        elif command[0] == "R":
            self.move_x(int(command[1:]))
        elif command == "y":
            self.actuate(self.y_pneumatic, not self.y_pneumatic.open)
        elif command == "z":
            self.actuate(self.z_pneumatic, not self.z_pneumatic.open)
        elif command == "r":
            self.actuate(self.rot_pneumatic, not self.rot_pneumatic.open)

        time.sleep(.5)
        self.routine(enable_event, thread_stack)
        #self.after(100, self.routine(disable_event, queue))
