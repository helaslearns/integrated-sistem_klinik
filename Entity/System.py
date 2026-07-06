
from typing import Any

from BST.BST import BST
from Queue.Queue import Queue
from Stack.Stack import Stack
from Heap import Heap
from Entity.Pasien import Pasien

class SystemKlinik:
    def __init__(self):
        self.antrian_daftar = Queue()
        self.database_pasien = BST()
        self.antrian_triase = Heap.MinHeap()
        self.riwayat_pasien = Stack()
        self.counter_rm = 1000

    def tambahPasien(self, nama, keluhan, prioritas):
        self.counter_rm += 1
        pasien = Pasien(self.counter_rm, nama, keluhan, prioritas)
        self.antrian_daftar.enqueue(pasien)
        self.database_pasien.insert(pasien)
        
        print(f"Pasien {pasien.nama} berhasil ditambahkan ke antrian pendaftaran dengan RM-{pasien.no_rm}.")

    def prosesPendaftaran(self):
        if self.antrian_daftar.isEmpty():
            print("\n[INFO] Antrian pendaftaran kosong.")
            return
        pasien = self.antrian_daftar.dequeue()
        if pasien is None:
            print("\n[INFO] Gagal mengambil pasien dari antrian pendaftaran.")
            return
        self.database_pasien.insert(pasien)     
        self.antrian_triase.insert(pasien)        
        aksi = f"Proses pendaftaran RM-{pasien.no_rm} ({pasien.nama})"
        self.riwayat_pasien.push(aksi)           
        print(f"\n[OK] {pasien.nama} (RM-{pasien.no_rm}) telah diproses: "
              f"data tersimpan & masuk antrean triase.")
    
    def panggilPasien(self):
        pasien = self.antrian_triase.delete_root()
        if pasien is None:
            print("\n[INFO] Antrian triase kosong.")
            return
        tindakan = f"Pasien RM-{pasien.no_rm} ({pasien.nama}) dipanggil untuk tindakan."
        self.riwayat_pasien.push(tindakan)
        print(f"\n[OK] {pasien.nama} (RM-{pasien.no_rm}) telah dipanggil untuk tindakan.")
    
    def cariPasien(self, no_rm):
        pasien = self.database_pasien.search(no_rm)
        if pasien:
            print(f"\n[DITEMUKAN] RM-{pasien.no_rm} | {pasien.nama} | "
                  f"Keluhan: {pasien.keluhan} | Prioritas: {pasien.prioritas} | "
                  f"Terdaftar: {pasien.waktu_daftar}")
        else:
            print(f"\n[INFO] Pasien dengan RM-{no_rm} tidak ditemukan.")

    def hapusPasien(self, no_rm):
        berhasil = self.database_pasien.delete(no_rm)
        if berhasil:
            aksi = f"Hapus data pasien RM-{no_rm}"
            self.riwayat_pasien.push(aksi)
            print(f"\n[OK] Data pasien RM-{no_rm} berhasil dihapus dari database.")
        else:
            print(f"\n[INFO] Pasien dengan RM-{no_rm} tidak ditemukan dalam database.") 

    def undoAksiTerakhir(self):
        aksi = self.riwayat_pasien.pop()
        if aksi:
            print(f"\n[UNDO] Aksi terakhir dibatalkan (dicatat): {aksi}")
            print("       Catatan: pembatalan efek data harus disesuaikan manual")
            print("       oleh kelompok sesuai kebutuhan studi kasus (opsional dikembangkan).")
        else:
            print("\n[INFO] Tidak ada tindakan untuk di-undo.")
    
    def displayDaftar(self):
        print("\n=== ANTREAN PENDAFTARAN (QUEUE) ===")
        self.antrian_daftar.display()
 
    def displayRiwayat(self):
        print("\n=== RIWAYAT TINDAKAN (STACK) ===")
        self.riwayat_pasien.display()
 
    def displayDatabasePasien(self):
        print("\n=== DATABASE PASIEN TERURUT NO. RM (BST - INORDER) ===")
        self.database_pasien.displayInorder()
        print("\n--- Visualisasi Bentuk Tree (BST) ---")
        self.database_pasien.displayTree()
 
    def displayTriase(self):
        print("\n=== ANTREAN TRIASE / PRIORITAS (HEAP - ARRAY) ===")
        self.antrian_triase.display()
        print("\n--- Visualisasi Bentuk Tree/Piramida (HEAP) ---")
        self.antrian_triase.displayHeap()
 
    def info_tree(self):
        print("\n=== INFORMASI BINARY SEARCH TREE ===")
        print(f"  Tinggi tree  : {self.database_pasien.height()}")
        print(f"  Jumlah node  : {self.database_pasien.nodeCount()}")
    