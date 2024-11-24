import json


def load_data(filename='candlestick.json'):
    """Завантаження даних з JSON-файлу"""
    with open(filename, 'r') as file:
        return json.load(file)


def calculate_average_close(data):
    """Розрахунок середньої ціни закриття"""
    close_prices = list(data['Close'].values())
    average_close = sum(close_prices) / len(close_prices)
    print("Середня ціна закриття:", average_close)
    return average_close


def find_max_price_change(data):
    """Визначення найбільшої зміни ціни протягом однієї години"""
    high_prices = data['High']
    low_prices = data['Low']
    max_change = 0
    max_change_time = None
    for i in high_prices.keys():
        change = high_prices[i] - low_prices[i]
        if change > max_change:
            max_change = change
            max_change_time = i
    print("Найбільша зміна ціни:", max_change, "час:", max_change_time)
    return max_change, max_change_time


def count_trends(data):
    """Визначення висхідних та низхідних тенденцій"""
    open_prices = data['Open']
    up_trend = down_trend = 0

    for i in open_prices.keys():
        if data['Close'][i] > open_prices[i]:
            up_trend += 1
        elif data['Close'][i] < open_prices[i]:
            down_trend += 1

    print("Кількість висхідних свічок:", up_trend)
    print("Кількість низхідних свічок:", down_trend)
    return up_trend, down_trend


def calculate_average_volume_by_trend(data):
    """
    Розраховує середній обсяг торгів для висхідних та низхідних свічок.
    Висхідні свічки мають ціну закриття вище за ціну відкриття, а низхідні — навпаики.
    """
    open_prices = data['Open']
    close_prices = data['Close']
    volumes = data['Volume']

    up_volume = []  # Обсяги торгів для висхідних свічок
    down_volume = []  # Обсяги торгів для низхідних свічок

    # Ітеруємося по свічках та збираємо обсяги для висхідних та низхідних свічок
    for i in open_prices.keys():
        if close_prices[i] > open_prices[i]:
            up_volume.append(volumes[i])
        elif close_prices[i] < open_prices[i]:
            down_volume.append(volumes[i])

    # Розрахунок середнього обсягу для висхідних та низхідних свічок
    average_up_volume = sum(up_volume) / len(up_volume) if up_volume else 0
    average_down_volume = sum(down_volume) / len(down_volume) if down_volume else 0

    print("Середній обсяг торгів для висхідних свічок:", average_up_volume)
    print("Середній обсяг торгів для низхідних свічок:", average_down_volume)

    return average_up_volume, average_down_volume


def find_most_stable_hour(data):
    """
    Знаходить годину з найменшою зміною ціни (різниця між найвищою і найнижчою цінами).
    Це дозволяє виявити період низької волатильності.
    """
    high_prices = data['High']
    low_prices = data['Low']
    min_change = float('inf')  # Ініціалізація мінімальної зміни
    min_change_time = None  # Ініціалізація часу з найменшою зміною

    # Ітеруємося по свічках та шукаємо мінімальну зміну
    for i in high_prices.keys():
        change = high_prices[i] - low_prices[i]
        if change < min_change:
            min_change = change
            min_change_time = i

    print("Найменша зміна ціни:", min_change, "час:", min_change_time)
    return min_change, min_change_time


def calculate_sma_trend(data, period=10):
    """
    Обчислює 10-періодне просте ковзне середнє (SMA) для ціни закриття.
    Визначає загальний напрямок тренду на основі зростання чи спаду SMA.
    """
    close_prices = list(data['Close'].values())
    sma = []  # Список для збереження значень SMA

    # Розрахунок 10-періодного SMA
    for i in range(len(close_prices) - period + 1):
        sma.append(sum(close_prices[i:i + period]) / period)

    # Підрахунок зростання і спадання SMA для визначення тренду
    up_trend = down_trend = 0
    for i in range(1, len(sma)):
        if sma[i] > sma[i - 1]:
            up_trend += 1
        elif sma[i] < sma[i - 1]:
            down_trend += 1

    # Визначення загального тренду
    trend = "Висхідний" if up_trend > down_trend else "Низхідний"

    print("Загальний напрямок тренду:", trend)
    return sma, trend


def find_extreme_close(data, N=20):
    """
    Знаходить максимальну і мінімальну ціну закриття за останні N свічок.
    Допомагає виявити локальні екстремуми на графіку цін.
    """
    close_prices = list(data['Close'].values())
    recent_closes = close_prices[-N:]  # Останні N значень ціни закриття

    max_close = max(recent_closes)
    min_close = min(recent_closes)

    print(f"Максимальна ціна закриття за останні {N} періодів:", max_close)
    print(f"Мінімальна ціна закриття за останні {N} періодів:", min_close)

    return max_close, min_close


if __name__ == "__main__":
    data = load_data()
    calculate_average_close(data)
    find_max_price_change(data)
    count_trends(data)
    calculate_average_volume_by_trend(data)
    find_most_stable_hour(data)
    calculate_sma_trend(data)
    find_extreme_close(data)
