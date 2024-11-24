import subprocess
import time


def main():
    filename = "data.txt"
    data = [34, 51, 67, 23, 45]
    coefficient = 2.5  # Коефіцієнт для множення

    # Записуємо початкові дані у файл
    with open(filename, "w") as f:
        f.write(" ".join(map(str, data)) + "\n")
    print(f"Записано {data} у файл {filename}.")

    # Запускаємо Go-програму як дочірній процес
    print("Запуск Go-програми для множення...")
    subprocess.run(["multiplier.exe", filename, str(coefficient)])

    # Читання результату після завершення Go-програми
    with open(filename, "r") as f:
        result = list(map(float, f.readline().split()))
    print(f"Отримано результат: {result}")

if __name__ == "__main__":
    main()
