import subprocess
import re
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_devices():
    """Получает список устройств через ARP-таблицу."""
    try:
        # Запускаем команду arp -a (выводит все известные устройства в сети)
        result = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            encoding="cp866", # Кодировка для русского Windows
            errors="ignore"
        )
        
        output = result.stdout
        devices = []
        
        # Парсим строки вида: 192.168.0.1     14-2e-5e-ec-fd-44     динамический
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            
            # Ищем IP-адрес в начале строки
            ip_match = re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+([0-9a-fA-F\-]{17})', line)
            if ip_match:
                ip = ip_match.group(1)
                mac = ip_match.group(2).upper().replace('-', ':')
                
                # Пропускаем broadcast и multicast адреса
                if ip.startswith("224.") or ip.startswith("239.") or ip.endswith(".255"):
                    continue
                    
                devices.append({"ip": ip, "mac": mac})
                
        # Убираем дубликаты (если есть)
        unique_devices = []
        seen_ips = set()
        for dev in devices:
            if dev['ip'] not in seen_ips:
                unique_devices.append(dev)
                seen_ips.add(dev['ip'])
                
        # Сортируем по последнему октету IP (чтобы было по порядку)
        unique_devices.sort(key=lambda x: int(x['ip'].split('.')[-1]))
        
        return unique_devices
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def run_scanner():
    clear_screen()
    print("=" * 65)
    print("   СКАНИРОВАНИЕ ЛОКАЛЬНОЙ СЕТИ (ARP-ТАБЛИЦА)")
    print("=" * 65)
    
    print("\nСканируем... (это займет пару секунд)")
    time.sleep(1)
    
    devices = get_devices()
    
    if not devices:
        print("\n❌ Не удалось найти устройства. Попробуй запустить от имени администратора.")
        return
        
    print(f"\nНайдено устройств: {len(devices)}\n")
    
    print(f"{'IP-адрес':<16} | {'MAC-адрес':<20} | {'Вендор (по MAC)':<20}")
    print("-" * 65)
    
    for dev in devices:
        ip = dev['ip']
        mac = dev['mac']
        
        # Пытаемся угадать производителя по первым 3 байтам MAC (OUI)
        # (Это не точно, но для популярных брендов работает)
        vendor = "Неизвестно"
        prefix = mac[:8]
        if prefix.startswith("14:2E:5E") or prefix.startswith("00:1A:2B"):
            vendor = "TP-Link"
        elif prefix.startswith("D8:E2:DF") or prefix.startswith("00:1A:2B"):
            vendor = "Xiaomi"
        elif prefix.startswith("00:1A:2B") or prefix.startswith("BC:5F:F4"):
            vendor = "ASUS"
        elif prefix.startswith("00:50:56") or prefix.startswith("00:0C:29"):
            vendor = "VMware"
            
        print(f"{ip:<16} | {mac:<20} | {vendor:<20}")

def main():
    while True:
        run_scanner()
        
        print("\n" + "=" * 50)
        print("Что будешь делать дальше?")
        print("1. Сканировать снова (обновить список)")
        print("2. Выйти")
        
        choice = input("\nТвой выбор (1-2): ")
        
        if choice == '2':
            print("\nВыход из сканера сети.")
            time.sleep(1)
            break

if __name__ == "__main__":
    main()