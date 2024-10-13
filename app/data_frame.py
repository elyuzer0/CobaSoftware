import tkinter as tk
from tkinter import ttk

class DataFrame:
    def __init__(self, master):
        self.frame = ttk.LabelFrame(master, text="Data Timbangan", padding="10")
        self.frame.grid(row=4, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.create_widgets()

    def create_widgets(self):
        self.weight_value = ttk.Label(self.frame, text="0.00 kg", font=("Arial", 48))
        self.weight_value.grid(row=0, column=0)