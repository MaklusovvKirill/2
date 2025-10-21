import math
from datetime import datetime

def calculate_circle_area(radius):
    """Возвращает площадь круга по заданному радиусу."""
    if radius < 0:
        raise ValueError("Радиус не может быть отрицательным")
    return math.pi * radius ** 2

def get_current_time():
    """Возвращает текущую дату и время в читаемом формате."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_prime(n):
    """Проверяет, является ли число простым."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True