import tkinter as tk
import json

def base_entry(root, name, _row, _column, sticky=None):
    stringvar = tk.StringVar()
    label = tk.Label(root, text=name)
    label.grid(row=_row, column=_column, sticky="e")
    entry = tk.Entry(root, textvariable=stringvar, width=10)
    entry.grid(row=_row, column=_column+1, sticky="w")
    return stringvar
    
def get_json(filename):
    with open(filename) as f:
        return dict(json.load(f))

def update_json(filename, key1, key2, new_data):
    data = get_json(filename)
    data[key1][key2] = new_data
    dump_json(filename, data)
    
def dump_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
def append_json(new_data, filename='parts.json'):
    data = get_json(filename)
    data.update(new_data)
    dump_json(filename, data)
    