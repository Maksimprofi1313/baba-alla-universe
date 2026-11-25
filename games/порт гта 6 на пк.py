import time
import os
import random
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """Печатает прогресс-бар."""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')

def port_gta6():
    clear_screen()
    print("=" * 60)
    print("   СИМУЛЯТОР ПОРТИРОВАНИЯ GTA 6 НА ПК")
    print("=" * 60)
    time.sleep(1)
    
    steps = [
        ("Скачиваем исходный код GTA 6 (утечка из Rockstar)...", 20),
        ("Расшифровываем файлы игры...", 15),
        ("Переписываем движок RAGE под DirectX 12...", 10),
        ("Адаптируем управление под клавиатуру и мышь...", 5),
        ("Оптимизируем графику для RTX 3060...", 15),
        ("Исправляем баги (их очень много)...", 30),
        ("Компилируем проект...", 5),
    ]
    
    total_time = sum(step[1] for step in steps)
    current_time = 0
    
    for step, duration in steps:
        print(f"\n[>] {step}")
        for i in range(duration):
            time.sleep(0.1) # Имитация работы
            current_time += 1
            print_progress(current_time, total_time, prefix='Прогресс:', suffix='Завершено', length=40)
            
    print("\n" + "=" * 60)
    print("✅ ПОРТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("=" * 60)
    time.sleep(1)
    
    print("\nЗапускаем GTA 6 на ПК...")
    time.sleep(2)
    
    # А вот и подвох
    print("\n❌ ОШИБКА: Не хватает видеопамяти!")
    print("❌ ОШИБКА: Видеокарта не найдена (она в ремонте).")
    print("❌ ОШИБКА: Rockstar подала в суд за пиратство.")
    print("\n💡 Вместо GTA 6 запускаем текстовый квест...")
    time.sleep(2)
    
    print("\nДобро пожаловать в текстовую GTA 6!")
    print("Ты в Лос-Сантосе. У тебя есть 100 рублей и ржавый велосипед.")
    print("Что будешь делать?")
    print("1. Украсть машину.")
    print("2. Ограбить магазин.")
    print("3. Пойти домой спать.")
    
    choice = input("\nТвой выбор (1-3): ")
    
    if choice == '1':
        print("\nТы пытаешься украсть машину, но она оказывается на ручной тормозе.")
        print("Полиция арестовала тебя. Игра окончена.")
    elif choice == '2':
        print("\nТы заходишь в магазин, но там сидит Баба Алла с бензопилой.")
        print("Она забирает твои 100 рублей и выгоняет тебя. Игра окончена.")
    else:
        print("\nТы идешь домой, ложишься спать и просыпаешься в 2026 году.")
        print("GTA 6 все еще не вышла. Игра окончена.")

if __name__ == "__main__":
    port_gta6()