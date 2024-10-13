import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import tkinter as tk

class MyHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"File {event.src_path} has been modified")
            self.app.reload()

class HotReloader:
    def __init__(self, app_module):
        self.root = tk.Tk()
        self.app_module = app_module
        self.app = None
        self.create_app()

    def create_app(self):
        if self.app:
            for widget in self.root.winfo_children():
                widget.destroy()
        app_module = importlib.import_module(self.app_module)
        importlib.reload(app_module)
        self.app = app_module.AplikasiTimbangan(self.root)

    def reload(self):
        self.create_app()

    def run(self):
        event_handler = MyHandler(self)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()

        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app_module = sys.argv[1]
    else:
        app_module = 'cais_combics_3'  # default module name
    
    hot_reloader = HotReloader(app_module)
    hot_reloader.run()