import subprocess
import re
import os
import time

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_devices():
    """Получает список устройств из локальной ARP-таблицы."""
    try:
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True,
                                encoding="cp866" if os.name == "nt" else "utf-8",
                                errors="ignore", timeout=5)
        devices = []
        for line in result.stdout.splitlines():
            match = re.match(r"^(\d{1,3}(?:\.\d{1,3}){3})\s+([0-9a-fA-F\-]{17})", line.strip())
            if not match:
                continue
            ip, mac = match.group(1), match.group(2).upper().replace("-", ":")
            if ip.startswith(("224.", "239.")) or ip.endswith(".255"):
                continue
            devices.append({"ip": ip, "mac": mac})
        unique = {device["ip"]: device for device in devices}
        return sorted(unique.values(), key=lambda item: tuple(map(int, item["ip"].split("."))))
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"Ошибка чтения ARP-таблицы: {exc}")
        return []

def identify_vendor(mac):
    """Осторожная оценка по нескольким известным префиксам; это не гарантия."""
    prefix = mac.upper().replace("-", ":")[:8]
    known = {
        "14:2E:5E": "TP-Link",
        "D8:E2:DF": "Неизвестный производитель (префикс из исходного проекта)",
        "BC:5F:F4": "ASUS",
        "00:50:56": "VMware",
        "00:0C:29": "VMware",
    }
    return known.get(prefix, "Неизвестно")

def run_scanner():
    clear_screen()
    print("=" * 65)
    print("   СКАНИРОВАНИЕ ЛОКАЛЬНОЙ СЕТИ (ARP-ТАБЛИЦА)")
    print("=" * 65)
    print("\nЧитаем локальную ARP-таблицу...")
    time.sleep(1)
    devices = get_devices()
    if not devices:
        print("\nУстройства в ARP-таблице не найдены.")
        return
    print(f"\nНайдено записей: {len(devices)}\n")
    print(f"{'IP-адрес':<16} | {'MAC-адрес':<20} | {'Вендор (оценка)':<30}")
    print("-" * 75)
    for device in devices:
        print(f"{device['ip']:<16} | {device['mac']:<20} | {identify_vendor(device['mac']):<30}")

def main():
    while True:
        run_scanner()
        print("\n1. Обновить список")
        print("2. Выйти")
        if input("\nТвой выбор (1-2): ").strip() == "2":
            print("\nВыход из сканера сети.")
            break

if __name__ == "__main__":
    main()
