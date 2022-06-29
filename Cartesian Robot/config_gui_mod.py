import tkinter as tk
import gui_lib
class config_part(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry('300x150')
        self.title("Part Configuration")
        self.columnconfigure((0,1,2,3), weight=1)
        self.rowconfigure((0,1,2,3,4), weight=2)
        #Name
        self.name = gui_lib.base_entry(self, "Part Name", 0, 1)
        #Diameter
        self.diameter = gui_lib.base_entry(self, "Diameter", 1, 1)
        #X
        self.parts_X = gui_lib.base_entry(self, "Plate X", 2, 1)
        #Y
        self.parts_Y = gui_lib.base_entry(self, "Plate Y", 3, 1)
        #Submit
        self.submit = tk.Button(self, text="Submit", width=15, command=self.submit)
        self.submit.grid(row=4, column=1, columnspan=2)

    def submit(self):
        if self.has_data():                
            gui_lib.append_json({
                self.name.get(): {
                    "diameter": self.diameter.get(),
                    "plate x": self.parts_X.get(),
                    "plate y": self.parts_Y.get()
                }
            })
            self.destroy()
            
    def has_data(self):
        for string in (self.name.get(), "hold"):
            if not string:
                return False
        for input in (self.diameter.get(), self.parts_X.get(), self.parts_Y.get()):
            if not input.strip(".").isnumeric():
                return False
        return True

class config_cords(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry('600x200')
        self.title("Coordinates Configuration")
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.rowconfigure((0), weight=3)
        self.rowconfigure((1, 2, 3, 4, 5), weight=1)
        #Part X
        self.part_X = gui_lib.base_entry(self, "Part X", 0, 0)
        #Part Y
        self.part_Y = gui_lib.base_entry(self, "Part Y", 2, 0)

        #Scale 1 X
        self.scale1_X = gui_lib.base_entry(self, "Scale 1 X", 0, 2)
        #Scale 1 Y
        self.scale1_Y = gui_lib.base_entry(self, "Scale 1 Y", 2, 2)

        #Scale 2 X
        self.scale2_X = gui_lib.base_entry(self, "Scale 2 X", 0, 4)
        #Scale 2 Y
        self.scale2_Y = gui_lib.base_entry(self, "Scale 2 Y", 2, 4)
        
        #Plate X
        self.plate_X = gui_lib.base_entry(self, "Plate X", 0, 6)
        #Plate Y
        self.plate_Y = gui_lib.base_entry(self, "Plate Y", 2, 6)
        
        #Part Submit
        self.submit_part = tk.Button(self, text="Submit", width=5, command=lambda: self.submit("part"))
        self.submit_part.grid(row=3, column=0, columnspan=2)        
        #Scale 1 Submit
        self.submit_scale1 = tk.Button(self, text="Submit", width=5, command=lambda: self.submit("scale1"))
        self.submit_scale1.grid(row=3, column=2, columnspan=2)
        #Scale 2 Submit
        self.submit_scale2 = tk.Button(self, text="Submit", width=5, command=lambda: self.submit("scale2"))
        self.submit_scale2.grid(row=3, column=4, columnspan=2)
        #Plate Submit
        self.submit_plate = tk.Button(self, text="Submit", width=5, command=lambda: self.submit("plate"))
        self.submit_plate.grid(row=3, column=6, columnspan=2)
        #Close
        self.close = tk.Button(self, text="Exit", width=5, command=lambda: self.destroy())
        self.close.grid(row=4, column=3, columnspan=2)
        
    def submit(self, name):
        if name == "part" and self.has_data(self.part_X, self.part_Y):
            gui_lib.update_json("cords.json", "part", "x", self.part_X.get())
            gui_lib.update_json("cords.json", "part", "y", self.part_Y.get())
            self.submit_part.grid_forget()
        elif name == "scale1" and self.has_data(self.scale1_X, self.scale1_Y):
            gui_lib.update_json("cords.json", "scale1", "x", self.scale1_X.get())
            gui_lib.update_json("cords.json", "scale1", "y", self.scale1_Y.get())
            self.submit_scale1.grid_forget()
        elif name == "scale2" and self.has_data(self.scale2_X, self.scale2_Y):
            gui_lib.update_json("cords.json", "scale2", "x", self.scale2_X.get())
            gui_lib.update_json("cords.json", "scale2", "y", self.scale2_Y.get())
            self.submit_scale2.grid_forget()
        elif name == "plate" and self.has_data(self.plate_X, self.plate_Y):
            gui_lib.update_json("cords.json", "plate", "x", self.plate_X.get())
            gui_lib.update_json("cords.json", "plate", "y", self.plate_Y.get())
            self.submit_plate.grid_forget()

            
    def has_data(self, *args):
        for input in args:
            if not input.get().strip(".").isnumeric():
                return False
        return True

