def fibonacci():
    """Бесконечный генератор чисел Фибоначчи."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for i, val in enumerate(fib):
    if i >= 100:
        break
    print(val, end=" ")
