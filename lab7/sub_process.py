import time


def child_process():
    print("subprocess started")  # початок дочірнього процесу

    time.sleep(3)  # затримка для демонстрації паралельного виконання

    print("subprocess finished")  # завершення дочірнього процесу


if __name__ == "__main__":
    child_process()
