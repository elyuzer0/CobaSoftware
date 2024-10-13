import tkinter as tk
import tkinter.ttk as ttk
from app.header_frame import HeaderFrame
from app.search_frame import SearchFrame
from app.cctv_frame import CCTVFrame
from app.connection_frame import ConnectionFrame
from app.data_frame import DataFrame
from app.control_frame import ControlFrame
from app.footer_frame import FooterFrame
from app.dummy_serial import DummySerial
import cv2

class AplikasiTimbangan:
    def __init__(self, master):
        self.master = master
        self.vid = None
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

        # Inisialisasi semua frame
        self.header_frame = HeaderFrame(self.main_frame)
        self.search_frame = SearchFrame(self.main_frame)
        self.connection_frame = ConnectionFrame(self.main_frame)
        self.data_frame = DataFrame(self.main_frame)
        self.control_frame = ControlFrame(self.main_frame)
        self.footer_frame = FooterFrame(self.main_frame)
        self.cctv_frame = CCTVFrame(self.main_frame)

             # Menambahkan konfigurasi bobot untuk setiap frame
        self.main_frame.grid_rowconfigure(0, weight=0)  # Header
        self.main_frame.grid_rowconfigure(1, weight=1)  # Search
        self.main_frame.grid_rowconfigure(2, weight=1)  # Connection
        self.main_frame.grid_rowconfigure(3, weight=1)  # Data
        self.main_frame.grid_rowconfigure(4, weight=1)  # Control
        self.main_frame.grid_rowconfigure(5, weight=0)  # Footer
        self.main_frame.grid_rowconfigure(6, weight=1)  # CCTV

        # Inisialisasi video
        self.video_source = 0  # Ganti dengan sumber video yang sesuai jika perlu
        self.vid = cv2.VideoCapture(self.video_source)

        self.update_cctv()

    def create_styles(self):
        style = ttk.Style()
        style.configure('Main.TFrame', background='#387478')
        style.configure('TLabel', background='#387478', foreground='white')
        style.configure('TButton', background='#387478')
        style.configure('TLabelframe', background='#387478')
        style.configure('TLabelframe.Label', background='#387478', foreground='white')

    def update_cctv(self):
        ret, frame = self.vid.read()
        if ret:
            self.cctv_frame.update_cctv(frame)
        self.master.after(10, self.update_cctv)

    def __del__(self):
        if self.vid is not None and self.vid.isOpened():  # Memastikan self.vid tidak None
            self.vid.release()

def main():
    root = tk.Tk()
    root.configure(bg='#387478')
    return AplikasiTimbangan(root)

if __name__ == "__main__":
    app = main()
    app.master.mainloop()