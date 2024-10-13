import tkinter as tk
from tkinter import ttk

class HeaderFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, padding="10", style='Main.TFrame')
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Aplikasi Timbangan CAIS Combics 3", font=("Arial", 18)).grid(row=0, column=0)