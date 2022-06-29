import tkinter as tk
import json
import os
import gui_lib
from robot import robot
from vector import vector
from threading import Thread
from queue import Queue
import config_gui_mod as cgm
class main_win(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.frame = self.master
        self.frame.title("Main")
        self.frame.geometry('650x200')
        self.CONTROL = Queue()
        self.control_hold = "idle"
        self.CONTROL.put(self.control_hold)
        self.STEPS = Queue()
        self.Robot = robot(self.CONTROL, self.STEPS)
        self.robot_thread = Thread(target=self.start_robot, args=(self.Robot,), daemon=True)
        self.INIT = False
        self.menu()
        self.grid(column=8,row=24)
        self.window()
        self.robot_thread.start()
        self.INIT = True

    def start_robot(self, Robot):
        Robot.loop()
    def menu(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open Parts", command=self.open_parts)
        self.filemenu.add_command(label="Open Coordinates", command=self.open_cords)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.configmenu = tk.Menu(self.menubar, tearoff=0)
        self.configmenu.add_command(label="New Part", command=self.new_config)
        self.configmenu.add_command(label="Config Coordinates", command=self.config_cords)
        self.menubar.add_cascade(label="Config", menu=self.configmenu)
        self.master.config(menu=self.menubar)  
    def window(self):
        self.frame.columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        #self.robot.set_cords(vector(0,0))
        self.start = tk.Button(text="run", height=1, width=10, bg="green", command=self.execute)
        self.start.grid(row=4, column=0, sticky='se')
        self.stop = tk.Button(text="stop", height=1, width=10, bg="red", command=self.disable)
        self.stop.grid(row=4, column=1, sticky='se')
        self.to_home = tk.Button(text="to home", height = 1, width=10, bg="blue", command=self.home)
        self.to_home.grid(row=5, column=0, sticky='se')
        self.button_control = tk.Button(text="button control", height=1, width=10, bg="orange", command=self.button)
        self.button_control.grid(row=5, column=5, sticky='se')
        self.rezero = tk.Button(text="zero robot", height=1, width=10, bg="yellow", command=self.zero)
        self.rezero.grid(row=7, column=5, sticky='se')
        self.variable = tk.StringVar()
        self.part_select = tk.Label(text="Part:")
        self.part_select.grid(row=0, column=4, sticky='se')
        self.part_option = tk.OptionMenu(self.master, self.variable, *gui_lib.get_json("parts.json").keys())
        self.part_option.grid(row=0, column=5, sticky='sew')
        #motor counts
        self.motors_label = tk.Label(text="Motors:")
        self.motors_label.grid(row=0, column=0, sticky= 'sw', padx=15)

        self.x_label = tk.Label(text="X:")
        self.x_label.grid(row=1, column=0, sticky='sw', padx=15)

        self.x_print = tk.Text(height=1, width=10)
        self.x_print.grid(row=1, column=0, sticky='se')

        self.y_label = tk.Label(text="Y:")
        self.y_label.grid(row=1, column=1, sticky='sw', padx=15)

        self.y_print = tk.Text(height=1, width=10)
        self.y_print.grid(row=1, column=1, sticky='se')
        #pneumatic booleans
        self.pneumatics_label = tk.Label(text="Pneumatics:")
        self.pneumatics_label.grid(row=3, column=4, sticky='sw', padx=15)

        self.y_pneu_label = tk.Label(text="Y:")
        self.y_pneu_label.grid(row=4, column=4, sticky='sw', padx=15)

        self.y_pneu_print = tk.Text(height=1, width=10)
        self.y_pneu_print.grid(row=4, column=4, sticky='se')

        self.z_pneu_label = tk.Label(text="Z:")
        self.z_pneu_label.grid(row=5, column=4, sticky='sw', padx=15)

        self.z_pneu_print = tk.Text(height=1, width=10)
        self.z_pneu_print.grid(row=5, column=4, sticky='se')

        self.rot_pneu_label = tk.Label(text="Rot:")
        self.rot_pneu_label.grid(row=6, column=4, sticky='sw', padx=15)

        self.rot_pneu_print = tk.Text(height=1, width=10)
        self.rot_pneu_print.grid(row=6, column=4, sticky='se')
        #button control
        self.button_control_distance = tk.Text(height=1, width=10)
        self.button_control_distance.grid(row=4, column=5, sticky='se')
        self.run_queues()

    def open_parts(self):
        os.system("parts.json, file.txt")
    def open_cords(self):
        os.system("cords.json, file.txt")
    def new_config(self):
        cgm.config_part()
    def config_cords(self):
        cgm.config_cords()
    def exit(self):
        self.master.destroy()


    def run_queues(self):
        self.x_print.delete(0.0, 'end')
        self.y_print.delete(0.0, 'end')

        self.y_pneu_print.delete(0.0, 'end')
        self.z_pneu_print.delete(0.0, 'end')
        self.rot_pneu_print.delete(0.0, 'end')

        cords = vector(0,0)
        if(self.INIT):
            cords = self.STEPS.get()

        self.x_print.insert("end", cords.x)
        self.y_print.insert("end", cords.y)

        self.y_pneu_print.insert("end", self.Robot.y_pneumatic.open)
        self.z_pneu_print.insert("end", self.Robot.z_pneumatic.open)
        self.rot_pneu_print.insert("end", self.Robot.rot_pneumatic.open)

        self.CONTROL.put(self.control_hold)
        self.control_hold = "idle"

        self.after(100, self.run_queues)


    def execute(self):
        self.start["state"] = tk.DISABLED
        self.to_home["state"] = tk.DISABLED
        self.button_control["state"] = tk.DISABLED
        self.control_hold = "start"
    def disable(self):
        self.start["state"] = tk.NORMAL
        self.to_home["state"] = tk.NORMAL
        self.button_control["state"] = tk.NORMAL
        self.control_hold = "disable"
        print("stopped")
        self.unbind_all("<KeyPress>")
    def home(self):
        self.start["state"] = tk.DISABLED
        self.to_home["state"] = tk.DISABLED
        self.button_control["state"] = tk.DISABLED
        self.control_hold = "home"
    def button(self):
        self.start["state"] = tk.DISABLED
        self.to_home["state"] = tk.DISABLED
        self.button_control["state"] = tk.DISABLED
        self.bind_all("<KeyPress>", self.keyPress)
    def zero(self):
        self.control_hold = "zero"
    def clean_part(self):
        self.disable()
    def keyPress(self, event):
        key = event.keysym
        distance = 0
        distance = self.button_control_distance.get(0.0,"end")
        if distance == "\n": distance = "0"
        if key == "Up":
            self.control_hold = "U" + distance
        elif(key == "Down"):
            self.control_hold = "D" + distance
        elif(key == "Left"):
            self.control_hold = "L" + distance
        elif(key == "Right"):
            self.control_hold = "R" + distance
        elif(key == "y"):
            self.control_hold = "y"
        elif(key == "z"):
            self.control_hold = "z"
        elif(key == "r"):
            self.control_hold = "r"

if __name__ == '__main__':
    main = main_win()
    main.mainloop()
    main.Robot.cartesian.cleanup()
    

    