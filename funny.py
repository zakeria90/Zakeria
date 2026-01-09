import os
import subprocess
import sys

# Color definitions for a professional terminal look
G = "\033[92m"  # GREEN
Y = "\033[93m"  # YELLOW
R = "\033[91m"  # RED
B = "\033[94m"  # BLUE
C = "\033[96m"  # CYAN
W = "\033[0m"   # WHITE/RESET

def banner():
    os.system('clear')
    print(f"{B}=================================================={W}")
    print(f"{C}          ZAKERIA PROJECT - VPS MANAGER          {W}")
    print(f"{Y}       Developed by: @zakeria90 | Ver: 1.0       {W}")
    print(f"{B}=================================================={W}")

def run_cmd(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"{R}Error executing command: {e}{W}")

def main_menu():
    while True:
        banner()
        print(f"{G}[01]{W} Update & Optimize System")
        print(f"{G}[02]{W} Install Xray (VLESS/VMess/Trojan)")
        print(f"{G}[03]{W} Create SSH User (Login)")
        print(f"{G}[04]{W} Install BadVPN (UDP for Gaming)")
        print(f"{G}[05]{W} Speedtest VPS")
        print(f"{G}[06]{W} Check System Status (RAM/CPU)")
        print(f"{R}[00]{W} Exit")
        print(f"{B}--------------------------------------------------{W}")
        
        choice = input(f"{C}Select an option: {W}")

        if choice == '1' or choice == '01':
            print(f"{Y}Updating system...{W}")
            run_cmd("apt update && apt upgrade -y")
        elif choice == '2' or choice == '02':
            run_cmd("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")
        elif choice == '3' or choice == '03':
            user = input("Enter new username: ")
            pw = input("Enter password: ")
            run_cmd(f"useradd -e `date -d '30 days' +'%Y-%m-%d'` -s /bin/false -M {user}")
            run_cmd(f"echo '{user}:{pw}' | chpasswd")
            print(f"{G}User {user} created successfully for 30 days!{W}")
            input("Press Enter to continue...")
        elif choice == '4' or choice == '04':
            print(f"{Y}Installing BadVPN...{W}")
            run_cmd("wget -O /usr/bin/badvpn-udpgw https://github.com/ambrop72/badvpn/raw/master/udpgw/badvpn-udpgw && chmod +x /usr/bin/badvpn-udpgw")
            run_cmd("screen -dmS badvpn badvpn-udpgw --listen-addr 127.0.0.1:7300")
            print(f"{G}BadVPN started on port 7300{W}")
            sleep(2)
        elif choice == '5' or choice == '05':
            run_cmd("curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -")
            input("Press Enter to continue...")
        elif choice == '6' or choice == '06':
            run_cmd("top")
        elif choice == '0' or choice == '00':
            print(f"{Y}Goodbye!{W}")
            break
        else:
            print(f"{R}Invalid selection!{W}")
            os.system("sleep 1")

if __name__ == "__main__":
    main_menu()
