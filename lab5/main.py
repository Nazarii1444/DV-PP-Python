import json
import random

from customQueue import CustomQueue, CustomDeclaration
from typing import List


def generate_declarations(count: int) -> List[CustomDeclaration]:
    vehicle_types = ['Volvo', 'Mercedes', 'MAN', 'Scania', 'DAF']
    cities = [
        ('Poland', 'Wroclaw'), ('Німеччина', 'Берлін'), ('Франція', 'Париж'),
        ('Україна', 'Київ'), ('Україна', 'Вінниця'), ('Україна', 'Одеса')
    ]
    products = [
        ('Техніка', 50000), ('Меблі', 30000), ('Текстиль', 20000),
        ('Продукти', 15000), ('Одяг', 25000), ('Автомобілі', 80000),
        ('Хімікати', 60000), ('Електроніка', 70000), ('Ліки', 40000),
        ('Будівельні матеріали', 35000), ('Папір', 5000), ('Мінерали', 9000)
    ]

    dangerous_products = ['Наркотики', 'Вибухівка', 'Динаміт', 'Зброя', 'Міни']
    owners = ['Green Day Company', 'Logistic LLC', 'Transport Ltd.', 'Fast Cargo']
    declarations = []

    for i in range(count):
        vehicle = random.choice(vehicle_types)
        id = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000, 9999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        owner = random.choice(owners)
        date = f"{random.randint(2020, 2023)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}"
        from_, to = random.sample(cities, 2)

        product_count = random.randint(1, 3)  # Від 1 до 3 продуктів
        product_list = random.sample(products + [(random.choice(dangerous_products), random.randint(1000, 20000))],
                                     product_count)
        contract_of_carriage = random.choice([True, False])

        declaration = CustomDeclaration(
            vehicle=vehicle,
            id=id,
            owner=owner,
            date=date,
            from_=from_,
            to=to,
            products=product_list,
            contract_of_carriage=contract_of_carriage
        )
        declarations.append(declaration)

    return declarations


def save_declarations_to_json(declarations: List[CustomDeclaration], filename: str):
    declarations_dicts = [declaration.__dict__ for declaration in declarations]

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(declarations_dicts, f, ensure_ascii=False, indent=4)

    print(f"Декларації успішно збережені у файл {filename}")


def run_scenario():
    """Run a customs control scenario demonstrating various queue operations."""
    with open('declarations.json', 'r', encoding='utf-8') as f:
        declarations_data = json.load(f)

    general_queue = CustomQueue()
    green_lane_queue = CustomQueue()

    # Create declarations from loaded data
    declarations = [
        CustomDeclaration(
            vehicle=decl["vehicle"],
            id=decl["id"],
            owner=decl["owner"],
            date=decl["date"],
            from_=(decl["from_"][0], decl["from_"][1]),
            to=(decl["to"][0], decl["to"][1]),
            products=[(p[0], p[1]) for p in decl["products"]],
            contract_of_carriage=decl["contract_of_carriage"]
        ) for decl in declarations_data
    ]

    # Add vehicles to the general queue
    print("\nДодавання авто до загальної черги:")
    for declaration in declarations:
        general_queue.add_to_queue(declaration, 'general')

    # Display the current state of the general queue
    print("\nПоточний стан загальної черги:")
    general_queue.display_queue()

    # Transfer a vehicle to the green lane queue
    print("\nПереміщення авто до зеленої черги:")
    general_queue.transfer_to_another_queue(green_lane_queue)

    # Check for dangerous goods
    dangerous_goods = ["Наркотики", "Динаміт"]
    print("\nПеревірка на наявність небезпечних товарів:")
    general_queue.check_dangerous_goods(dangerous_goods)

    # Display the most expensive product in the queue
    print("\nАвто з найбільш цінним товаром:")
    general_queue.vehicle_with_most_expensive_product()

    # Display the list of vehicles carrying a specific product
    print("\nПерелік авто, які везуть електроніку:")
    general_queue.list_vehicles_with_product("Електроніка")

    # Remove a vehicle from the queue
    print("\nВидалення авто з черги (немає дозволу):")
    general_queue.remove_vehicle("L4683J")

    # Summary of all products and their total value
    print("\nПідсумок товарів та їх загальної вартості:")
    general_queue.product_summary()

    # List vehicles heading to Odessa
    print("\nПерелік авто, які прямують до Одеси:")
    general_queue.vehicles_to_odessa()

    # Finish inspection of a vehicle
    print("\nЗавершення огляду авто:")
    green_lane_queue.finish_inspection()

    # Display the current state of both queues
    print("\nПоточний стан зеленої черги:")
    green_lane_queue.display_queue()

    print("\nПоточний стан загальної черги:")
    general_queue.display_queue()


if __name__ == "__main__":
    run_scenario()
