from db import get_connection
import datetime 
from rekomendasi_knapsack import rekomendasi_paket_knapsack
from tabulate import tabulate 
import os
from interval_tree import IntervalTree

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def customer_dashboard(customer_id): 
    while True:
        clear_console()
        print("\n=== Dashboard Customer ===")
        print("1. Booking Jadwal")
        print("2. Lihat Data Booking Saya")
        print("3. Batalkan Booking")
        print("4. Pilih Metode Pembayaran")
        print("5. Rekomendasi Paket Berdasarkan Budget")
        print("6. Review")
        print("7. Keluar ke Menu Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            booking_jadwal(customer_id)
        elif pilihan == "2":
            lihat_data_booking(customer_id)
        elif pilihan == "3":
            batalkan_booking(customer_id)
        elif pilihan == "4":
            pilih_metode_pembayaran(customer_id)
        elif pilihan == "5":
            rekomendasi_paket_knapsack()
        elif pilihan == "6":
            review_menu(customer_id)
        elif pilihan == "7":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan enter untuk lanjut")
            clear_console()

def get_all_paket(): 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_paket_jasa, nama_paket, harga, deskripsi, durasi FROM paket_jasa ORDER BY id_paket_jasa")
    paket_list = cur.fetchall()
    cur.close()
    conn.close()
    return paket_list

def get_sorted_bookings(tanggal): 
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT waktu_mulai, waktu_selesai
        FROM booking
        JOIN status_booking ON booking.id_status_booking = status_booking.id_status_booking
        WHERE status_booking.status != 'Dibatalkan' AND tanggal_pelaksanaan = %s
        ORDER BY waktu_mulai
    """, (tanggal,))

    rows = cur.fetchall() 
    cur.close()
    conn.close()

    def to_time(t): 
        if isinstance(t, str):
            return datetime.datetime.strptime(t, "%H:%M:%S").time()
        return t

    result = []
    for row in rows: 
        mulai = to_time(row[0])
        selesai = to_time(row[1])
        result.append((mulai, selesai))
    return result

def binary_search(arr, target): 
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left

def is_slot_available(tanggal, mulai, selesai): 
    bookings = get_sorted_bookings(tanggal) 

    waktu_mulai = []
    for booking in bookings: 
        start_booking = booking[0] 
        waktu_mulai.append(start_booking)
    idx = binary_search(waktu_mulai, mulai) 

    def conflict(start1, end1, start2, end2): 
        return start1 < end2 and start2 < end1 

    for i in [idx - 1, idx]: 
        if 0 <= i < len(bookings): 
            start_db, end_db = bookings[i] 
            if conflict(mulai, selesai, start_db, end_db): 
                return False
    return True

def booking_jadwal(customer_id):
    print("\n=== Booking Jadwal ===")
    paket_jasa = get_all_paket()  

    table_data = []
    for (id_paket_jasa, nama_paket, harga, deskripsi, durasi) in paket_jasa:
        harga_format = f"Rp{harga:,.0f}".replace(",", ".")
        deskripsi_ringkas = (deskripsi[:98] + "...") if len(deskripsi) > 98 else deskripsi
        table_data.append([
            id_paket_jasa, nama_paket, harga_format, deskripsi_ringkas, f"{durasi} jam"
        ])

    headers = ["Id Paket", "Nama Paket", "Harga", "Deskripsi", "Durasi"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    try:
        id_paket_jasa = int(input("Masukkan ID Paket yang dipilih: "))
        paket = None
        for p in paket_jasa:
            if p[0] == id_paket_jasa:
                paket = p
                break
        
        if paket is None:
            print("ID Paket tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        durasi = paket[4]  
        tanggal_booking = datetime.date.today()
        tanggal_pelaksanaan_dt = None
        waktu_mulai_dt = None
        waktu_selesai_dt = None
        tempat = None

        if durasi == 0:
            pass

        else:
            tanggal_pelaksanaan = input("Tanggal Pelaksanaan (YYYY-MM-DD): ")
            tanggal_pelaksanaan_dt = datetime.datetime.strptime(tanggal_pelaksanaan, "%Y-%m-%d").date()

            if durasi == 12:
                waktu_mulai_dt = datetime.time(8, 0)
                waktu_selesai_dt = datetime.time(20, 0)
                if not is_slot_available(tanggal_pelaksanaan_dt, waktu_mulai_dt, waktu_selesai_dt):
                    print("Jadwal full day sudah terisi pada tanggal tersebut.")
                    input("Tekan enter untuk lanjut")
                    clear_console()
                    return
                tempat = input("Tempat: ")
                
            else: 
                start_hour = 8
                end_hour = 20
                available_slots = [] 
                for hour in range(start_hour, end_hour - durasi + 1): 
                    mulai_coba = datetime.time(hour, 0) 
                    selesai_coba = (datetime.datetime.combine(datetime.date.today(), mulai_coba) + datetime.timedelta(hours=durasi)).time() 
                    if is_slot_available(tanggal_pelaksanaan_dt, mulai_coba, selesai_coba):
                        available_slots.append((mulai_coba, selesai_coba)) 

                if not available_slots:
                    print("Tidak ada slot waktu tersedia pada tanggal tersebut.")
                    input("Tekan enter untuk lanjut")
                    clear_console()
                    return

                print("Slot waktu tersedia:")
                nomor = 1
                for slot in available_slots:
                    mulai = slot[0]
                    selesai = slot[1]
                    print(f"{nomor}. {mulai.strftime('%H:%M')} - {selesai.strftime('%H:%M')}")
                    nomor += 1

                pilihan_slot = int(input("Pilih nomor slot: "))
                if not (1 <= pilihan_slot <= len(available_slots)):
                    print("Pilihan slot tidak valid.")
                    input("Tekan enter untuk lanjut")
                    clear_console()
                    return

                slot_dipilih = available_slots[pilihan_slot - 1]
                waktu_mulai_dt = slot_dipilih[0]
                waktu_selesai_dt = slot_dipilih[1]
                tempat = input("Tempat: ")

        jumlah = input("Jumlah item (opsional): ")
        catatan = input("Catatan (opsional): ")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO booking (
                tanggal_booking, tanggal_pelaksanaan, waktu_mulai, waktu_selesai, 
                tempat, id_pengguna, id_fotografer, id_status_booking, 
                id_paket_jasa, jumlah, catatan
            ) VALUES (%s, %s, %s, %s, %s, %s, NULL, 1, %s, %s, %s)
            RETURNING id_booking
        """, (
            tanggal_booking, tanggal_pelaksanaan_dt, waktu_mulai_dt,
            waktu_selesai_dt, tempat, customer_id, id_paket_jasa,
            jumlah or None, catatan or None
        ))

        booking_id = cur.fetchone()[0]
        conn.commit()
        print("Booking berhasil disimpan!")

        if durasi == 0:
            print("Konsultasi desain lebih lanjut hubungi Hajar Media No.Telp: 083135806641")

    except Exception as e:
        print("Terjadi kesalahan saat booking:", e)

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def lihat_data_booking(customer_id):
    print("\n=== Riwayat Booking Anda ===")

    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                b.id_booking,
                pj.nama_paket,
                b.tanggal_booking,
                b.tanggal_pelaksanaan,
                b.waktu_mulai,
                b.waktu_selesai,
                b.tempat,
                sb.status,
                b.jumlah,
                b.catatan
            FROM booking b
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
            JOIN status_booking sb ON b.id_status_booking = sb.id_status_booking
            WHERE b.id_pengguna = %s
            ORDER BY b.id_booking
        """, (customer_id,))
        
        bookings = cur.fetchall()
        
        if not bookings:
            print("Anda belum memiliki data booking.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return
        
        for b in bookings:
            print("\n-------------------------------")
            print(f"ID Booking          : {b[0]}")
            print(f"Nama Paket          : {b[1]}")
            print(f"Tanggal Booking     : {b[2]}")
            print(f"Tanggal Pelaksanaan : {b[3] if b[3] else '-'}")
            print(f"Waktu Mulai         : {b[4].strftime('%H:%M') if b[4] else '-'}")
            print(f"Waktu Selesai       : {b[5].strftime('%H:%M') if b[5] else '-'}")
            print(f"Tempat              : {b[6] if b[6] else '-'}")
            print(f"Status              : {b[7]}")
            print(f"Jumlah              : {b[8] if b[8] else '-'}")
            print(f"Catatan             : {b[9] if b[9] else '-'}")
        print("-------------------------------")

    except Exception as e:
        print("Terjadi kesalahan saat mengambil data booking:", e)
    
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def batalkan_booking(customer_id):
    print("\n=== Pembatalan Booking ===")

    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                b.id_booking,
                pj.nama_paket,
                b.tanggal_pelaksanaan,
                b.waktu_mulai,
                b.waktu_selesai,
                sb.status,
                b.id_status_booking
            FROM booking b
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
            JOIN status_booking sb ON b.id_status_booking = sb.id_status_booking
            WHERE b.id_pengguna = %s
            ORDER BY b.id_booking 
        """, (customer_id,))
        
        bookings = cur.fetchall()
        
        if not bookings:
            print("Anda belum memiliki booking.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return
        
        print("Daftar Booking:")
        print("Booking yang sudah disetujui harus konsultasi ke admin Hajar Media: 083135806641\n")
        for b in bookings:
            print(f"{b[0]} - {b[1]} | Tanggal: {b[2] or '-'} | Waktu: {b[3] or '-'} - {b[4] or '-'} | Status: {b[5]}")
        
        booking_id = input("Masukkan ID Booking yang ingin dibatalkan: ")

        cur.execute("""
            SELECT id_status_booking FROM booking
            WHERE id_booking = %s AND id_pengguna = %s
        """, (booking_id, customer_id))
        
        result = cur.fetchone()

        if not result:
            print("Booking tidak ditemukan atau bukan milik Anda.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        current_status_id = result[0]

        if current_status_id == 1:
            cur.execute("""
                UPDATE booking SET id_status_booking = 3
                WHERE id_booking = %s
            """, (booking_id,))
            conn.commit()
            print("Booking berhasil dibatalkan.")
        elif current_status_id == 2:
            print("Booking sudah disetujui. Silahkan ajukan pembatalan melalui -Hajar Media No.Telp: 083235806641-.")
        elif current_status_id == 3:
            print("Booking ini sudah dibatalkan sebelumnya.")
        else:
            print("Status booking tidak valid untuk pembatalan.")

    except Exception as e:
        print("Terjadi kesalahan saat proses pembatalan:", e)
    
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def pilih_metode_pembayaran(customer_id):
    import datetime
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT b.id_booking, pj.nama_paket, pj.harga, b.tanggal_pelaksanaan
            FROM booking b
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
            LEFT JOIN pembayaran p ON b.id_booking = p.id_booking
            WHERE b.id_pengguna = %s AND b.id_status_booking = 2 AND p.id_pembayaran IS NULL
        """, (customer_id,))
        bookings = cur.fetchall()

        if not bookings:
            print("\nTidak ada booking yang siap dibayar.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print("\n=== Pilih Booking untuk Pembayaran ===")
        for b in bookings:
            print(f"{b[0]} - {b[1]} | Tanggal: {b[3]} | Total: Rp{b[2]:,.0f}")

        id_booking = input("Masukkan ID Booking yang ingin dibayar: ")

        valid = False
        for b in bookings:
            if str(b[0]) == id_booking:
                valid = True
                break

        if not valid:
            print("ID booking tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        harga_total = None
        for b in bookings:
            if str(b[0]) == id_booking:
                harga_total = b[2]
                break

        cur.execute("SELECT id_metode_pembayaran, metode_pembayaran FROM metode_pembayaran")
        metode = cur.fetchall()
        print("\n=== Metode Pembayaran ===")
        for m in metode:
            print(f"{m[0]}. {m[1]}")

        metode_id = int(input("Pilih metode pembayaran (masukkan ID): "))
        valid = False
        for m in metode:
            if m[0] == metode_id:
                valid = True
                break

        if not valid:
            print("Metode pembayaran tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        tanggal_pembayaran = datetime.date.today()

        cur.execute("""
            INSERT INTO pembayaran (id_booking, id_metode_pembayaran, total_harga, tanggal_pembayaran)
            VALUES (%s, %s, %s, %s)
        """, (id_booking, metode_id, harga_total, tanggal_pembayaran))

        conn.commit()
        print("Metode pembayaran berhasil dicatat. \nSilakan lakukan pembayaran dengan menghubungi Hajar Media No.Telp: 083135806641.")
    except Exception as e:
        print("Terjadi kesalahan saat proses pembayaran:", e)
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def review_menu(customer_id):
    while True:
        print("\n=== Menu Review ===")
        print("1. Lihat Review")
        print("2. Isi Review")
        print("3. Kembali")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            lihat_review()
        elif pilihan == "2":
            isi_review(customer_id)
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid!")
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
            input("Tekan enter untuk lanjut")
            clear_console()
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

def isi_review(customer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT b.id_booking, pj.nama_paket, b.tanggal_pelaksanaan
            FROM booking b
            JOIN paket_jasa pj ON b.id_paket_jasa = pj.id_paket_jasa
            WHERE b.id_pengguna = %s AND b.id_status_booking = 4
            AND b.id_booking NOT IN (SELECT id_booking FROM review)
        """, (customer_id,))
        bookings = cur.fetchall()

        if not bookings:
            print("Tidak ada booking selesai yang bisa direview.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print("\n--- Booking Selesai yang Bisa Direview ---")
        for b in bookings:
            print(f"ID Booking: {b[0]} | Paket: {b[1]} | Tgl Pelaksanaan: {b[2]}")

        id_booking = input("Masukkan ID Booking yang ingin direview: ")

        id_booking_valid = False
        for b in bookings:
            if str(b[0]) == id_booking:
                id_booking_valid = True
                break

        if not id_booking_valid:
            print("ID Booking tidak valid.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        rating = int(input("Masukkan rating (1-5): "))
        if rating < 1 or rating > 5:
            print("Rating harus antara 1 sampai 5.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        komentar = input("Masukkan komentar: ")

        tanggal_review = datetime.date.today()

        cur.execute("""
            INSERT INTO review (id_booking, rating, komentar, tanggal_review)
            VALUES (%s, %s, %s, %s)
        """, (id_booking, rating, komentar, tanggal_review))
        conn.commit()

        print("Review berhasil disimpan!")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()