from db import get_connection
import os

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def rekomendasi_paket_knapsack():
    print("\n=== Rekomendasi Paket Berdasarkan Budget ===")
    print("Kategori:")
    print("1. Wisuda")
    print("2. Wedding")
    print("3. Event")
    pilihan = input("Pilih kategori (1/2/3): ")

    if pilihan == "1":
        table = "paket_knapsack_wisuda"
    elif pilihan == "2":
        table = "paket_knapsack_wedding"
    elif pilihan == "3":
        table = "paket_knapsack_event"
    else:
        print("Pilihan tidak valid.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    try:
        budget = int(input("Masukkan budget maksimal (dalam Rupiah): "))
    except ValueError:
        print("Input budget tidak valid.")
        input("Tekan enter untuk lanjut")
        clear_console()
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT nama_item, harga, nilai_manfaat FROM {table}")
        rows = cur.fetchall()

        if not rows:
            print("Tidak ada data paket di kategori ini.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        nama_item = [row[0] for row in rows]
        harga = [row[1] for row in rows]
        nilai_manfaat = [row[2] for row in rows]
        n = len(harga)

        dp = [[0] * (budget + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(budget + 1):
                if harga[i - 1] <= w:
                    dp[i][w] = max(nilai_manfaat[i - 1] + dp[i - 1][w - harga[i - 1]], dp[i - 1][w])
                else:
                    dp[i][w] = dp[i - 1][w]

        w = budget
        selected = []
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected.append(i - 1)
                w -= harga[i - 1]

        if not selected:
            print("Tidak ada kombinasi paket yang cocok dengan budget Anda.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return

        print("\n--- Rekomendasi Paket ---")
        total_harga = 0
        total_manfaat = 0
        for i in reversed(selected):
            print(f"- {nama_item[i]} | Harga: Rp{harga[i]:,} | Nilai Manfaat: {nilai_manfaat[i]}")
            total_harga += harga[i]
            total_manfaat += nilai_manfaat[i]

        print(f"\nTotal Harga: Rp{total_harga:,}")
        print(f"Total Manfaat: {total_manfaat}")

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()