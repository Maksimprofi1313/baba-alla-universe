import os
import time
import random
import sys

# Символы для матрицы (японские катаканы, цифры и латиница)
chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def matrix_rain():
    clear_screen()
    
    # Настройки
    width = 80  # Ширина экрана
    height = 25 # Высота экрана (для консоли)
    
    # Создаем списки для колонок (позиция капли в каждой колонке)
    drops = [random.randint(0, height) for _ in range(width)]
    
    try:
        while True:
            # Создаем пустой экран (матрицу символов)
            screen = [[' ' for _ in range(width)] for _ in range(height)]
            
            # Заполняем экран
            for x in range(width):
                # В каждой колонке ставим символ на позицию капли
                y = drops[x]
                if 0 <= y < height:
                    screen[y][x] = random.choice(chars)
                    
                # Также добавляем "хвост" (символы выше капли, но тусклее)
                # (В консоли нельзя сделать цвет, поэтому просто символы)
                for i in range(1, 4):
                    if 0 <= y - i < height:
                        screen[y - i][x] = random.choice(chars)
                
                # Двигаем каплю вниз
                drops[x] += 1
                
                # Если капля упала за экран, сбрасываем её наверх (случайно)
                if drops[x] > height + random.randint(0, 10):
                    drops[x] = 0
                    
            # Выводим экран
            # Используем sys.stdout.write для быстрого вывода без переносов
            output = "\n".join("".join(row) for row in screen)
            sys.stdout.write("\033[H") # Курсор в начало
            sys.stdout.write(output)
            sys.stdout.flush()
            
            # Задержка (чем меньше, тем быстрее)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nМатрица остановлена. Добро пожаловать в реальный мир.")

if __name__ == "__main__":
    matrix_rain()