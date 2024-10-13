import tkinter as tk
from tkinter import ttk

class FooterFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, padding="10", style='Main.TFrame')
        self.frame.grid(row=6, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Copyright 2024").grid(row=0, column=0)