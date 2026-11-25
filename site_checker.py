import socket
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_site(host, port=443, timeout=3):
    """Проверяет, открывается ли сайт (подключается к 443 порту) и замеряет время."""
    try:
        # Замеряем время до подключения
        start_time = time.time()
        
        # Создаем сокет и пытаемся подключиться
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        
        # Получаем IP по доменному имени
        ip = socket.gethostbyname(host)
        
        # Пытаемся подключиться
        result = s.connect_ex((ip, port))
        s.close()
        
        end_time = time.time()
        ping_ms = (end_time - start_time) * 1000
        
        if result == 0:
            return True, ping_ms, ip
        else:
            return False, None, ip
            
    except socket.gaierror:
        return False, "DNS Error", None
    except socket.timeout:
        return False, "Timeout", None
    except Exception as e:
        return False, str(e), None

def run_checker():
    clear_screen()
    print("=" * 60)
    print("   ПРОВЕРКА ДОСТУПНОСТИ САЙТОВ (TCP 443)")
    print("=" * 60)
    
    # Список сайтов для проверки
    sites = [
        "youtube.com",
        "github.com",
        "store.steampowered.com",
        "ggsel.net",
        "yandex.ru",
        "google.com",
        "discord.com",
        "cloudflare.com"
    ]
    
    print(f"\nПроверяем {len(sites)} сайтов...\n")
    time.sleep(1)
    
    results = []
    
    for site in sites:
        print(f"Проверяем {site}...", end="", flush=True)
        
        is_up, ping, ip = check_site(site)
        
        if is_up:
            print(f" [OK] (IP: {ip}, {ping:.0f} ms)")
            results.append((site, True, ping))
        else:
            print(f" [ОШИБКА] ({ping})")
            results.append((site, False, ping))
            
        time.sleep(0.5) # Пауза между проверками
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    
    up_count = 0
    for site, is_up, ping in results:
        if is_up:
            up_count += 1
            print(f"✅ {site:<25} — Работает (пинг: {ping:.0f} ms)")
        else:
            print(f"❌ {site:<25} — Недоступен ({ping})")
            
    print("\n" + "=" * 60)
    print(f"Итог: {up_count} из {len(sites)} сайтов доступны.")
    
    if up_count < len(sites):
        print("⚠️ Некоторые сайты недоступны. Возможно, они заблокированы или лежат.")
    else:
        print("✅ Все сайты доступны. Интернет работает отлично!")

def main():
    while True:
        run_checker()
        
        print("\n" + "=" * 50)
        print("Что будешь делать дальше?")
        print("1. Проверить еще раз")
        print("2. Выйти")
        
        choice = input("\nТвой выбор (1-2): ")
        
        if choice == '2':
            print("\nВыход. Хорошего дня!")
            time.sleep(1)
            break

if __name__ == "__main__":
    main()