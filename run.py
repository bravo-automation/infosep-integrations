import sys

def run_tecnoglobal():
    from tecnoglobal.tecnoglobal import TecnoGlobal
    tg = TecnoGlobal()
    tg.get_products()
    tg.organize_products()

def run_intcomex():
    from intcomex.intcomex import Intcomex
    intcomex = Intcomex()
    intcomex.get_info_from_intcomex()

if __name__ == "__main__":
    print("Select which script to run:")
    print("1. TecnoGlobal")
    print("2. Intcomex")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        run_tecnoglobal()
    elif choice == "2":
        run_intcomex()
    else:
        print("Invalid choice. Please select 1 or 2.")