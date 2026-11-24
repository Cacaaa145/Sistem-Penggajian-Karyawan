"""
Sistem Penggajian Karyawan (Payroll) Sederhana
Final Project - Pemrograman Python

Fitur:
1. Tambah karyawan
2. Lihat daftar karyawan
3. Ubah data karyawan
4. Hapus karyawan
5. Input absensi & lembur bulanan
6. Hitung & cetak slip gaji
7. Laporan total penggajian
0. Keluar
"""

import random

# ====================== DATA ======================
# Dictionary utama: kunci = ID karyawan, nilai = dictionary data karyawan
karyawan = {}

# Daftar jabatan yang valid (list) beserta tunjangan jabatannya (dictionary)
DAFTAR_JABATAN = ["staff", "supervisor", "manager"]
TUNJANGAN_JABATAN = {"staff": 500000, "supervisor": 1000000, "manager": 2000000}

# Konstanta aturan gaji (mudah diubah saat live modification)
UPAH_LEMBUR_PER_JAM = 25000
POTONGAN_PER_HARI_ABSEN = 100000
PERSEN_BPJS = 0.03  # 3% dari gaji pokok


# ====================== FUNGSI BANTU ======================
def format_rupiah(angka):
    """Ubah angka menjadi format Rp 1.000.000"""
    return "Rp {:,.0f}".format(angka).replace(",", ".")


def input_angka(pesan, minimum=0):
    """Minta input angka bulat, ulangi sampai valid."""
    while True:
        teks = input(pesan).strip()
        if teks.isdigit() and int(teks) >= minimum:
            return int(teks)
        print("  [!] Masukkan angka bulat >= {}.".format(minimum))


def input_jabatan():
    """Minta input jabatan sampai valid."""
    while True:
        jabatan = input("Jabatan ({}): ".format("/".join([j.title() for j in DAFTAR_JABATAN]))).strip().lower()
        if jabatan in DAFTAR_JABATAN:
            return jabatan
        print("  [!] Jabatan tidak valid.")


def buat_id():
    """ID otomatis: angka acak 5 digit yang belum dipakai di keys dictionary."""
    while True:
        id_baru = random.randint(10000, 99999)
        if id_baru not in karyawan:
            return id_baru


def cari_id_dari_nama(nama):
    """Cari key (ID otomatis) berdasarkan nama. Kembalikan None jika tidak ada."""
    for id_karyawan, data in karyawan.items():
        if data["nama"].lower() == nama.lower():
            return id_karyawan
    return None


def input_nama():
    """Minta nama karyawan dari user, kembalikan key-nya (atau None)."""
    nama = input("Nama karyawan: ").strip()
    return cari_id_dari_nama(nama)


def cari_karyawan(id_karyawan):
    """Kembalikan data karyawan, atau None jika tidak ada."""
    return karyawan.get(id_karyawan)


# ====================== LOGIKA GAJI ======================
def hitung_pajak(gaji_bruto):
    """Pajak sederhana bertingkat berdasarkan gaji bruto."""
    if gaji_bruto <= 5000000:
        persen = 0
    elif gaji_bruto <= 10000000:
        persen = 0.05
    elif gaji_bruto <= 20000000:
        persen = 0.10
    else:
        persen = 0.15
    return gaji_bruto * persen


def hitung_gaji(data):
    """Hitung semua komponen gaji, kembalikan dalam bentuk dictionary."""
    tunjangan = TUNJANGAN_JABATAN[data["jabatan"]]
    upah_lembur = data["jam_lembur"] * UPAH_LEMBUR_PER_JAM
    gaji_bruto = data["gaji_pokok"] + tunjangan + upah_lembur

    potongan_absen = data["hari_absen"] * POTONGAN_PER_HARI_ABSEN
    potongan_bpjs = data["gaji_pokok"] * PERSEN_BPJS
    pajak = hitung_pajak(gaji_bruto)
    total_potongan = potongan_absen + potongan_bpjs + pajak

    gaji_bersih = gaji_bruto - total_potongan
    if gaji_bersih < 0:  # gaji bersih tidak boleh negatif
        gaji_bersih = 0

    return {
        "gaji_pokok": data["gaji_pokok"],
        "tunjangan": tunjangan,
        "upah_lembur": upah_lembur,
        "gaji_bruto": gaji_bruto,
        "potongan_absen": potongan_absen,
        "potongan_bpjs": potongan_bpjs,
        "pajak": pajak,
        "total_potongan": total_potongan,
        "gaji_bersih": gaji_bersih,
    }


# ====================== FITUR MENU ======================
def tambah_karyawan():
    print("\n--- Tambah Karyawan ---")
    nama = input("Nama: ").strip().title()
    if nama == "":
        print("[!] Nama tidak boleh kosong.")
        return
    if cari_id_dari_nama(nama) is not None:
        print("[!] Nama sudah terdaftar.")
        return
    id_karyawan = buat_id()  # ID otomatis, dipakai sebagai key dictionary
    jabatan = input_jabatan()
    gaji_pokok = input_angka("Gaji pokok (Rp): ", minimum=1)

    karyawan[id_karyawan] = {
        "nama": nama,
        "jabatan": jabatan,
        "gaji_pokok": gaji_pokok,
        "hari_absen": 0,
        "jam_lembur": 0,
    }
    print("[OK] Karyawan {} berhasil ditambahkan dengan ID {}.".format(nama, id_karyawan))


