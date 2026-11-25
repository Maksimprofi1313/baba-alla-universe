import ipaddress
import socket
import time
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def scan_port(ip, port, timeout=0.5):
    """Проверяет TCP-порт указанного локального/частного адреса."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((ip, port)) == 0
    except OSError:
        return False

def run_scanner():
    clear_screen()
    print("=" * 50)
    print("   СКАНЕР ПОРТОВ (ЛОКАЛЬНАЯ ЛАБОРАТОРИЯ)")
    print("=" * 50)
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except OSError:
        local_ip = "127.0.0.1"
    print(f"\nТвой локальный IP: {local_ip}")
    target_ip = input("Введи IP своего устройства (Enter — localhost): ").strip() or "127.0.0.1"
    try:
        address = ipaddress.ip_address(target_ip)
    except ValueError:
        print("Некорректный IP-адрес.")
        return
    if not (address.is_private or address.is_loopback or address.is_link_local):
        print("Разрешены только loopback, частные и link-local адреса.")
        return

    print(f"\nПроверяем ограниченный список портов на {address}...")
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS",
        443: "HTTPS", 445: "SMB", 3306: "MySQL",
        3389: "RDP", 8080: "HTTP alternate",
    }
    open_ports = []
    for port, service in common_ports.items():
        print(f"Проверяем {port} ({service})...", end="", flush=True)
        if scan_port(str(address), port):
            print(" [ОТКРЫТ]")
            open_ports.append((port, service))
        else:
            print(" [закрыт]")
        time.sleep(0.05)

    print("\n" + "=" * 50)
    if open_ports:
        print("Открытые порты:")
        for port, service in open_ports:
            print(f"  {port} ({service})")
    else:
        print("Открытые порты не обнаружены.")

def main():
    while True:
        run_scanner()
        print("\n1. Проверить ещё раз")
        print("2. Выйти")
        if input("\nТвой выбор (1-2): ").strip() == "2":
            print("Выход из сканера.")
            break

if __name__ == "__main__":
    main()
