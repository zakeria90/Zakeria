import os
import subprocess
import sys
import time

# Color definitions for a professional terminal look
G = "\033[92m"  # GREEN
Y = "\033[93m"  # YELLOW
R = "\033[91m"  # RED
B = "\033[94m"  # BLUE
C = "\033[96m"  # CYAN
W = "\033[0m"   # WHITE/RESET

def get_ip():
    """Fetch the server IP address automatically."""
    try:
        ip = subprocess.getoutput("hostname -I | cut -d' ' -f1")
        return ip
    except:
        return "Unknown"

def banner():
    """Display the main header with server info."""
    os.system('clear')
    server_ip = get_ip()
    print(f"{B}=================================================={W}")
    print(f"{C}          ZAKERIA PROJECT - VPS MANAGER          {W}")
    print(f"{Y}    IP: {server_ip} | Developed by: @zakeria90    {W}")
    print(f"{B}=================================================={W}")

def run_cmd(command):
    """Execute shell commands safely."""
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"{R}Error executing command: {e}{W}")

def main_menu():
    while True:
        banner()
        print(f"{G}[01]{W} Update & Optimize System")
        print(f"{G}[02]{W} Install Xray Core (VLESS/VMess/Trojan)")
        print(f"{G}[03]{W} Create SSH User (30 Days)")
        print(f"{G}[04]{W} Enable Gaming Support (BadVPN UDP 7300)")
        print(f"{G}[05]{W} Run Speedtest (Network Speed)")
        print(f"{G}[06]{W} Check System Resources (RAM/CPU)")
        print(f"{R}[00]{W} Exit")
        print(f"{B}--------------------------------------------------{W}")
        
        choice = input(f"{C}Select an option: {W}")

        if choice == '1' or choice == '01':
            print(f"{Y}Updating system repositories...{W}")
            run_cmd("apt update && apt upgrade -y")
            input(f"\n{G}Update complete. Press Enter to return...{W}")
            
        elif choice == '2' or choice == '02':
            print(f"{Y}Installing Xray Official Core...{W}")
            run_cmd("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")
            time.sleep(2)
            
        elif choice == '3' or choice == '03':
            user = input("Enter username: ")
            pw = input("Enter password: ")
            run_cmd(f"useradd -e `date -d '30 days' +'%Y-%m-%d'` -s /bin/false -M {user}")
            run_cmd(f"echo '{user}:{pw}' | chpasswd")
            print(f"{G}User {user} created successfully!{W}")
            time.sleep(2)
            
        elif choice == '4' or choice == '04':
            print(f"{Y}Installing BadVPN for UDP redirection...{W}")
            run_cmd("wget -O /usr/bin/badvpn-udpgw https://github.com/ambrop72/badvpn/raw/master/udpgw/badvpn-udpgw && chmod +x /usr/bin/badvpn-udpgw")
            run_cmd("screen -dmS badvpn badvpn-udpgw --listen-addr 127.0.0.1:7300")
            print(f"{G}BadVPN is now running on port 7300!{W}")
            time.sleep(2)
            
        elif choice == '5' or choice == '05':
            print(f"{Y}Running Network Speedtest...{W}")
            run_cmd("curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -")
            input(f"\n{G}Press Enter to return...{W}")
            
        elif choice == '6' or choice == '06':
            banner()
            print(f"{C}System Resource Usage:{W}")
            run_cmd("top -n 1 -b | head -n 15")
            input(f"\n{G}Press Enter to return...{W}")
            
        elif choice == '0' or choice == '00':
            print(f"{Y}Exiting Zakeria Project. Goodbye!{W}")
            break
        else:
            print(f"{R}Invalid selection! Please try again.{W}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
