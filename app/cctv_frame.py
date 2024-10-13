import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class CCTVFrame:
    def __init__(self, master):
        self.frame = ttk.Frame(master, padding="10", style='Main.TFrame')
        self.frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Layar CCTV", font=("Arial", 14)).grid(row=0, column=0, columnspan=2)
        self.cctv_label = ttk.Label(self.frame, relief=tk.SUNKEN, width=40, anchor=tk.CENTER)
        self.cctv_label.grid(row=1, column=0, columnspan=2, pady=(2, 5))

    def update_cctv(self, frame):
        # Mengubah BGR ke RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Mengubah ukuran frame agar tidak lebih dari 300 piksel
        frame = cv2.resize(frame, (300, 200))  # Atur ukuran sesuai kebutuhan
        # Mengubah ke Image
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.cctv_label.imgtk = imgtk
        self.cctv_label.configure(image=imgtk)