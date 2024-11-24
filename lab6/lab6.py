import os
import random
import shutil
from datetime import datetime, timedelta


def generate_test_files(directory):
    """
    Функція для генерації файлів різного типу
    :param directory:
    :return:
    """
    os.makedirs(directory, exist_ok=True)
    extensions = ['txt', 'py', 'jpg', 'json', 'pdf', 'docx', 'png']

    for i in range(1, 13):
        ext = random.choice(extensions)
        filepath = os.path.join(directory, f"test_file_{i}.{ext}")
        with open(filepath, 'w') as f:
            f.write(f"Test file {i} with extension {ext}")

        mod_time = datetime.now() - timedelta(days=random.randint(1, 30))
        os.utime(filepath, (mod_time.timestamp(), mod_time.timestamp()))


def find_oldest_newest_files(directory):
    """
    Завдання 1: Знаходимо найстаріші та найновіші файли
    :param directory:
    :return:
    """
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort(key=lambda x: os.path.getctime(x))

    print("Найстаріші файли:")
    for file in files[:2]:
        print(f"{file} - {datetime.fromtimestamp(os.path.getctime(file))}")

    print("\nНайновіші файли:")
    for file in files[-2:]:
        print(f"{file} - {datetime.fromtimestamp(os.path.getctime(file))}")


def find_duplicates(dir1, dir2):
    """
    Завдання 2: Пошук дубльованих файлів у двох папках
    :param dir1:
    :param dir2:
    :return:
    """
    files1 = {f: os.path.getsize(os.path.join(dir1, f)) for f in os.listdir(dir1) if
              os.path.isfile(os.path.join(dir1, f))}
    files2 = {f: os.path.getsize(os.path.join(dir2, f)) for f in os.listdir(dir2) if
              os.path.isfile(os.path.join(dir2, f))}

    duplicates = [(f, size) for f, size in files1.items() if f in files2 and files2[f] == size]

    print("Знайдено дублікати:")
    for f, size in duplicates:
        print(f"Файл: {f}, Розмір: {size} байт")


def filter_files_by_extension(directory, extensions):
    """
    Завдання 3: Перевірка типу файлів і виведення загального списку файлів
    :param directory:
    :param file_types:
    :return:
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.split('.')[-1] in extensions:
                print(os.path.join(root, file))


def move_files_by_type(directory):
    """
    Завдання 4: Переміщення файлів у окремі папки за типами
    :param directory:
    :return:
    """
    folder_mapping = {
        'json': 'JSON_Files',
        'png': 'Images',
        'pdf': 'Docs',
        'docx': 'Docs'
    }

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            ext = file.split('.')[-1]
            if ext in folder_mapping:
                target_dir = os.path.join(directory, folder_mapping[ext])
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(target_dir, file))
                print(f"Файл {file} переміщено до {target_dir}")


if __name__ == '__main__':
    # Генерація файлів та запуск завдань
    base_dir = "test_directory"
    second_dir = "test_directory_2"

    # Генерація файлів у двох папках
    generate_test_files(base_dir)
    generate_test_files(second_dir)

    print("Завдання 1:")
    find_oldest_newest_files(base_dir)

    print("\nЗавдання 2:")
    find_duplicates(base_dir, second_dir)

    print("\nЗавдання 3:")
    filter_files_by_extension(base_dir, ['docx', 'py', 'jpg', 'json',])

    print("\nЗавдання 4:")
    move_files_by_type(base_dir)
