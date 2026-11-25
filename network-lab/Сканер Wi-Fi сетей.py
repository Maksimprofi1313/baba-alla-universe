import subprocess
import re
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_wifi():
    """Запускает netsh и парсит вывод."""
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=Bssid"],
            capture_output=True,
            text=True,
            encoding="cp866",
            errors="ignore"
        )
        
        output = result.stdout
        
        networks = []
        current_ssid = None
        current_auth = None
        current_signal = None
        
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            
            # Ищем SSID (SSID 1: Имя)
            if line.startswith("SSID"):
                # Берем всё после первого двоеточия
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_ssid = parts[1].strip()
                    
            # Ищем аутентификацию
            elif "Проверка подлинности" in line:
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_auth = parts[1].strip()
                    
            # Ищем сигнал (Сигнал: 38%)
            elif line.startswith("Сигнал") or line.startswith("Signal"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_signal = parts[1].strip()
                    
            # Конец блока сети (если нашли сигнал)
            if current_signal and current_ssid is not None:
                networks.append({
                    "ssid": current_ssid,
                    "auth": current_auth,
                    "signal": current_signal
                })
                current_ssid = None
                current_auth = None
                current_signal = None
                
        return networks, output
        
    except Exception as e:
        return [], f"Ошибка: {e}"

def run_scanner():
    clear_screen()
    print("=" * 60)
    print("   СКАНЕР WI-FI СЕТЕЙ (В РАДИУСЕ ДЕЙСТВИЯ)")
    print("=" * 60)
    
    print("\nСканируем эфир...")
    time.sleep(1)
    
    networks, raw_output = scan_wifi()
    
    if not networks:
        print("\n❌ Не удалось распознать сети. Вот что выдала система:")
        print("-" * 40)
        print(raw_output[:500])
        print("-" * 40)
        return
        
    print(f"\nНайдено сетей: {len(networks)}\n")
    
    # Сортируем по уровню сигнала
    def get_signal_percent(sig_str):
        match = re.search(r'(\d+)', sig_str)
        if match:
            return int(match.group(1))
        return 0
        
    networks.sort(key=lambda x: get_signal_percent(x['signal']), reverse=True)
    
    print(f"{'SSID':<30} | {'Сигнал':<10} | {'Защита':<20}")
    print("-" * 65)
    
    for net in networks:
        ssid = net['ssid'] if net['ssid'] else "[Скрытая]"
        signal = net['signal']
        auth = net['auth'] if net['auth'] else "Открытая"
        
        if auth == "Открытая" or "Open" in auth:
            auth = "⚠️ ОТКРЫТАЯ"
            
        print(f"{ssid:<30} | {signal:<10} | {auth:<20}")

def main():
    while True:
        run_scanner()
        
        print("\n" + "=" * 50)
        print("Что будешь делать дальше?")
        print("1. Сканировать снова")
        print("2. Выйти")
        
        choice = input("\nТвой выбор (1-2): ")
        
        if choice == '2':
            print("\nВыход.")
            time.sleep(1)
            break

if __name__ == "__main__":
    main()