def lihat_karyawan():
    print("\n--- Daftar Karyawan ---")
    if len(karyawan) == 0:
        print("Belum ada data karyawan.")
        return
    print("{:<8}{:<20}{:<12}{:>16}".format("ID", "Nama", "Jabatan", "Gaji Pokok"))
    print("-" * 56)
    for id_karyawan, data in karyawan.items():
        print("{:<8}{:<20}{:<12}{:>16}".format(
            id_karyawan, data["nama"], data["jabatan"].title(), format_rupiah(data["gaji_pokok"])))


def ubah_karyawan():
    print("\n--- Ubah Data Karyawan ---")
    id_karyawan = input_nama()
    data = cari_karyawan(id_karyawan)
    if data is None:
        print("[!] Karyawan tidak ditemukan.")
        return

    print("Mengubah:", data["nama"])
    print("1. Jabatan\n2. Gaji pokok")
    pilihan = input("Pilih data yang diubah: ").strip()
    if pilihan == "1":
        data["jabatan"] = input_jabatan()
        print("[OK] Jabatan diperbarui.")
    elif pilihan == "2":
        data["gaji_pokok"] = input_angka("Gaji pokok baru (Rp): ", minimum=1)
        print("[OK] Gaji pokok diperbarui.")
    else:
        print("[!] Pilihan tidak valid.")


def hapus_karyawan():
    print("\n--- Hapus Karyawan ---")
    id_karyawan = input_nama()
    if id_karyawan not in karyawan:
        print("[!] Karyawan tidak ditemukan.")
        return
    konfirmasi = input("Yakin hapus {}? (y/n): ".format(karyawan[id_karyawan]["nama"])).lower()
    if konfirmasi == "y":
        del karyawan[id_karyawan]
        print("[OK] Data dihapus.")
    else:
        print("Dibatalkan.")


def input_absensi_lembur():
    print("\n--- Input Absensi & Lembur Bulanan ---")
    id_karyawan = input_nama()
    data = cari_karyawan(id_karyawan)
    if data is None:
        print("[!] Karyawan tidak ditemukan.")
        return

    data["hari_absen"] = input_angka("Jumlah hari absen (0-31): ")
    while data["hari_absen"] > 31:
        print("  [!] Maksimal 31 hari.")
        data["hari_absen"] = input_angka("Jumlah hari absen (0-31): ")
    data["jam_lembur"] = input_angka("Total jam lembur: ")
    print("[OK] Data absensi & lembur disimpan.")


def cetak_slip():
    print("\n--- Slip Gaji ---")
    id_karyawan = input_nama()
    data = cari_karyawan(id_karyawan)
    if data is None:
        print("[!] Karyawan tidak ditemukan.")
        return

    gaji = hitung_gaji(data)
    print("\n" + "=" * 40)
    print("           SLIP GAJI KARYAWAN")
    print("=" * 40)
    print("ID      :", id_karyawan)
    print("Nama    :", data["nama"])
    print("Jabatan :", data["jabatan"].title())
    print("Absen   : {} hari | Lembur: {} jam".format(data["hari_absen"], data["jam_lembur"]))
    print("-" * 40)
    print("PENDAPATAN")
    print("  Gaji pokok      :", format_rupiah(gaji["gaji_pokok"]))
    print("  Tunjangan       :", format_rupiah(gaji["tunjangan"]))
    print("  Upah lembur     :", format_rupiah(gaji["upah_lembur"]))
    print("  Gaji bruto      :", format_rupiah(gaji["gaji_bruto"]))
    print("POTONGAN")
    print("  Absensi         :", format_rupiah(gaji["potongan_absen"]))
    print("  BPJS            :", format_rupiah(gaji["potongan_bpjs"]))
    print("  Pajak           :", format_rupiah(gaji["pajak"]))
    print("  Total potongan  :", format_rupiah(gaji["total_potongan"]))
    print("-" * 40)
    print("GAJI BERSIH       :", format_rupiah(gaji["gaji_bersih"]))
    print("=" * 40)


def laporan_penggajian():
    print("\n--- Laporan Penggajian ---")
    if len(karyawan) == 0:
        print("Belum ada data karyawan.")
        return

    total_bersih = 0
    print("{:<8}{:<20}{:>18}".format("ID", "Nama", "Gaji Bersih"))
    print("-" * 46)
    for id_karyawan, data in karyawan.items():
        gaji = hitung_gaji(data)
        total_bersih += gaji["gaji_bersih"]
        print("{:<8}{:<20}{:>18}".format(id_karyawan, data["nama"], format_rupiah(gaji["gaji_bersih"])))
    print("-" * 46)
    print("Jumlah karyawan :", len(karyawan))
    print("Total pengeluaran gaji :", format_rupiah(total_bersih))


# ====================== MENU UTAMA ======================
def tampilkan_menu():
    print("\n" + "=" * 36)
    print("   SISTEM PENGGAJIAN KARYAWAN")
    print("=" * 36)
    print("1. Tambah karyawan")
    print("2. Lihat daftar karyawan")
    print("3. Ubah data karyawan")
    print("4. Hapus karyawan")
    print("5. Input absensi & lembur")
    print("6. Cetak slip gaji")
    print("7. Laporan penggajian")
    print("0. Keluar")


def main():
    while True:  # program berjalan terus sampai user memilih keluar
        tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            tambah_karyawan()
        elif pilihan == "2":
            lihat_karyawan()
        elif pilihan == "3":
            ubah_karyawan()
        elif pilihan == "4":
            hapus_karyawan()
        elif pilihan == "5":
            input_absensi_lembur()
        elif pilihan == "6":
            cetak_slip()
        elif pilihan == "7":
            laporan_penggajian()
        elif pilihan == "0":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("[!] Menu tidak valid, coba lagi.")


if __name__ == "__main__":
    main()