def add(x, y):
    """Функция сложения"""
    return x + y

def subtract(x, y):
    """Функция вычитания"""
    return x - y

def multiply(x, y):
    """Функция умножения"""
    return x * y

def divide(x, y):
    """Функция деления с проверкой деления на ноль"""
    if y == 0:
        return "Ошибка: Деление на ноль невозможно!"
    return x / y

def calculator():
    """Основная функция калькулятора, управляющая циклом."""
    print("=====================================")
    print("        🐍 Простой Калькулятор 🐍     ")
    print("=====================================")
    
    while True:
        print("\nВыберите операцию:")
        print("1. Сложение (+)")
        print("2. Вычитание (-)")
        print("3. Умножение (*)")
        print("4. Деление (/)")
        print("5. Выход")
        
        choice = input("Введите номер операции (1/2/3/4/5): ")
        
        if choice == '5':
            print("Спасибо за использование калькулятора! До свидания!")
            break
        
        if choice != '1' and choice != '2' and choice != '3' and choice != '4':
            print("⚠️ Пожалуйста, введите корректный номер операции.")
            continue

        try:
            # Получаем два числа от пользователя
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
        except ValueError:
            print("⚠️ Ошибка: Пожалуйста, вводите только числа.")
            continue

        # Выполнение операции в зависимости от выбора
        if choice == '1':
            result = add(num1, num2)
            print(f"\n✅ Результат: {num1} + {num2} = {result}")
        elif choice == '2':
            result = subtract(num1, num2)
            print(f"\n✅ Результат: {num1} - {num2} = {result}")
        elif choice == '3':
            result = multiply(num1, num2)
            print(f"\n✅ Результат: {num1} * {num2} = {result}")
        elif choice == '4':
            result = divide(num1, num2)
            print(f"\n✅ Результат: {num1} / {num2} = {result}")

# Запуск калькулятора
if __name__ == "__main__":
    calculator()
