import os
import subprocess
import sys
import time

# --- Color Definitions ---
G = "\033[92m"  # GREEN
Y = "\033[93m"  # YELLOW
R = "\033[91m"  # RED
B = "\033[94m"  # BLUE
C = "\033[96m"  # CYAN
W = "\033[0m"   # RESET

def get_ip():
    """Fetch the server IP address."""
    try:
        ip = subprocess.getoutput("hostname -I | cut -d' ' -f1")
        return ip
    except:
        return "Unknown"

def banner():
    """Display the professional header."""
    os.system('clear')
    server_ip = get_ip()
    print(f"{B}=================================================={W}")
    print(f"{C}          ZAKERIA PROJECT - ULTIMATE VPS         {W}")
    print(f"{Y}    IP: {server_ip} | Developed by: @zakeria90    {W}")
    print(f"{B}=================================================={W}")

def run_cmd(command):
    """Execute shell commands safely."""
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"{R}Error: {e}{W}")

def setup_ultimate_panel():
    banner()
    print(f"{R}[!] CRITICAL REQUIREMENT:{W}")
    domain = input(f"{Y}Please enter your Domain (Pointed to this IP): {W}")
    
    if not domain:
        print(f"{R}Error: Domain is mandatory to proceed!{W}")
        time.sleep(2)
        return

    print(f"{G}>>> Starting Installation for: {domain}{W}")
    time.sleep(1)

    # 1. System Update & Tools Installation
    print(f"{C}Installing Core Tools (Nginx, SSLH, Dropbear, Socat)...{W}")
    run_cmd("apt update && apt install -y nginx stunnel4 sslh screen socat ufw dropbear curl python3-pip")

    # 2. SSL Certificate Generation & Permanent Installation
    print(f"{C}Generating SSL Certificate via Acme.sh...{W}")
    run_cmd("curl https://get.acme.sh | sh")
    # Issue Certificate
    run_cmd(f"~/.acme.sh/acme.sh --issue -d {domain} --standalone --force")
    # Permanent Path Installation (The Gold Tip)
    run_cmd("mkdir -p /etc/zakeria-ssl")
    run_cmd(f"~/.acme.sh/acme.sh --install-cert -d {domain} --fullchain-file /etc/zakeria-ssl/fullchain.pem --key-file /etc/zakeria-ssl/privkey.pem")
    print(f"{G}SSL installed at: /etc/zakeria-ssl/{W}")

    # 3. Comprehensive Firewall Configuration (TCP & UDP)
    print(f"{C}Configuring Advanced Firewall Ports...{W}")
    tcp_ports = ["80", "443", "8080", "8443", "8880", "8062", "8000", "9443", "2082", "3303", "109", "111", "69", "53"]
    udp_ports = ["7300", "5300", "5353", "53"]
    
    for tp in tcp_ports:
        run_cmd(f"ufw allow {tp}/tcp")
    for up in udp_ports:
        run_cmd(f"ufw allow {up}/udp")
    
    run_cmd("ufw allow 1:65535/udp") # Global UDP for Custom Protocols
    run_cmd("echo 'y' | ufw enable")

    # 4. Xray Core Installation (VLESS/VMess/Trojan/gRPC)
    print(f"{C}Installing Xray Official Core...{W}")
    run_cmd("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")

    # 5. Gaming Support (BadVPN UDPGW 7300)
    print(f"{C}Setting up BadVPN for Gaming...{W}")
    run_cmd("wget -O /usr/bin/badvpn-udpgw https://github.com/ambrop72/badvpn/raw/master/udpgw/badvpn-udpgw && chmod +x /usr/bin/badvpn-udpgw")
    run_cmd("screen -dmS badvpn badvpn-udpgw --listen-addr 127.0.0.1:7300")

    print(f"\n{G}SUCCESS! ZAKERIA PROJECT is fully deployed.{W}")
    print(f"{Y}Domain: {domain} | Ports: All Active{W}")
    input("\nPress Enter to return to menu...")

def main_menu():
    while True:
        banner()
        print(f"{G}[01]{W} Full Installation (Domain Required)")
        print(f"{G}[02]{W} Create SSH/V2Ray User (30 Days)")
        print(f"{G}[03]{W} Renew SSL Certificate")
        print(f"{G}[04]{W} Network Speedtest")
        print(f"{G}[05]{W} System Resource Monitor")
        print(f"{R}[00]{W} Exit")
        print(f"{B}--------------------------------------------------{W}")
        
        choice = input(f"{C}Select an option: {W}")

        if choice == '1' or choice == '01':
            setup_ultimate_panel()
        elif choice == '2' or choice == '02':
            user = input("Enter Username: ")
            pw = input("Enter Password: ")
            run_cmd(f"useradd -e `date -d '30 days' +'%Y-%m-%d'` -s /bin/false -M {user}")
            run_cmd(f"echo '{user}:{pw}' | chpasswd")
            print(f"{G}User {user} created successfully!{W}")
            time.sleep(2)
        elif choice == '3' or choice == '03':
            print(f"{Y}Renewing SSL certificates...{W}")
            run_cmd("~/.acme.sh/acme.sh --cron")
            time.sleep(2)
        elif choice == '4' or choice == '04':
            run_cmd("curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -")
            input(f"\n{G}Press Enter to return...{W}")
        elif choice == '5' or choice == '05':
            banner()
            run_cmd("top -n 1 -b | head -n 15")
            input(f"\n{G}Press Enter to return...{W}")
        elif choice == '0' or choice == '00':
            print(f"{Y}Thank you for using Zakeria Project. Goodbye!{W}")
            break
        else:
            print(f"{R}Invalid selection!{W}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
