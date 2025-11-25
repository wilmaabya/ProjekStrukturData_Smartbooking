import getpass 
from db import get_connection 
import bcrypt 
import os

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def signup_customer():
    conn = get_connection() 
    cur = conn.cursor()
    print("\n=== Sign Up Customer ===")

    while True:
        nama = input("Nama: ").strip() 
        email = input("Email: ").strip()
        no_telepon = input("No Telepon: ").strip()
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        if not nama or not email or not username or not password:
            print("Data tidak lengkap, kembali ke menu utama.")
            input("Tekan enter untuk lanjut")
            clear_console()
            cur.close()
            conn.close()
            return

        if "@" not in email or "." not in email:
            print("Email tidak valid. Kembali ke menu utama.")
            print("Data tidak lengkap, kembali ke menu utama.")
            input("Tekan enter untuk lanjut")
            cur.close()
            conn.close()
            return

        if not (no_telepon.isdigit() and len(no_telepon) == 12 and no_telepon.startswith("08")): 
            print("No Telepon tidak valid")
            print("Data tidak lengkap, kembali ke menu utama.")
            input("Tekan enter untuk lanjut")
            cur.close() 
            conn.close() 
            return

        if len(username) < 3:
            print("Username minimal 3 karakter. Kembali ke menu utama.")
            print("Data tidak lengkap, kembali ke menu utama.")
            input("Tekan enter untuk lanjut")
            cur.close()
            conn.close()
            return

        if len(password) < 6:
            print("Password minimal 6 karakter. Kembali ke menu utama.")
            print("Data tidak lengkap, kembali ke menu utama.")
            input("Tekan enter untuk lanjut")
            cur.close()
            conn.close()
            return
        break

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 

    try:
        cur.execute(""" 
            INSERT INTO pengguna (nama, email, no_telepon, username, password, id_role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nama, email, no_telepon, username, hashed_pw.decode('utf-8'), 2))
        conn.commit()
        print("Akun berhasil dibuat.")
    except Exception as e:
        print("Gagal membuat akun:", e)
    finally:
        cur.close()
        conn.close()
    input("Tekan enter untuk lanjut")
    clear_console()

def login():
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id_pengguna, nama, password, id_role 
            FROM pengguna 
            WHERE username = %s
        """, (username,))
        user = cur.fetchone()
        if user:
            stored_hash = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                print(f"Selamat datang, {user[1]}!")
                input("Tekan enter untuk lanjut")
                clear_console()
                return user
            else:
                print("Password salah.")
                input("Tekan enter untuk lanjut")
                clear_console()
                return None
        else:
            print("Username tidak ditemukan.")
            input("Tekan enter untuk lanjut")
            clear_console()
            return None
    except Exception as e:
        print("Terjadi kesalahan saat login:", e)
        input("Tekan enter untuk lanjut")
        clear_console()
        return None
    finally:
        cur.close()
        conn.close()
        