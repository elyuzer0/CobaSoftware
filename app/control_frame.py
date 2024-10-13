import tkinter as tk
from tkinter import ttk

class ControlFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, padding="10", style='Main.TFrame')
        self.frame.grid(row=5, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.create_widgets()

    def create_widgets(self):
        self.start_button = ttk.Button(self.frame, text="Mulai Pembacaan", command=self.mulai_pembacaan, state=tk.DISABLED)
        self.start_button.grid(row=0, column=0, padx=(0, 5), sticky=tk.E)

        self.stop_button = ttk.Button(self.frame, text="Hentikan", command=self.hentikan_pembacaan, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=(5, 0), sticky=tk.W)

    def mulai_pembacaan(self):
        pass  # Implementasi logika pembacaan

    def hentikan_pembacaan(self):
        pass  # Implementasi logika penghentian