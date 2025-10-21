# Импортируем наш модуль
import utils

def main():
    print("Добро пожаловать в демо-программу!")
    
    # Используем функцию из модуля
    radius = 5
    area = utils.calculate_circle_area(radius)
    print(f"Площадь круга с радиусом {radius} = {area:.2f}")
    
    # Текущее время
    print("Текущее время:", utils.get_current_time())
    
    # Проверка простых чисел
    numbers = [2, 3, 4, 17, 25, 29]
    print("\nПроверка простых чисел:")
    for num in numbers:
        status = "простое" if utils.is_prime(num) else "не простое"
        print(f"{num} — {status}")

# Точка входа в программу
if __name__ == "__main__":
    main()