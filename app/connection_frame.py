import tkinter as tk
from tkinter import ttk
from app.dummy_serial import DummySerial

class ConnectionFrame:
    def __init__(self, master):
        self.frame = ttk.LabelFrame(master, text="Koneksi", padding="10")
        self.frame.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Port:").grid(row=0, column=0, sticky=tk.W)
        self.port_combobox = ttk.Combobox(self.frame, values=['COM1', 'COM2', 'COM3', 'COM4'])
        self.port_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.port_combobox.set('COM3')

        self.connect_button = ttk.Button(self.frame, text="Hubungkan", command=self.hubungkan)
        self.connect_button.grid(row=0, column=2)

        self.status_label = ttk.Label(self.frame, text="Status: Tidak terhubung")
        self.status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W)

    def hubungkan(self):
        port = self.port_combobox.get()
        self.ser = DummySerial(port)
        self.status_label.config(text=f"Status: Terhubung ke {port}")