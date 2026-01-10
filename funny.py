import os
import subprocess
import sys
import time

# Color definitions
G, Y, R, B, C, W = "\033[92m", "\033[93m", "\033[91m", "\033[94m", "\033[96m", "\033[0m"

def get_ip():
    try:
        ip = subprocess.getoutput("hostname -I | cut -d' ' -f1")
        return ip
    except: return "Unknown"

def banner():
    os.system('clear')
    server_ip = get_ip()
    print(f"{B}=================================================={W}")
    print(f"{C}          ZAKERIA PROJECT - ULTIMATE VPS         {W}")
    print(f"{Y}    IP: {server_ip} | Developed by: @zakeria90    {W}")
    print(f"{B}=================================================={W}")

def run_cmd(command):
    try: subprocess.run(command, shell=True, check=True)
    except Exception as e: print(f"{R}Error: {e}{W}")

def setup_ultimate_panel():
    banner()
    print(f"{R}[!] CRITICAL STEP:{W}")
    domain = input(f"{Y}Please enter your Domain (Pointed to this IP): {W}")
    
    if not domain:
        print(f"{R}Domain is required to proceed!{W}")
        time.sleep(2)
        return

    print(f"{G}>>> Starting Installation for Domain: {domain}{W}")
    time.sleep(2)

    # 1. Update & Base Tools
    run_cmd("apt update && apt install -y nginx stunnel4 sslh screen socat ufw dropbear curl")

    # 2. SSL Certificate (Acme.sh) - طلب الشهادة أولاً
    print(f"{C}Requesting SSL Certificate for {domain}...{W}")
    run_cmd("curl https://get.acme.sh | sh")
    # محاولة استخراج الشهادة (يجب أن يكون الدومين مربوطاً بالـ IP)
    run_cmd(f"~/.acme.sh/acme.sh --issue -d {domain} --standalone --force")

    # 3. Configure All Requested Ports
    print(f"{C}Opening All Multi-Protocol Ports...{W}")
    tcp_p = ["80", "443", "8080", "8443", "8880", "8062", "8000", "9443", "2082", "3303", "109", "111", "69"]
    udp_p = ["7300", "5300", "5353", "53"]
    for tp in tcp_p: run_cmd(f"ufw allow {tp}/tcp")
    for up in udp_p: run_cmd(f"ufw allow {up}/udp")
    run_cmd("ufw allow 1:65535/udp")
    run_cmd("echo 'y' | ufw enable")

    # 4. Install Xray Core
    print(f"{C}Installing Xray Core...{W}")
    run_cmd("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")

    # 5. BadVPN for Gaming
    run_cmd("wget -O /usr/bin/badvpn-udpgw https://github.com/ambrop72/badvpn/raw/master/udpgw/badvpn-udpgw && chmod +x /usr/bin/badvpn-udpgw")
    run_cmd("screen -dmS badvpn badvpn-udpgw --listen-addr 127.0.0.1:7300")

    print(f"\n{G}SUCCESS! System is ready with Domain: {domain}{W}")
    input("Press Enter to return to menu...")

def main_menu():
    while True:
        banner()
        print(f"{G}[01]{W} Start Full Installation (Requires Domain)")
        print(f"{G}[02]{W} Create SSH/V2Ray User")
        print(f"{G}[03]{W} Renew SSL Certificate")
        print(f"{G}[04]{W} Speedtest & Resources")
        print(f"{R}[00]{W} Exit")
        print(f"{B}--------------------------------------------------{W}")
        
        choice = input(f"{C}Select: {W}")
        if choice == '1' or choice == '01':
            setup_ultimate_panel()
        elif choice == '2' or choice == '02':
            u = input("Username: "); p = input("Password: ")
            run_cmd(f"useradd -e `date -d '30 days' +'%Y-%m-%d'` -s /bin/false -M {u} && echo '{u}:{p}' | chpasswd")
            print(f"{G}User {u} created!{W}"); time.sleep(2)
        elif choice == '3' or choice == '03':
            run_cmd("~/.acme.sh/acme.sh --cron")
        elif choice == '0' or choice == '00':
            break

if __name__ == "__main__":
    main_menu()
