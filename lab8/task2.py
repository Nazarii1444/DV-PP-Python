import os
import time
import webbrowser
import requests


def fetch_and_save_page(page_url: str, output_file: str):
    """Функція для завантаження веб-сторінки та збереження її у файл."""
    try:
        print(f"Завантаження сторінки за адресою: {page_url}")
        response = requests.get(page_url)

        if response.ok:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Сторінка успішно збережена у файл: {output_file}")
        else:
            print(f"Не вдалося завантажити сторінку. Статус: {response.status_code}")

    except requests.RequestException as error:
        print(f"Помилка під час завантаження: {error}")


if __name__ == '__main__':
    page_url = 'https://en.wikipedia.org/wiki/Self-organization'
    output_file = 'self_organization.html'

    fetch_and_save_page(page_url, output_file)
    time.sleep(5)

    try:
        print("Відкриття збереженої веб-сторінки у браузері...")
        file_path = os.path.abspath(output_file)
        webbrowser.open(f'file://{file_path}')
    except Exception as open_error:
        print(f"Помилка під час відкриття файлу: {open_error}")
