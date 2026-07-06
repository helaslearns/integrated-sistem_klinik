from Entity.System import SystemKlinik

def input_prioritas():
    print("  Pilih tingkat kegawatan:")
    print("  1. Gawat Darurat")
    print("  2. Sedang")
    print("  3. Ringan")

    while True:
            try:
                p = int(input("  Pilihan (1-3): "))
                if p in (1, 2, 3):
                    return p
                print("  Input harus 1, 2, atau 3.")
            except ValueError:
                print("  Input tidak valid, masukkan angka.")

def main():
    sistem = SystemKlinik()
 
    menu = """
=====================================================
   SISTEM ANTREAN & TRIASE KLINIK
=====================================================
 1.  Daftar pasien baru               (Queue)
 2.  Proses pendaftaran terdepan      (Queue -> BST -> Heap)
 3.  Panggil pasien berikutnya        (Heap)
 4.  Cari data pasien                 (BST)
 5.  Hapus data pasien                (BST)
 6.  Tampilkan antrean pendaftaran    (Queue)
 7.  Tampilkan riwayat tindakan       (Stack)
 8.  Tampilkan database pasien        (BST - Inorder)
 9.  Tampilkan antrean triase         (Heap)
 10. Undo tindakan terakhir           (Stack)
 11. Info tree (tinggi & jumlah node) (BST)
 0.  Keluar
=====================================================
"""
 
    while True:
        print(menu)
        pilihan = input("Pilih menu: ").strip()
 
        if pilihan == "1":
            nama = input("Nama pasien: ").strip()
            keluhan = input("Keluhan: ").strip()
            prioritas = input_prioritas()
            sistem.tambahPasien(nama, keluhan, prioritas)
 
        elif pilihan == "2":
            sistem.prosesPendaftaran()
 
        elif pilihan == "3":
            sistem.panggilPasien()
 
        elif pilihan == "4":
            try:
                no_rm = int(input("Masukkan No. RM: "))
                sistem.cariPasien(no_rm)
            except ValueError:
                print("\n[ERROR] No. RM harus berupa angka.")
 
        elif pilihan == "5":
            try:
                no_rm = int(input("Masukkan No. RM yang akan dihapus: "))
                sistem.hapusPasien(no_rm)
            except ValueError:
                print("\n[ERROR] No. RM harus berupa angka.")
 
        elif pilihan == "6":
            sistem.displayDaftar()
 
        elif pilihan == "7":
            sistem.displayRiwayat()
 
        elif pilihan == "8":
            sistem.displayDatabasePasien()
 
        elif pilihan == "9":
            sistem.displayTriase()
 
        elif pilihan == "10":
            sistem.undoAksiTerakhir()
 
        elif pilihan == "11":
            sistem.info_tree()
 
        elif pilihan == "0":
            print("\nProgram selesai. Terima kasih!")
            break
 
        else:
            print("\n[ERROR] Pilihan tidak valid.")

def mainAuto():
    sistem = SystemKlinik()
 
    print(">>> DEMO: Pasien datang dan mendaftar (QUEUE)")
    sistem.tambahPasien("Andi", "Demam tinggi", 2)
    sistem.tambahPasien("Budi", "Kecelakaan lalu lintas", 1)
    sistem.tambahPasien("Citra", "Kontrol rutin", 3)
    sistem.displayDaftar()
 
    print("\n>>> DEMO: Proses semua pendaftaran (QUEUE -> BST -> HEAP)")
    for _ in range(3):
        sistem.prosesPendaftaran()
    sistem.displayDatabasePasien()
    sistem.displayTriase()
 
    print("\n>>> DEMO: Panggil pasien berdasarkan prioritas (HEAP)")
    sistem.panggilPasien()  # harusnya Budi (prioritas 1) duluan
    sistem.panggilPasien()  # lalu Andi (prioritas 2)
 
    print("\n>>> DEMO: Cari & hapus data pasien (BST)")
    sistem.cariPasien(1003)  # Citra
    sistem.hapusPasien(1001)  # Andi
 
    print("\n>>> DEMO: Info tree (BST)")
    sistem.info_tree()
 
    print("\n>>> DEMO: Riwayat tindakan (STACK)")
    sistem.displayRiwayat()
 
    print("\n>>> DEMO: Undo tindakan terakhir (STACK)")
    sistem.undoAksiTerakhir()

if __name__ == "__main__":
    opsi = input("Pilih mode: 1. Manual | 2. Demo otomatis : ").strip()
    match opsi:
        case "1":
            main()
        case "2":
            mainAuto()
        case _:
            print("Pilihan tidak valid. Keluar dari program.")
            exit(1)
        