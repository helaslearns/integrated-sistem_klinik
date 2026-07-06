
import time

class Pasien:
    def __init__(self, no_rm, nama, keluhan, prioritas):
        self.no_rm = no_rm
        self.nama = nama
        self.keluhan = keluhan
        self.prioritas = prioritas  # 1 = darurat, 2 = sedang, 3 = ringan
        self.waktu_daftar = time.strftime("%H:%M:%S")
 
    def __repr__(self):
        return f"Pasien(RM-{self.no_rm}, {self.nama})"