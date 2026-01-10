import os
import subprocess
import sys
import time

# Color definitions
G = "\033[92m"  # GREEN
Y = "\033[93m"  # YELLOW
R = "\033[91m"  # RED
B = "\033[94m"  # BLUE
C = "\033[96m"  # CYAN
W = "\033[0m"   # WHITE/RESET

def get_ip():
    try:
        ip = subprocess.getoutput("hostname -I | cut -d' ' -f1")
        return ip
    except:
        return "Unknown"

def banner():
    os.system('clear')
    server_ip = get_ip()
    print(f"{B}=================================================={W}")
    print(f"{C}          ZAKERIA PROJECT - ULTIMATE VPS         {W}")
    print(f"{Y}    IP: {server_ip} | Developed by: @zakeria90    {W}")
    print(f"{B}=================================================={W}")

def run_cmd(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"{R}Error: {e}{W}")

def setup_all_services():
    banner()
    print(f"{Y}Installing All Services & Opening Ports...{W}")
    
    # 1. Installing Necessary Packages
    run_cmd("apt update && apt install -y nginx stunnel4 sslh screen socat ufw dropbear")

    # 2. Opening All Requested Ports (TCP & UDP)
    tcp_ports = ["80", "443", "8080", "8443", "8880", "8062", "8000", "9443", "2082", "3303", "109", "111", "69"]
    udp_ports = ["7300", "5300", "5353", "53"]
    
    print(f"{C}Configuring Firewall...{W}")
    for tp in tcp_ports:
        run_cmd(f"ufw allow {tp}/tcp")
    for up in udp_ports:
        run_cmd(f"ufw allow {up}/udp")
    run_cmd("ufw allow 1:65535/udp")
    run_cmd("echo 'y' | ufw enable")

    # 3. Installing Xray Core
    print(f"{C}Installing Xray Core (VLESS/VMess/Trojan/gRPC)...{W}")
    run_cmd("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")

    # 4. Starting BadVPN for Gaming
    run_cmd("wget -O /usr/bin/badvpn-udpgw https://github.com/ambrop72/badvpn/raw/master/udpgw/badvpn-udpgw && chmod +x /usr/bin/badvpn-udpgw")
    run_cmd("screen -dmS badvpn badvpn-udpgw --listen-addr 127.0.0.1:7300")

    print(f"{G}All Services Installed Successfully!{W}")
    time.sleep(2)

def main_menu():
    while True:
        banner()
        print(f"{G}[01]{W} Setup Ultimate Services (Protocols & Ports)")
        print(f"{G}[02]{W} Create User (SSH/Vmess/Vless/Trojan)")
        print(f"{G}[03]{W} Install SSL Certificate (Domain)")
        print(f"{G}[04]{W} Run Speedtest")
        print(f"{G}[05]{W} Check System Resources")
        print(f"{R}[00]{W} Exit")
        print(f"{B}--------------------------------------------------{W}")
        
        choice = input(f"{C}Select an option: {W}")

        if choice == '1' or choice == '01':
            setup_all_services()
        elif choice == '2' or choice == '02':
            user = input("Enter username: ")
            pw = input("Enter password: ")
            run_cmd(f"useradd -e `date -d '30 days' +'%Y-%m-%d'` -s /bin/false -M {user}")
            run_cmd(f"echo '{user}:{pw}' | chpasswd")
            print(f"{G}User {user} created for 30 days!{W}")
            time.sleep(2)
        elif choice == '3' or choice == '03':
            domain = input("Enter your Domain: ")
            run_cmd("curl https://get.acme.sh | sh")
            run_cmd(f"~/.acme.sh/acme.sh --issue -d {domain} --standalone")
            input(f"\n{G}SSL process finished. Press Enter...{W}")
        elif choice == '4' or choice == '04':
            run_cmd("curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -")
            input(f"\n{G}Press Enter...{W}")
        elif choice == '5' or choice == '05':
            run_cmd("top -n 1 -b | head -n 15")
            input(f"\n{G}Press Enter...{W}")
        elif choice == '0' or choice == '00':
            print(f"{Y}Goodbye!{W}")
            break
