from auth import signup_customer, login 
from customer_dashboard import customer_dashboard
from admin_dashboard import admin_dashboard
import os 

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def menu_utama():
    while True: 
        clear_console()
        input(f'''
            ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗            
            ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝            
            ███████╗██╔████╔██║███████║██████╔╝   ██║               
            ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║               
            ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║               
            ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝               
                                                                    
            ██████╗  ██████╗  ██████╗ ██╗  ██╗██╗███╗   ██╗ ██████╗ 
            ██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝██║████╗  ██║██╔════╝ 
            ██████╔╝██║   ██║██║   ██║█████╔╝ ██║██╔██╗ ██║██║  ███╗
            ██╔══██╗██║   ██║██║   ██║██╔═██╗ ██║██║╚██╗██║██║   ██║
            ██████╔╝╚██████╔╝╚██████╔╝██║  ██╗██║██║ ╚████║╚██████╔╝
            ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
        ''')

        print("=== Menu Utama ===")
        print("1. Login")
        print("2. Sign Up")
        print("3. Keluar")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            user = login() 
            if user: 
                id_pengguna, _, _, id_role = user 
                if id_role == 2:  
                    customer_dashboard(id_pengguna)
                elif id_role == 1:  
                    admin_dashboard()
        elif pilihan == "2":
            berhasil = signup_customer() 
            if not berhasil: 
                continue 
        elif pilihan == "3":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan enter untuk lanjut")
            clear_console()
            
if __name__ == "__main__":
    menu_utama()
