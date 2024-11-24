import xml.etree.ElementTree as ET


def display_all_titles():
    """Функція для відображення заголовків всіх новин"""
    print("Список заголовків новин:")
    for item in root.findall('.//item'):
        title = item.find('title').text
        print(f"- {title}")
    print()


def find_news_by_keyword(keyword):
    """Функція для пошуку новини за ключовими словами в заголовку"""
    print(f"Пошук новин за ключовим словом '{keyword}':")
    found = False
    for item in root.findall('.//item'):
        title = item.find('title').text
        if keyword.lower() in title.lower():
            description = item.find('description').text
            link = item.find('link').text
            print(f"\nЗаголовок: {title}\nОпис: {description}\nПосилання: {link}")
            found = True
    if not found:
        print("Новини за даним ключовим словом не знайдено.")
    print()


def list_unique_pub_dates():
    """Функція для виведення унікальних дат публікації новин"""
    unique_dates = set()
    for item in root.findall('.//item'):
        pub_date = item.find('pubDate').text
        unique_dates.add(pub_date)
    print("Унікальні дати публікацій:", unique_dates)
    print()


def count_news_by_date(date):
    """Функція для підрахунку кількості новин за день"""
    count = sum(1 for item in root.findall('.//item') if item.find('pubDate').text.startswith(date))
    print(f"Кількість новин за {date}: {count}")


if __name__ == '__main__':
    # Завантаження XML-файлу
    tree = ET.parse('bbc_news_data.xml')
    root = tree.getroot()

    print("display_all_titles()")
    display_all_titles()
    print()

    print("find_news_by_keyword('election')")
    find_news_by_keyword('election')
    print()

    print("list_unique_pub_dates()")
    list_unique_pub_dates()
    print()

    print("count_news_by_date('Tue, 05 Nov 2024')")
    count_news_by_date('Tue, 05 Nov 2024')
    print()