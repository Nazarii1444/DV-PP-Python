import subprocess
import time
import os


def main():
    print("main process - started")  # початок основного процесу

    # Визначення шляху до дочірнього процесу
    child_script = os.path.join(os.path.abspath('.'), 'sub_process.py')

    # Запуск дочірнього процесу асинхронно
    parprog = subprocess.Popen(["python", child_script])

    # Основний процес продовжує виконання
    time.sleep(2)  # затримка для демонстрації паралельного виконання
    print("main process - continue")  # продовження основного процесу

    # Перевіряємо, чи завершився дочірній процес
    print("subprocess finished ? ", parprog.poll())  # poll() повертає None, якщо процес ще працює

    # Завершення основного процесу
    print("main process - finished")
    parprog.wait()  # Очікуємо завершення дочірнього процесу перед виходом


if __name__ == "__main__":
    main()
