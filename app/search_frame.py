import tkinter as tk
from tkinter import ttk

class SearchFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, padding="10", style='Main.TFrame')
        self.frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.create_widgets()

    def create_widgets(self):
        logo_label = ttk.Label(self.frame, text="Logo", font=("Arial", 14))  # Ganti dengan gambar logo jika ada
        logo_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        self.gate_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.gate_entry.insert(0, "Gate In / Gate Out")
        self.gate_entry.bind("<FocusIn>", self.on_entry_click)
        self.gate_entry.bind("<FocusOut>", self.on_focusout)
        self.gate_entry.config(fg='grey')
        self.gate_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))

        ttk.Button(self.frame, text="STID", command=self.search_stid).grid(row=0, column=2, sticky=tk.E)

        menu_frame = ttk.Frame(self.frame)
        menu_frame.grid(row=0, column=3, sticky=tk.E, padx=(5, 0))

        ttk.Button(menu_frame, text="No Print", command=self.no_print_command).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_frame, text="Reprint", command=self.reprint_command).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_frame, text="Home", command=self.home_command).pack(side=tk.LEFT, padx=2)

    def on_entry_click(self, event):
        if self.gate_entry.get() == "Gate In / Gate Out":
            self.gate_entry.delete(0, "end")
            self.gate_entry.insert(0, '')
            self.gate_entry.config(fg='black')

    def on_focusout(self, event):
        if self.gate_entry.get() == '':
            self.gate_entry.insert(0, "Gate In / Gate Out")
            self.gate_entry.config(fg='grey')

    def search_stid(self):
        gate_value = self.gate_entry.get()
        if gate_value != "Gate In / Gate Out":
            print(f"Mencari STID untuk Gate: {gate_value}")
        else:
            print("Silakan Gate In / Gate Out terlebih dahulu")

    def no_print_command(self):
        print("No Print button clicked")

    def reprint_command(self):
        print("Reprint button clicked")

    def home_command(self):
        print("Home button clicked")