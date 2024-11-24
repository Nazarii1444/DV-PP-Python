import os
import subprocess
from datetime import datetime
import pandas as pd
import yfinance as yf
from data_collection import DataCollector


class DataCollector:
    def __init__(self):
        pass

    def fetch_data(self, symbol, start_date="2020-01-01", end_date=None):
        """
        Отримання фінансових даних з Yahoo Finance через бібліотеку yfinance.
        :param symbol: Символ акції (наприклад, AAPL).
        :param start_date: Дата початку (у форматі YYYY-MM-DD).
        :param end_date: Дата закінчення (у форматі YYYY-MM-DD, за замовчуванням сьогоднішній день).
        :return: Дані у форматі DataFrame.
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")

        try:
            data = yf.download(symbol, start=start_date, end=end_date)

            # Очищення зайвих рядків (якщо вони є)
            if "Adj Close" in data.columns:
                data = data[
                    ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']]  # Залишаємо тільки потрібні стовпці

            # Видалення зайвих рядків, які не містять корисних даних
            data.reset_index(inplace=True)
            data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S+00:00')  # Форматування дати

            return data
        except Exception as e:
            print(f"Помилка під час отримання даних: {e}")
            return None

    def save_data(self, data, file_path):
        """
        Збереження даних у файл CSV.
        :param data: Дані у форматі DataFrame.
        :param file_path: Шлях до файлу збереження.
        """
        try:
            data.to_csv(file_path, index=False)
            print(f"Дані збережено у файл: {file_path}")
        except IOError as e:
            print(f"Помилка збереження даних: {e}")

    def is_data_up_to_date(self, file_path):
        """
        Перевірка, чи є дані у файлі актуальними.
        :param file_path: Шлях до файлу даних.
        :return: True, якщо дані актуальні, інакше False.
        """
        try:
            data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
            last_date = data.index.max().strftime("%Y-%m-%d")
            today = datetime.now().strftime("%Y-%m-%d")
            return last_date == today
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return False


def load_csv_from_yf():
    # Ініціалізація об'єкта збору даних
    collector = DataCollector()

    # Шлях до збережених даних
    data_path = "financial_data.csv"

    # Перевірка наявності даних за поточний день
    if not os.path.exists(data_path) or not collector.is_data_up_to_date(data_path):
        print("Дані за поточний день відсутні або застарілі. Завантажую нові дані...")
        data = collector.fetch_data(symbol="AAPL", start_date="2020-01-01")
        if data is not None:
            collector.save_data(data, data_path)
            print("Дані успішно завантажені та збережені.")
    else:
        print("Дані за поточний день вже доступні.")

def run_exe(file_path: str):
    try:
        if not os.path.exists(file_path):
            print(f"Файл не знайдено: {file_path}")
            return

        subprocess.run(file_path, shell=True, check=True)
        print(f"Файл {file_path} успішно запущено.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при запуску файлу: {e}")
    except Exception as e:
        print(f"Невідома помилка: {e}")

def run_subprocess():
    print('Running subprocess')
    run_exe("ohlcv_chart.exe")
    print('Subprocess ended')

def main():
    # load_csv_from_yf()
    run_subprocess()

if __name__ == "__main__":
    main()
