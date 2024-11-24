import json
from pprint import pprint

# Завантаження JSON-файлу
with open('candlestick.json') as file:
    data = json.load(file)

# Перегляд структури JSON як текст
for i in data:
    print(data[i])

# Перегляд структури JSON як json
pprint(data)
