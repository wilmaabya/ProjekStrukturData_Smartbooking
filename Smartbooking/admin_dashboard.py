from db import get_connection
import re 
import psycopg2  
import os
from tabulate import tabulate
from heap_priority_queue import MaxHeap


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def admin_dashboard():
    while True:
        clear_console()
        print("\n=== Dashboard Admin ===")
        print("1. Lihat Data Booking Customers")
        print("2. Lihat Data Customers")
        print("3. Kelola Paket Jasa")
        print("4. Kelola Fotografer")
        print("5. Lihat Review")
        print("6. Lihat Booking Pending (Priority)") 
        print("7. Lihat Booking Prioritas (MaxHeap)")
        print("8. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_booking_customers()
        elif pilihan == "2":
            lihat_data_customers()
        elif pilihan == "3":
            kelola_paket_jasa()
        elif pilihan == "4":
            kelola_fotografer()
        elif pilihan == "5":
            lihat_review()
        elif pilihan == "6":
            lihat_booking_pending_priority()      # ➜ panggil fungsi heap
        elif pilihan == "7":
            lihat_booking_prioritas()
        elif pilihan == "8":
            break

        else:
            print("Pilihan tidak valid!")
            input("Tekan enter untuk lanjut")
            clear_console()

def lihat_booking_customers():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                b.id_booking,
                u.id_pengguna,
                u.nama,
                pj.nama_paket,
                b.tanggal_booking,
                b.tanggal_pelaksanaan,
                b.waktu_mulai,
                b.waktu_selesai,
                b.tempat,
                sb.status,
                b.jumlah,
                b.catatan,
                f.nama,
                p.total_harga,
                p.tanggal_pembayaran,
                mp.metode_pembayaran
            FROM booking b
            JOIN pengguna u ON b.id_pengguna = u.id_pengguna
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
            JOIN status_booking sb ON b.id_status_booking = sb.id_status_booking
            LEFT JOIN fotografer f ON b.id_fotografer = f.id_fotografer
            LEFT JOIN pembayaran p ON b.id_booking = p.id_booking
            LEFT JOIN metode_pembayaran mp ON p.id_metode_pembayaran = mp.id_metode_pembayaran
            ORDER BY b.tanggal_booking DESC
        """)

        bookings = cur.fetchall()
        if not bookings:
            print("Tidak ada data booking.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        for b in bookings:
            print("\n------------------------------------")
            print(f"ID Booking          : {b[0]}")
            print(f"ID Pengguna         : {b[1]}")
            print(f"Nama Pengguna       : {b[2]}")
            print(f"Nama Paket          : {b[3]}")
            print(f"Tanggal Booking     : {b[4]}")
            print(f"Tanggal Pelaksanaan : {b[5] or '-'}")
            print(f"Waktu Mulai         : {b[6].strftime('%H:%M') if b[6] else '-'}")
            print(f"Waktu Selesai       : {b[7].strftime('%H:%M') if b[7] else '-'}")
            print(f"Tempat              : {b[8] or '-'}")
            print(f"Status Booking      : {b[9]}")
            print(f"Jumlah              : {b[10] or '-'}")
            print(f"Catatan             : {b[11] or '-'}")
            print(f"Fotografer          : {b[12] or '-'}")
            print(f"Total harga         : {b[13]}")
            print(f"Tanggal Pembayaran  : {b[14] or '-'}")
            print(f"Metode Pembayaran   : {b[15] or '-'}")

        print("\n--- Ubah Status Booking ---")
        ubah = input("Mau ubah status booking? (y/n): ")
        if ubah.lower() == 'y':
            id_booking = input("Masukkan ID Booking yang ingin diubah: ")

            cur.execute("SELECT id_status_booking FROM booking WHERE id_booking = %s", (id_booking,))
            res = cur.fetchone()

            if not res:
                print("ID Booking tidak ditemukan.")
                input("Tekan enter untuk lanjut")
                clear_console()
                return

            print("\nPilih Status Baru:")
            print("1. Disetujui")
            print("2. Dibatalkan")
            print("3. Selesai")
            status_pilihan = input("Pilih (1/2/3): ")

            if status_pilihan not in ['1', '2', '3']:
                print("Pilihan status tidak valid.")
                input("Tekan enter untuk lanjut")
                clear_console()
                return

            status_mapping = {
            '1': 2, 
            '2': 3,  
            '3': 4   
            }
            status_baru = status_mapping[status_pilihan]

            cur.execute("""
                UPDATE booking SET id_status_booking = %s
                WHERE id_booking = %s
            """, (int(status_baru), id_booking))
            conn.commit()
            print("Status booking berhasil diperbarui.")
            input("Tekan enter untuk lanjut")
            clear_console()

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def lihat_data_customers():
    print("\n=== Data Seluruh Customer ===")
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT nama, email, no_telepon, username
            FROM pengguna
            WHERE id_role = '2'
            ORDER BY nama
        """)

        customers = cur.fetchall()

        if not customers:
            print("Belum ada data customer.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print(f"{'No':<3} {'Nama':<25} {'Email':<30} {'No Telepon':<15} {'Username':<20}")
        print("-" * 100)

        for idx, (nama, email, no_telepon, username) in enumerate(customers, start=1):
            print(f"{idx:<3} {nama:<25} {email:<30} {no_telepon:<15} {username:<20}")

    except Exception as e:
        print("Terjadi kesalahan saat mengambil data customer:", e)

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def lihat_data_customers():
    print("\n=== Data Seluruh Customer ===")
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT nama, email, no_telepon, username
            FROM pengguna
            WHERE id_role = '2'
            ORDER BY nama
        """)

        customers = cur.fetchall()

        if not customers:
            print("Belum ada data customer.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print(f"{'No':<3} {'Nama':<25} {'Email':<30} {'No Telepon':<15} {'Username':<20}")
        print("-" * 100)

        for idx, (nama, email, no_telepon, username) in enumerate(customers, start=1):
            print(f"{idx:<3} {nama:<25} {email:<30} {no_telepon:<15} {username:<20}")

    except Exception as e:
        print("Terjadi kesalahan saat mengambil data customer:", e)

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def kelola_paket_jasa():
    while True:
        print("\n=== Kelola Data Paket Jasa ===")
        print("1. Lihat Data Paket Jasa")
        print("2. Input Data Paket Jasa Baru")
        print("3. Update Paket Jasa")
        print("4. Hapus Paket Jasa")
        print("5. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_paket_jasa()
        elif pilihan == "2":
            input_paket_jasa()
        elif pilihan == "3":
            update_paket_jasa()
        elif pilihan == "4":
            hapus_paket_jasa()
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()

def lihat_paket_jasa():
    print("\n=== Data Paket Jasa ===")
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                p.id_paket_jasa,
                p.nama_paket,
                p.harga,
                p.deskripsi,
                p.durasi,
                j.nama_jenis,
                COALESCE(db.total_dipesan, 0) AS total_dipesan
            FROM paket_jasa p
            JOIN jenis_layanan j ON p.id_jenis_layanan = j.id_jenis_layanan
            LEFT JOIN (
                SELECT id_paket_jasa, COUNT(*) AS total_dipesan
                FROM booking
                GROUP BY id_paket_jasa
            ) AS db ON p.id_paket_jasa = db.id_paket_jasa
            ORDER BY p.id_paket_jasa;
        """)

        paket_jasa = cur.fetchall()

        if not paket_jasa:
            print("Belum ada paket jasa.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        table_data = []
        for (id_paket_jasa, nama_paket, harga, deskripsi, durasi, nama_jenis, total_dipesan) in paket_jasa:
            harga_format = f"Rp{harga:,.0f}".replace(",", ".")
            deskripsi_ringkas = (deskripsi[:50] + "...") if len(deskripsi) > 50 else deskripsi
            table_data.append([
                id_paket_jasa, nama_paket, harga_format, deskripsi_ringkas, f"{durasi} jam", nama_jenis, total_dipesan
            ])

        headers = ["Id Paket", "Nama Paket", "Harga", "Deskripsi", "Durasi", "Jenis Layanan", "Total Dipesan"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    except Exception as e:
        print("Terjadi kesalahan saat mengambil data paket jasa:", e)

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def input_paket_jasa():
    print("\n=== Input Paket Jasa Baru ===")

    nama = input("Nama Paket: ").strip()
    if not nama:
        print("Nama paket tidak boleh kosong.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    harga_input = input("Harga (Rp): ").strip()
    if not harga_input.isdigit():
        print("Harga harus berupa angka positif.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return
    
    harga = int(harga_input)
    if harga <= 0:
        print("Harga harus lebih dari 0.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    deskripsi = input("Deskripsi: ").strip()
    if not deskripsi:
        print("Deskripsi tidak boleh kosong.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    durasi_input = input("Durasi (jam) [0 = tanpa jadwal, 2, 5, 12]: ").strip()
    if not durasi_input.isdigit():
        print("Durasi harus berupa angka 0, 5, atau 12.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return
    durasi = int(durasi_input)
    if durasi not in [0, 2, 5, 12]:
        print("Durasi tidak valid. Hanya boleh 0, 2, 5, atau 12.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    print("Pilih Jenis Layanan:")
    print("1. Fotografi")
    print("2. Videografi")
    print("3. Desain")
    print("4. Fotografi + Videografi")
    jenis_input_str = input("Masukkan ID Jenis Layanan (1-4): ").strip()
    if not jenis_input_str.isdigit():
        print("ID Jenis Layanan harus berupa angka 1 sampai 4.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return
    jenis_input = int(jenis_input_str)
    if jenis_input not in [1, 2, 3, 4]:
        print("ID Jenis Layanan tidak valid.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO paket_jasa (nama_paket, harga, deskripsi, durasi, id_jenis_layanan)
            VALUES (%s, %s, %s, %s, %s)
        """, (nama, harga, deskripsi, durasi, jenis_input))

        conn.commit()
        print("Paket jasa berhasil ditambahkan!")

    except Exception as e:
        print("Terjadi kesalahan saat memasukkan data paket jasa:", e)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def update_paket_jasa():
    print("\n=== Update Data Paket Jasa ===")
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id_paket_jasa, nama_paket FROM paket_jasa ORDER BY id_paket_jasa")
        paket_list = cur.fetchall()

        if not paket_list:
            print("Belum ada paket jasa yang bisa diupdate.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print("\nDaftar Paket Jasa:")
        for id_paket, nama in paket_list:
            print(f"{id_paket}. {nama}")

        id_paket_input = input("\nMasukkan ID Paket Jasa yang ingin diubah: ")

        cur.execute("SELECT * FROM paket_jasa WHERE id_paket_jasa = %s", (id_paket_input,))
        data = cur.fetchone()
        if not data:
            print("ID Paket tidak ditemukan.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print("\n--- Masukkan data baru (kosongkan jika tidak ingin diubah) ---")

        nama_paket_baru = input(f"Nama Paket ({data[1]}): ") or data[1]
        
        harga_input = input(f"Harga ({data[2]}): ")
        if harga_input == '':
            harga_baru = data[2]
        else:
            try:
                harga_baru = int(harga_input)
            except ValueError:
                print("Harga harus berupa angka.")
                input("Tekan enter untuk lanjut")
                clear_console()
                return

        deskripsi_baru = input(f"Deskripsi ({data[3]}): ") or data[3]

        print("ID Jenis Layanan:")
        print("1: Fotografer")
        print("2: Videografer")
        print("3: Desain")
        print("4: Fotografer + Videografer")
        jenis_layanan_input = input(f"ID Jenis Layanan ({data[4]}): ")
        if jenis_layanan_input == '':
            jenis_layanan_baru = data[4]
        else:
            try:
                jenis_layanan_baru = int(jenis_layanan_input)
                if jenis_layanan_baru not in [1, 2, 3, 4]:
                    raise ValueError
            except ValueError:
                print("Jenis layanan hanya boleh 1, 2, 3, atau 4.")
                input("Tekan enter untuk lanjut")
                clear_console()
                return

        durasi_input = input(f"Durasi (0, 2, 5, 12 jam) ({data[5]}): ")
        if durasi_input == '':
            durasi_baru = data[5]
        else:
            try:
                durasi_baru = int(durasi_input)
                if durasi_baru not in [0, 2, 5, 12]:
                    raise ValueError
            except ValueError:
                print("Durasi hanya boleh 0, 2, 5, atau 12 jam.")
                input("Tekan enter untuk lanjut")
                clear_console()
                return

        cur.execute("""
            UPDATE paket_jasa
            SET nama_paket = %s,
                harga = %s,
                deskripsi = %s,
                id_jenis_layanan = %s,
                durasi = %s
            WHERE id_paket_jasa = %s
        """, (nama_paket_baru, harga_baru, deskripsi_baru, jenis_layanan_baru, durasi_baru, id_paket_input))

        conn.commit()
        print("Data paket jasa berhasil diperbarui.")

    except Exception as e:
        print("Terjadi kesalahan saat mengupdate data paket jasa:", e)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

    input("Tekan enter untuk lanjut")
    clear_console()

def hapus_paket_jasa():
    clear_console()
    print("\n=== Hapus Paket Jasa ===")
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id_paket_jasa, nama_paket FROM paket_jasa ORDER BY id_paket_jasa")
        paket_list = cur.fetchall()

        if not paket_list:
            print("Belum ada data paket jasa.")
            input("Tekan enter untuk kembali...")
            clear_console()
            return

        print("\nDaftar Paket Jasa:")
        for id_paket, nama_paket in paket_list:
            print(f"ID: {id_paket} - Nama: {nama_paket}")

        id_hapus = input("\nMasukkan ID Paket Jasa yang ingin dihapus: ")

        cur.execute("SELECT * FROM paket_jasa WHERE id_paket_jasa = %s", (id_hapus,))
        if not cur.fetchone():
            print("ID paket jasa tidak ditemukan.")
            input("Tekan enter untuk kembali...")
            clear_console()
            return

        konfirmasi = input(f"Apakah kamu yakin ingin menghapus paket jasa dengan ID {id_hapus}? (y/n): ").lower()
        if konfirmasi != 'y':
            print("Penghapusan dibatalkan.")
            input("Tekan enter untuk kembali...")
            clear_console()
            return

        cur.execute("DELETE FROM paket_jasa WHERE id_paket_jasa = %s", (id_hapus,))
        conn.commit()

        print("Paket jasa berhasil dihapus.")
    except Exception as e:
        print("Terjadi kesalahan saat menghapus paket jasa:", e)
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
        input("Tekan enter untuk kembali...")
        clear_console()

def kelola_fotografer():
    while True:
        print("\n=== Kelola Data Fotografer ===")
        print("1. Lihat Data Fotografer")
        print("2. Input Data Fotografer Baru")
        print("3. Update Data Fotografer")
        print("4. Hapus Data Fotografer")
        print("5. Tempatkan Fotografer ke Booking Disetujui")
        print("6. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_data_fotografer()
        elif pilihan == "2":
            input_fotografer()
        elif pilihan == "3":
            update_fotografer()
        elif pilihan == "4":
            hapus_fotografer()
        elif pilihan == "5":
            tempatkan_fotografer()
        elif pilihan == "6":
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()

def lihat_data_fotografer():
    print("\n=== Data Seluruh Fotografer ===")
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT b.id_fotografer, f.nama, f.email, f.no_telepon, COUNT(*) as total_booking
            FROM booking b
            JOIN fotografer f ON b.id_fotografer = f.id_fotografer
            GROUP BY b.id_fotografer, f.nama, f.email, f.no_telepon
            HAVING COUNT(*) >= 1
            ORDER BY b.id_fotografer
        """)

        fotografer = cur.fetchall()

        if not fotografer:
            print("Belum ada data fotografer.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print(f"{'ID':<3} {'Nama':<25} {'Email':<30} {'No Telepon':<15} {'Total Booking':<15}")
        print("-" * 100)

        for id_fotografer, nama, email, no_telepon, total_booking in fotografer:
            print(f"{id_fotografer:<3} {nama:<25} {email:<30} {no_telepon:<15} {total_booking:<15}")

    except Exception as e:
        print("Terjadi kesalahan saat mengambil data fotografer:", e)

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def input_fotografer():
    print("\n=== Input Data Fotografer ===")

    nama = input("Nama Fotografer: ").strip()
    if not nama:
        print("Nama fotografer tidak boleh kosong.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    email = input("Email: ").strip()
    if not email:
        print("Email tidak boleh kosong.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        print("Format email tidak valid.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    no_telp = input("No Telepon: ").strip()
    if not no_telp:
        print("Nomor telepon tidak boleh kosong.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return
    if not no_telp.isdigit():
        print("Nomor telepon hanya boleh berisi angka.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return
    if not no_telp.startswith("08"):
        print("Nomor telepon harus diawali dengan '08'.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return
    if len(no_telp) != 12:
        print("Nomor telepon harus terdiri dari 12 digit angka.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO fotografer (nama, email, no_telepon)
            VALUES (%s, %s, %s)
        """, (nama, email, no_telp))

        conn.commit()
        print("Fotografer berhasil ditambahkan.")

    except psycopg2.errors.UniqueViolation:
        print("Gagal menambahkan: Email sudah digunakan fotografer lain.")
        conn.rollback()

    except Exception as e:
        print("Terjadi kesalahan saat input fotografer:", e)
        if conn:
            conn.rollback()

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

    input("Tekan enter untuk lanjut")
    clear_console()

def update_fotografer():
    print("\n=== Update Data Fotografer ===")
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id_fotografer, nama FROM fotografer ORDER BY id_fotografer")
        fotografer_list = cur.fetchall()

        if not fotografer_list:
            print("Belum ada data fotografer.")
            input("Tekan enter untuk lanjut...")
            clear_console()
            return

        print("\nDaftar Fotografer:")
        for id_foto, nama in fotografer_list:
            print(f"{id_foto}. {nama}")

        id_foto = input("\nMasukkan ID Fotografer yang ingin diupdate: ")

        cur.execute("SELECT * FROM fotografer WHERE id_fotografer = %s", (id_foto,))
        data = cur.fetchone()

        if not data:
            print("ID Fotografer tidak ditemukan.")
            input("Tekan enter untuk lanjut...")
            clear_console()
            return

        print("\n--- Masukkan data baru (kosongkan jika tidak ingin diubah) ---")

        nama_baru = input(f"Nama ({data[1]}): ") or data[1]
        email_baru = input(f"Email ({data[2]}): ") or data[2]
        telepon_baru = input(f"No Telepon ({data[3]}): ") or data[3]

        if '@' not in email_baru or '.' not in email_baru:
            print("Email tidak valid. Harus mengandung '@' dan '.'")
            input("Tekan enter untuk lanjut...")
            clear_console()
            return

        if not telepon_baru.startswith("08") or len(telepon_baru) != 12 or not telepon_baru.isdigit():
            print("Nomor telepon harus dimulai dengan '08' dan terdiri dari 12 digit angka.")
            input("Tekan enter untuk lanjut...")
            clear_console()
            return

        cur.execute("""
            UPDATE fotografer
            SET nama = %s, email = %s, no_telepon = %s
            WHERE id_fotografer = %s
        """, (nama_baru, email_baru, telepon_baru, id_foto))

        conn.commit()
        print("Data fotografer berhasil diupdate.")

    except Exception as e:
        print("Terjadi kesalahan:", e)

    finally:
        cur.close()
        conn.close()
        input("Tekan enter untuk lanjut...")
        clear_console()

def hapus_fotografer():
    clear_console()
    print("\n=== Hapus Data Fotografer ===")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id_fotografer, nama FROM fotografer ORDER BY id_fotografer")
        fotografer_list = cur.fetchall()

        if not fotografer_list:
            print("Belum ada data fotografer.")
            input("Tekan enter untuk kembali...")
            clear_console()
            return

        print("\nDaftar Fotografer:")
        for id_f, nama in fotografer_list:
            print(f"ID: {id_f} - Nama: {nama}")

        id_hapus = input("\nMasukkan ID Fotografer yang ingin dihapus: ").strip()

        cur.execute("SELECT * FROM fotografer WHERE id_fotografer = %s", (id_hapus,))
        if not cur.fetchone():
            print("ID fotografer tidak ditemukan.")
            input("Tekan enter untuk kembali...")
            clear_console()
            return

        konfirmasi = input(f"Apakah kamu yakin ingin menghapus fotografer dengan ID {id_hapus}? (y/n): ").lower()
        if konfirmasi != 'y':
            print("Penghapusan dibatalkan.")
            input("Tekan enter untuk kembali...")
            clear_console()
            return

        cur.execute("DELETE FROM fotografer WHERE id_fotografer = %s", (id_hapus,))
        conn.commit()

        print("Fotografer berhasil dihapus.")

    except Exception as e:
        print("Terjadi kesalahan saat menghapus fotografer:", e)
        if conn:
            conn.rollback()

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

        input("Tekan enter untuk kembali...")
        clear_console()

def tempatkan_fotografer():
    print("\n=== Tempatkan Fotografer ===")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT b.id_booking, p.nama_paket, u.nama, b.tanggal_pelaksanaan, b.waktu_mulai, b.waktu_selesai
            FROM booking b
            JOIN paket_jasa p ON b.id_paket_jasa = p.id_paket_jasa
            JOIN pengguna u ON b.id_pengguna = u.id_pengguna
            WHERE b.id_status_booking = 2 AND b.id_fotografer IS NULL
            ORDER BY b.tanggal_pelaksanaan
        """)
        bookings = cur.fetchall()

        if not bookings:
            print("Tidak ada booking disetujui yang belum memiliki fotografer.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print("Daftar Booking:")
        for b in bookings:
            print(f"{b[0]} - {b[1]} | Customer: {b[2]} | Tanggal: {b[3] or '-'} | Waktu: {b[4] or '-'} - {b[5] or '-'}")

        id_booking = int(input("Masukkan ID Booking yang akan ditempatkan fotografer: "))
        if not any(b[0] == id_booking for b in bookings):
            print("ID Booking tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        cur.execute("SELECT id_fotografer, nama FROM fotografer ORDER BY id_fotografer")
        fotografer_list = cur.fetchall()

        if not fotografer_list:
            print("Belum ada fotografer terdaftar.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print("Daftar Fotografer:")
        for f in fotografer_list:
            print(f"{f[0]} - {f[1]}")

        id_fotografer = int(input("Masukkan ID Fotografer yang akan ditempatkan: "))
        if not any(f[0] == id_fotografer for f in fotografer_list):
            print("ID Fotografer tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        cur.execute("""
            UPDATE booking SET id_fotografer = %s
            WHERE id_booking = %s
        """, (id_fotografer, id_booking))
        conn.commit()

        print("Fotografer berhasil ditempatkan ke booking.")

    except Exception as e:
        print("Terjadi kesalahan saat menempatkan fotografer:", e)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def lihat_review():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT r.id_review, u.nama, pj.nama_paket, r.rating, r.komentar, r.tanggal_review
            FROM review r
            JOIN booking b ON r.id_booking = b.id_booking
            JOIN pengguna u ON b.id_pengguna = u.id_pengguna
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
        """)
        reviews = cur.fetchall()

        if not reviews:
            print("Belum ada review.")
            return

        n = len(reviews)
        for i in range(n):
            for j in range(0, n - i - 1):
                if reviews[j][3] < reviews[j + 1][3]: 
                    reviews[j], reviews[j + 1] = reviews[j + 1], reviews[j]

        print("\n--- Semua Review (disorting rating tertinggi) ---")
        for r in reviews:
            print("\n-----------------------------")
            print(f"Nama Pengguna  : {r[1]}")
            print(f"Nama Paket     : {r[2]}")
            print(f"Rating         : {r[3]}")
            print(f"Komentar       : {r[4]}")
            print(f"Tanggal Review : {r[5].strftime('%Y-%m-%d')}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def lihat_booking_pending_priority():
    clear_console()
    print("\n=== Booking Pending (Priority Queue) ===")

    try:
        conn = get_connection()
        cur = conn.cursor()

        # ambil booking pending (status pending = 1)
        cur.execute("""
            SELECT 
                b.id_booking,
                u.nama,
                b.tanggal_pelaksanaan,
                pj.harga
            FROM booking b
            JOIN pengguna u ON b.id_pengguna = u.id_pengguna
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
            WHERE b.id_status_booking = 1
        """)

        data = cur.fetchall()

        if not data:
            print("Tidak ada booking pending.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        # buat heap
        heap = MaxHeap()
        import datetime
        now = datetime.datetime.now()

        # masukkan ke heap
        for id_booking, nama_cust, tgl_pelaksanaan, harga in data:
            if tgl_pelaksanaan is None:
                # kalo belum ada tanggal, prioritas kecil
                priority = -9999
            else:
                tgl_obj = datetime.datetime.strptime(str(tgl_pelaksanaan), "%Y-%m-%d")
                selisih_hari = (tgl_obj - now).days
                priority = -abs(selisih_hari)

            # format item: (priority, id, nama, tanggal)
            heap.insert((priority, id_booking, nama_cust, tgl_pelaksanaan))

        print("\nBooking Prioritas Teratas:")
        print("(berdasarkan tanggal paling dekat)")

        # ambil 1 booking paling urgent
        top = heap.extract_max()
        if not top:
            print("Heap kosong.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        priority, idb, nama_cust, tgl_pel = top

        print("\n----------------------------------")
        print(f"ID Booking     : {idb}")
        print(f"Nama Customer  : {nama_cust}")
        print(f"Tanggal        : {tgl_pel}")
        print("----------------------------------")

        input("\nTekan enter untuk lanjut")
        clear_console()

    except Exception as e:
        print("Terjadi kesalahan saat memproses priority queue:", e)
        input("Tekan enter untuk lanjut")
        clear_console()

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

def lihat_booking_prioritas():
    print("\n=== Booking Prioritas (MaxHeap) ===")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                b.id_booking,
                u.nama,
                pj.nama_paket,
                b.tanggal_booking,
                b.tanggal_pelaksanaan,
                b.waktu_mulai,
                sb.status,
                b.jumlah,
                COALESCE(p.total_harga, 0)
            FROM booking b
            JOIN pengguna u ON b.id_pengguna = u.id_pengguna
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
            JOIN status_booking sb ON b.id_status_booking = sb.id_status_booking
            LEFT JOIN pembayaran p ON b.id_booking = p.id_booking
        """)

        data = cur.fetchall()

        if not data:
            print("Tidak ada booking sama sekali.")
            input("Tekan enter untuk lanjut...")
            clear_console()
            return

        # INISIASI MAX HEAP
        heap = MaxHeap()

        # MASUKKAN BOOKING KE DALAM HEAP
        for row in data:
            id_booking = row[0]
            nama = row[1]
            paket = row[2]
            tanggal = row[3]
            pelaksanaan = row[4]
            mulai = row[5]
            status = row[6]
            jumlah = row[7]
            harga = row[8]

            # bikin skor prioritas
            skor = 0

            # prioritas paling tinggi: sudah bayar
            if harga > 0:
                skor += 1000

            # booking lebih baru prioritas naik
            if tanggal:
                skor += tanggal.toordinal()

            # jumlah peserta juga jadi faktor
            skor += (jumlah or 1) * 5

            # status tertentu dinaikkan
            if status.lower() == "menunggu":
                skor += 50
            elif status.lower() == "disetujui":
                skor += 150

            heap.push(skor, {
                "id_booking": id_booking,
                "nama": nama,
                "paket": paket,
                "tanggal_booking": tanggal,
                "tanggal_pelaksanaan": pelaksanaan,
                "waktu_mulai": mulai,
                "status": status,
                "jumlah": jumlah,
                "harga": harga
            })

        print("\n--- Urutan Booking Berdasarkan Prioritas ---")
        rank = 1

        while not heap.is_empty():
            skor, item = heap.pop()
            print(f"\n#{rank} | PRIORITAS: {skor}")
            print(f"ID Booking   : {item['id_booking']}")
            print(f"Customer     : {item['nama']}")
            print(f"Paket        : {item['paket']}")
            print(f"Tanggal Book : {item['tanggal_booking']}")
            print(f"Pelaksanaan  : {item['tanggal_pelaksanaan'] or '-'}")
            print(f"Waktu Mulai  : {item['waktu_mulai'] or '-'}")
            print(f"Jumlah       : {item['jumlah']}")
            print(f"Total Bayar  : {item['harga']}")
            print(f"Status       : {item['status']}")
            rank += 1

    except Exception as e:
        print("Terjadi kesalahan saat mengambil booking:", e)
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

    input("\nTekan enter untuk lanjut...")
    clear_console()
