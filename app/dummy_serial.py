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