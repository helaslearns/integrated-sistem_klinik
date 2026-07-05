import typing
import BST.BST as BST
import Queue.Queue as Queue
import Heap.Heap as Heap
import Stack.Stack as Stack


# ==========================================
# SISTEM UTAMA (Integrasi Bisnis)
# ==========================================

class Pasien:
    def __init__(self, id_pasien, nama, tingkat_keparahan=0):
        self.id_pasien = id_pasien
        self.nama = nama
        self.tingkat_keparahan = tingkat_keparahan # 1 (Ringan) - 3 (Gawat Darurat)
        self.status = "Menunggu"

    def __str__(self):
        return f"[ID: {self.id_pasien}] {self.nama} (Keparahan: {self.tingkat_keparahan})"

class SistemIGD:
    def __init__(self):
        self.queue_registrasi = Queue.Queue()
        self.bst_rekam_medis = BST.BST()
        self.heap_prioritas = Heap.MaxHeap()
        self.stack_riwayat = Stack.Stack()
        self.auto_id = 100

    def pasien_datang(self, nama):
        # 1. Pasien datang masuk Queue
        pasien_baru = Pasien(self.auto_id, nama)
        self.queue_registrasi.enqueue(pasien_baru)
        print(f"[*] Pasien {nama} masuk antrean registrasi.")
        self.auto_id += 1

    def proses_triage(self, tingkat_keparahan):
        # 2. Perawat memproses antrean (Queue -> BST & Heap)
        pasien = self.queue_registrasi.dequeue()
        if not pasien:
            print("[!] Tidak ada pasien di antrean registrasi.")
            return

        pasien.tingkat_keparahan = tingkat_keparahan

        # Simpan ke BST sebagai database
        self.bst_rekam_medis.insert(pasien)
        # Masukkan ke IGD berdasarkan prioritas (Heap)
        self.heap_prioritas.insert(pasien)

        print(f"[*] Triage Selesai: {pasien.nama} dimasukkan ke IGD dengan prioritas {tingkat_keparahan}.")

    def dokter_tangani_pasien(self):
        # 3. Dokter memanggil pasien prioritas tertinggi (Heap -> Stack)
        pasien = self.heap_prioritas.delete_root()
        if not pasien:
            print("[!] Tidak ada pasien yang menunggu di IGD.")
            return

        pasien.status = "Ditangani"
        self.stack_riwayat.push(pasien)
        print(f"[+] Dokter sedang menangani: {pasien.nama} (Prioritas: {pasien.tingkat_keparahan})")

    def batalkan_penanganan(self):
        # 4. Undo jika dokter salah panggil (Stack -> Heap)
        pasien = self.stack_riwayat.pop()
        if not pasien:
            print("[!] Tidak ada riwayat penanganan untuk dibatalkan.")
            return

        pasien.status = "Menunggu"
        self.heap_prioritas.insert(pasien)
        print(f"[-] Batal penanganan: {pasien.nama} dikembalikan ke antrean IGD.")

# ==========================================
# MENU CLI
# ==========================================
if __name__ == "__main__":
    sistem = SistemIGD()

    while True:
        print("\n=== SISTEM MANAJEMEN IGD RUMAH SAKIT ===")
        print("1. Pasien Baru Datang (Masuk Queue)")
        print("2. Proses Triage Pasien (Queue -> Heap & BST)")
        print("3. Dokter Tangani Pasien (Ambil dari Heap -> Stack)")
        print("4. Batalkan Penanganan Terakhir (Undo dari Stack)")
        print("5. Lihat Semua Antrean (Display Queue & Heap)")
        print("6. Lihat Database Rekam Medis (BST Inorder)")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            nama = input("Nama Pasien: ")
            sistem.pasien_datang(nama)
        elif pilihan == '2':
            if sistem.queue_registrasi.peek():
                print(f"Memproses: {sistem.queue_registrasi.peek().nama}") # type: ignore
                try:
                    keparahan = int(input("Masukkan tingkat keparahan (1-Ringan, 2-Sedang, 3-Gawat): "))
                    sistem.proses_triage(keparahan)
                except ValueError:
                    print("Input harus berupa angka!")
            else:
                print("Antrean registrasi kosong.")
        elif pilihan == '3':
            sistem.dokter_tangani_pasien()
        elif pilihan == '4':
            sistem.batalkan_penanganan()
        elif pilihan == '5':
            print("\n--- STATUS SAAT INI ---")
            sistem.queue_registrasi.display()
            sistem.heap_prioritas.display()
            sistem.stack_riwayat.display()
        elif pilihan == '6':
            print("\n--- DATABASE REKAM MEDIS (BST) ---")
            sistem.bst_rekam_medis.inorder_traversal(sistem.bst_rekam_medis.root)
            print(f"Total Pasien Terdaftar: {sistem.bst_rekam_medis.count_nodes(sistem.bst_rekam_medis.root)}")
        elif pilihan == '0':
            print("Keluar dari sistem. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")