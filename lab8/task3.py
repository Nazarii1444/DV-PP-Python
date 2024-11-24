import os
import webbrowser

import requests


def download_and_save_xml(xml_file_url: str, output_filename: str):
    """Функція для завантаження та збереження XML-файлу."""
    try:
        print(f"Спроба завантаження XML-файлу з: {xml_file_url}")
        response = requests.get(xml_file_url)

        if response.ok:
            with open(output_filename, "wb") as file:
                file.write(response.content)
            print(f"XML-файл успішно збережено у файл: {output_filename}")
        else:
            print(f"Помилка завантаження. Статус відповіді: {response.status_code}")

    except requests.RequestException as error:
        print(f"Сталася помилка під час завантаження XML-файлу: {error}")


if __name__ == '__main__':
    xml_file_url = "http://feeds.bbci.co.uk/news/rss.xml"
    output_file = "bbc_news_data.xml"

    download_and_save_xml(xml_file_url, output_file)

    try:
        print("Спроба відкрити збережений XML-файл у браузері...")
        file_path = os.path.abspath(output_file)
        webbrowser.open(f'file://{file_path}')
    except Exception as open_error:
        print(f"Сталася помилка під час відкриття файлу: {open_error}")
