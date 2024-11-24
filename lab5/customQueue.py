from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class CustomDeclaration:
    vehicle: str
    id: str
    owner: str
    date: str
    from_: Tuple[str, str]
    to: Tuple[str, str]
    products: List[Tuple[str, int]]
    contract_of_carriage: bool


class CustomQueue:
    def __init__(self):
        self._queue = []

    def is_empty(self):
        return len(self._queue) == 0

    # Базовий метод додавання елемента в чергу
    def enqueue(self, item):
        if isinstance(item, CustomDeclaration):
            self._queue.append(item)
        else:
            print("Невірний формат даних для додавання в чергу")

    # Базовий метод видалення елемента з черги
    def dequeue(self):
        if not self.is_empty():
            return self._queue.pop(0)
        else:
            print("Черга порожня")

    # Метод переміщення авто до іншої черги (пов'язаний зі змістом задачі)
    def move_to_other_queue(self, other_queue):
        if not self.is_empty():
            item = self.dequeue()
            other_queue.enqueue(item)
        else:
            print("Немає авто для переміщення")

    # Метод видалення авто з черги (пов'язаний зі змістом задачі)
    def remove_item(self, item):
        if item in self._queue:
            self._queue.remove(item)
        else:
            print("Цього авто немає в черзі")

    # Метод виведення черги (пов'язаний зі змістом задачі)
    def display_queue(self):
        for idx, item in enumerate(self._queue):
            print(f"{idx + 1}. {item.vehicle} - {item.id}")

    # Метод пошуку авто за ключем (пов'язаний зі змістом задачі)
    def find_item_by_key(self, key, value):
        return [item for item in self._queue if getattr(item, key) == value]

    # Засоби контролю та захисту: перевірка унікальності авто в черзі
    def is_unique(self, id):
        for item in self._queue:
            if item.id == id:
                print(f"Авто з номером {id} вже в черзі")
                return False
        return True

    # Засоби контролю: додавання з перевіркою
    def safe_enqueue(self, item):
        if self.is_unique(item.id):
            self.enqueue(item)
        else:
            print(f"Авто {item.vehicle} з номером {item.id} не може бути додано")

    # Контроль: видалення з захистом
    def safe_dequeue(self):
        if not self.is_empty():
            item = self.dequeue()
            print(f"Авто {item.vehicle} успішно пройшло митний огляд.")
        else:
            print("Немає авто в черзі для митного огляду")

    # Метод контролю: огляд авто на наявність небезпечних товарів
    def check_dangerous_goods(self, dangerous_goods):
        for item in self._queue:
            for product in item.products:
                if product[0] in dangerous_goods:
                    print(f"Попередження! Авто {item.vehicle} перевозить небезпечний товар: {product[0]}")

    def add_to_queue(self, vehicle: CustomDeclaration, queue_type: str):
        if queue_type == 'зелений коридор':
            # логіка для зеленої черги
            print(f"Авто {vehicle.vehicle} додано в зелений коридор.")
        else:
            # логіка для загальної черги
            self.safe_enqueue(vehicle)
            print(f"Авто {vehicle.vehicle} додано в загальну чергу.")

    # Операція: закінчити огляд і дозволити перетин кордону
    def finish_inspection(self):
        self.safe_dequeue()

    # Операція: перевести авто з однієї черги в іншу
    def transfer_to_another_queue(self, other_queue):
        self.move_to_other_queue(other_queue)
        print(f"Авто переміщено до іншої черги.")

    # Функція викреслює авто з черги (немає дозволу на перетин кордону)
    def remove_vehicle(self, id: str):
        vehicle = self.find_item_by_key('id', id)
        if vehicle:
            self.remove_item(vehicle[0])
            print(f"Авто {vehicle[0].vehicle} з номером {id} викреслено з черги.")

    # Функція складає перелік авто, які везуть вказаний товар
    def list_vehicles_with_product(self, product_name: str):
        vehicles = [item for item in self._queue if any(product[0] == product_name for product in item.products)]
        if vehicles:
            print(f"Авто, які везуть {product_name}:")
            for vehicle in vehicles:
                print(f"{vehicle.vehicle} - {vehicle.id}")
        else:
            print(f"Жодне авто не везе товар {product_name}.")

    # Функція повертає, яке авто має товар найбільшої вартості
    def vehicle_with_most_expensive_product(self):
        if not self.is_empty():
            most_expensive = max(self._queue, key=lambda item: max(product[1] for product in item.products))
            print(f"Авто {most_expensive.vehicle} з товаром найбільшої вартості.")
        else:
            print("Черга порожня")

    # Операція: таблиця товарів і цін (підсумок)
    def product_summary(self):
        summary = {}
        for item in self._queue:
            for product in item.products:
                if product[0] in summary:
                    summary[product[0]] += product[1]
                else:
                    summary[product[0]] = product[1]
        print("Таблиця товарів і цін:")
        for product, total_value in summary.items():
            print(f"{product}: {total_value}")

    # Операція: які авто прямують до Одеси
    def vehicles_to_odessa(self):
        vehicles = [item for item in self._queue if item.to[1] == 'Одеса']
        if vehicles:
            print("Авто, які прямують до Одеси:")
            for vehicle in vehicles:
                print(f"{vehicle.vehicle} - {vehicle.id}")
        else:
            print("Немає авто, які прямують до Одеси.")


