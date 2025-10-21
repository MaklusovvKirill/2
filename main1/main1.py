import utils

def main():
    print("Добро пожаловать в демо-программу!")
    
    radius = 5
    area = utils.calculate_circle_area(radius)
    print(f"Площадь круга с радиусом {radius} = {area:.2f}")
    
    print("Текущее время:", utils.get_current_time())
    
    numbers = [2, 3, 4, 17, 25, 29]
    print("\nПроверка простых чисел:")
    for num in numbers:
        status = "простое" if utils.is_prime(num) else "не простое"
        print(f"{num} — {status}")

if __name__ == "__main__":
    main()