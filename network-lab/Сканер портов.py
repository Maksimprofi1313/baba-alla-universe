import socket
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_port(ip, port, timeout=0.5):
    """Пытается подключиться к порту. Если получается — порт открыт."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except Exception:
        return False

def run_scanner():
    clear_screen()
    print("=" * 50)
    print("   СКАНЕР ПОРТОВ (ТОЛЬКО ДЛЯ СВОИХ УСТРОЙСТВ!)")
    print("=" * 50)
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"\nТвой локальный IP: {local_ip}")
    except Exception:
        local_ip = "127.0.0.1"
        print(f"\nНе удалось определить IP. Используем: {local_ip}")

    target_ip = input("\nВведи IP для сканирования (Enter - свой IP): ").strip()
    if not target_ip:
        target_ip = local_ip

    print(f"\nСканируем {target_ip}...")
    
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP (Веб)", 110: "POP3", 135: "RPC", 139: "NetBIOS",
        443: "HTTPS", 445: "SMB (Сетевые папки)", 3306: "MySQL",
        3389: "RDP (Удаленный рабочий стол)", 8080: "HTTP-прокси",
    }

    open_ports = []
    
    for port, service in common_ports.items():
        print(f"Проверяем порт {port} ({service})...", end="", flush=True)
        if scan_port(target_ip, port):
            print(" [ОТКРЫТ]")
            open_ports.append((port, service))
        else:
            print(" [закрыт]")
        time.sleep(0.05)

    print("\n" + "=" * 50)
    if open_ports:
        print("Найдены открытые порты:")
        for port, service in open_ports:
            print(f"  ⚠️ Порт {port} ({service}) — ОТКРЫТ")
    else:
        print("✅ Все проверенные порты закрыты. Отлично!")

def main():
    while True:
        run_scanner()
        
        print("\n" + "=" * 50)
        print("Что будешь делать дальше?")
        print("1. Сканировать другой IP (или этот же заново)")
        print("2. Выйти")
        
        choice = input("\nТвой выбор (1-2): ")
        
        if choice == '2':
            print("\nВыход из сканера. Будь в безопасности!")
            time.sleep(1)
            break

if __name__ == "__main__":
    main()