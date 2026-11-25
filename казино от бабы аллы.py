import random
import time
import os

# Попробуем подключить звуки (работает только на Windows)
try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_sound(freq, duration):
    if HAS_SOUND:
        winsound.Beep(freq, duration)

def spin_roulette(bet, choice_type, choice_value):
    print("\nКрутим рулетку...", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
        play_sound(500, 50) # Звук тиканья
    print()
    
    number = random.randint(0, 36)
    
    # Определяем цвет (упрощенно: четные - черные, нечетные - красные, 0 - зеленый)
    if number == 0:
        color = "Зеленый"
    elif number % 2 == 0:
        color = "Черный"
    else:
        color = "Красный"
        
    print(f"🎲 Выпало число: {number} ({color})")
    
    win_amount = 0
    
    if choice_type == 'color':
        if choice_value == color:
            if color == "Зеленый":
                win_amount = bet * 14
                print("💥 ДЖЕКПОТ! ЗЕЛЕНЫЙ!")
            else:
                win_amount = bet * 2
                print(f"✅ Ты угадал цвет!")
    elif choice_type == 'number':
        if choice_value == number:
            win_amount = bet * 35
            print(f"🔥 НЕВЕРОЯТНО! Ты угадал число {number}!")
            
    if win_amount > 0:
        play_sound(1000, 200) # Звук победы
        print(f"💰 Ты выиграл {win_amount} фишек!")
        return win_amount
    else:
        play_sound(200, 300) # Звук проигрыша
        print("❌ Ты проиграл.")
        return 0

def main():
    balance = 1000
    name = input("Как тебя зовут, игрок? (Enter - Идионик): ").strip() or "Идионик"
    
    while balance > 0:
        clear_screen()
        print("=" * 45)
        print(f"🎰 КАЗИНО 'У БАБЫ АЛЛЫ' 🎰")
        print(f"👤 Игрок: {name} | 💰 Баланс: {balance} фишек")
        print("=" * 45)
        
        print("1. Ставка на ЦВЕТ (x2, Зеленый x14)")
        print("2. Ставка на ЧИСЛО (x35)")
        print("3. Выход")
        
        choice = input("\nТвой выбор (1-3): ")
        
        if choice == '3':
            print(f"\n{name}, ты забрал {balance} фишек и ушел. Баба Алла недовольна.")
            break
            
        if choice not in ['1', '2']:
            print("Неверный выбор.")
            time.sleep(1)
            continue
            
        try:
            bet = int(input(f"Сколько ставишь? (У тебя {balance}): "))
            if bet <= 0 or bet > balance:
                print("Неверная ставка.")
                time.sleep(1)
                continue
        except ValueError:
            print("Введи число.")
            time.sleep(1)
            continue
            
        balance -= bet
        
        if choice == '1':
            print("\nВыбери цвет:")
            print("1. Красный")
            print("2. Черный")
            print("3. Зеленый")
            c_choice = input("(1-3): ")
            colors = {'1': 'Красный', '2': 'Черный', '3': 'Зеленый'}
            if c_choice in colors:
                balance += spin_roulette(bet, 'color', colors[c_choice])
            else:
                print("Отмена.")
                balance += bet
        elif choice == '2':
            try:
                num_choice = int(input("Выбери число от 0 до 36: "))
                if 0 <= num_choice <= 36:
                    balance += spin_roulette(bet, 'number', num_choice)
                else:
                    print("Число вне диапазона. Отмена.")
                    balance += bet
            except ValueError:
                print("Введи число. Отмена.")
                balance += bet
                
        time.sleep(2)

    if balance <= 0:
        print("\n💀 Ты проиграл всё. Баба Алла забирает твою шубу из Понго и выставляет тебя на улицу.")

if __name__ == "__main__":
    main()