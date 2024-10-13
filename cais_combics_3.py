import tkinter as tk
from tkinter import ttk
import time
import csv
from datetime import datetime
import random
import threading

class DummySerial:
    def __init__(self, port):
        self.port = port
        self.is_open = True

    def write(self, data):
        pass

    def readline(self):
        return f"{random.uniform(0.1, 10.0):.2f} kg".encode('ascii')

    def close(self):
        self.is_open = False
        print(f"Koneksi ke {self.port} ditutup")

class AplikasiTimbangan:
    def __init__(self, master):
        self.master = master
        master.title("Aplikasi Timbangan CAIS Combics 3")
        master.geometry("800x600")
        master.configure(bg='#387478')
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.create_styles()

        self.main_frame = ttk.Frame(master, padding="10", style='Main.TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.create_header_frame()
        self.create_search_frame()
        self.create_connection_frame()
        self.create_data_frame()
        self.create_control_frame()
        self.create_footer_frame()

        self.ser = None
        self.is_reading = False

    def create_styles(self):
        style = ttk.Style()
        style.configure('Main.TFrame', background='#387478')
        style.configure('TLabel', background='#387478', foreground='white')
        style.configure('TButton', background='#387478')
        style.configure('TLabelframe', background='#387478')
        style.configure('TLabelframe.Label', background='#387478', foreground='white')

    def create_header_frame(self):
        header_frame = ttk.Frame(self.main_frame, padding="10", style='Main.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        header_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(header_frame, text="Aplikasi Timbangan CAIS Combics 3", font=("Arial", 18)).grid(row=0, column=0)

    def create_search_frame(self):
        search_frame = ttk.Frame(self.main_frame, padding="10", style='Main.TFrame')
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        search_frame.grid_columnconfigure(1, weight=1)

        # Menambahkan logo di sebelah kiri
        logo_label = ttk.Label(search_frame, text="Logo", font=("Arial", 14))  # Ganti dengan gambar logo jika ada
        logo_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        ttk.Label(search_frame).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.gate_entry = tk.Entry(search_frame, font=("Arial", 14))  # Mengatur ukuran font
        self.gate_entry.insert(0, "Gate In / Gate Out")
        self.gate_entry.bind("<FocusIn>", self.on_entry_click)
        self.gate_entry.bind("<FocusOut>", self.on_focusout)
        self.gate_entry.config(fg='grey')
        self.gate_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(search_frame, text="STID", command=self.search_stid).grid(row=0, column=2, sticky=tk.E)

        # Menambahkan tombol menu di sebelah kanan
        menu_frame = ttk.Frame(search_frame)
        menu_frame.grid(row=0, column=3, sticky=tk.E, padx=(5, 0))

        ttk.Button(menu_frame, text="No Print", command=self.no_print_command).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_frame, text="Reprint", command=self.reprint_command).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_frame, text="Home", command=self.home_command).pack(side=tk.LEFT, padx=2)

        # Menambahkan layar CCTV dan field teks di bawah search
        cctv_frame = ttk.Frame(self.main_frame, padding="10", style='Main.TFrame')
        cctv_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

        # Layar CCTV
        ttk.Label(cctv_frame, text="Layar CCTV", font=("Arial", 14)).grid(row=0, column=0, columnspan=2)
        # Ganti dengan widget video atau gambar sesuai kebutuhan
        cctv_label = ttk.Label(cctv_frame, text="[CCTV Video Here]", relief=tk.SUNKEN, width=40, anchor=tk.CENTER)
        cctv_label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Field teks untuk Kapal, Tambatan, dan Nomor Polisi
        ttk.Label(cctv_frame, text="Kapal:").grid(row=2, column=0, sticky=tk.W)
        self.kapal_entry = tk.Entry(cctv_frame, font=("Arial", 14))
        self.kapal_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(cctv_frame, text="Tambatan:").grid(row=3, column=0, sticky=tk.W)
        self.tambatan_entry = tk.Entry(cctv_frame, font=("Arial", 14))
        self.tambatan_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        ttk.Label(cctv_frame, text="Nomor Polisi:").grid(row=4, column=0, sticky=tk.W)
        self.nomor_polisi_entry = tk.Entry(cctv_frame, font=("Arial", 14))
        self.nomor_polisi_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

        ttk.Button(cctv_frame, text="STID", command=self.search_stid).grid(row=5, column=1, sticky=tk.E)

        # Field Berat In dengan button Lock
        ttk.Label(cctv_frame, text="Berat In:").grid(row=6, column=0, sticky=tk.W)
        self.berat_in_entry = tk.Entry(cctv_frame, font=("Arial", 14))
        self.berat_in_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))

        ttk.Button(cctv_frame, text="Lock", command=self.lock_weight).grid(row=6, column=2, sticky=tk.E)

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
            # Implementasi logika pencarian di sini
        else:
            print("Silakan Gate In / Gate Out terlebih dahulu")

    def create_connection_frame(self):
        connection_frame = ttk.LabelFrame(self.main_frame, text="Koneksi", padding="10")
        connection_frame.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        connection_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(connection_frame, text="Port:").grid(row=0, column=0, sticky=tk.W)
        self.port_combobox = ttk.Combobox(connection_frame, values=['COM1', 'COM2', 'COM3', 'COM4'])
        self.port_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.port_combobox.set('COM3')

        self.connect_button = ttk.Button(connection_frame, text="Hubungkan", command=self.hubungkan)
        self.connect_button.grid(row=0, column=2)

        self.status_label = ttk.Label(connection_frame, text="Status: Tidak terhubung")
        self.status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W)

    def create_data_frame(self):
        data_frame = ttk.LabelFrame(self.main_frame, text="Data Timbangan", padding="10")
        data_frame.grid(row=4, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_rowconfigure(0, weight=1)

        self.weight_value = ttk.Label(data_frame, text="0.00 kg", font=("Arial", 48))
        self.weight_value.grid(row=0, column=0)

    def create_control_frame(self):
        control_frame = ttk.Frame(self.main_frame, padding="10", style='Main.TFrame')
        control_frame.grid(row=5, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        control_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ttk.Button(control_frame, text="Mulai Pembacaan", command=self.mulai_pembacaan, state=tk.DISABLED)
        self.start_button.grid(row=0, column=0, padx=(0, 5), sticky=tk.E)

        self.stop_button = ttk.Button(control_frame, text="Hentikan", command=self.hentikan_pembacaan, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=(5, 0), sticky=tk.W)

    def create_footer_frame(self):
        footer_frame = ttk.Frame(self.main_frame, padding="10", style='Main.TFrame')
        footer_frame.grid(row=6, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        footer_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(footer_frame, text="Copyright 2024").grid(row=0, column=0)

    def hubungkan(self):
        port = self.port_combobox.get()
        self.ser = DummySerial(port)
        self.status_label.config(text=f"Status: Terhubung ke {port}")
        self.start_button.config(state=tk.NORMAL)
        self.connect_button.config(state=tk.DISABLED)

    def mulai_pembacaan(self):
        self.is_reading = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.baca_data_terus_menerus, daemon=True).start()

    def hentikan_pembacaan(self):
        self.is_reading = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def baca_data_terus_menerus(self):
        while self.is_reading:
            data = self.ser.readline().decode('ascii').strip()
            self.master.after(0, self.update_weight_display, data)
            self.simpan_ke_csv(data)
            time.sleep(1)

    def update_weight_display(self, data):
        self.weight_value.config(text=data)

    def simpan_ke_csv(self, data):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('data_berat.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([waktu, data])

    # Metode untuk tombol menu
    def no_print_command(self):
        print("No Print button clicked")

    def reprint_command(self):
        print("Reprint button clicked")

    def home_command(self):
        print("Home button clicked")

    def lock_weight(self):
        berat_in_value = self.berat_in_entry.get()
        print(f"Berat In dikunci: {berat_in_value}")

def main():
    root = tk.Tk()
    root.configure(bg='#387478')
    return AplikasiTimbangan(root)

if __name__ == "__main__":
    app = main()
    app.master.mainloop()