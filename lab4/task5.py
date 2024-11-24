from customstack import CustomStack


def iterative_hanoi(n, source, destination, auxiliary):
    """
    Ітеративне вирішення задачі Ханойських веж.
    Переміщує n дисків зі стрижня source на стрижень destination, використовуючи auxiliary.
    Повертає кількість переміщень.
    """
    total_moves = 2 ** n - 1  # Загальна кількість необхідних переміщень
    moves_made = 0

    # Якщо кількість дисків парна, міняємо цільовий і допоміжний стрижні місцями
    if n % 2 == 0:
        destination, auxiliary = auxiliary, destination

    # Ініціалізуємо стрижень source з n дисками
    for disk in range(n, 0, -1):
        source.push(disk)

    # Виконуємо ітераційні переміщення
    for move_number in range(1, total_moves + 1):
        if move_number % 3 == 1:
            moves_made += perform_move(source, destination)
        elif move_number % 3 == 2:
            moves_made += perform_move(source, auxiliary)
        elif move_number % 3 == 0:
            moves_made += perform_move(auxiliary, destination)

    return moves_made


def perform_move(from_rod, to_rod):
    """
    Виконує переміщення верхнього диска з from_rod на to_rod, або навпаки, залежно від стану.
    Повертає 1, якщо переміщення відбулося.
    """
    if from_rod.get_size() == 0:
        # Переміщуємо диск з to_rod на from_rod, якщо from_rod порожній
        disk = to_rod.pop()
        from_rod.push(disk)
        print(f"Move disk {disk} from {to_rod.name} to {from_rod.name}")
    elif to_rod.get_size() == 0:
        # Переміщуємо диск з from_rod на to_rod, якщо to_rod порожній
        disk = from_rod.pop()
        to_rod.push(disk)
        print(f"Move disk {disk} from {from_rod.name} to {to_rod.name}")
    else:
        # Переміщуємо диск залежно від розмірів верхніх дисків на обох стрижнях
        if from_rod.peek() < to_rod.peek():
            disk = from_rod.pop()
            to_rod.push(disk)
            print(f"Move disk {disk} from {from_rod.name} to {to_rod.name}")
        else:
            disk = to_rod.pop()
            from_rod.push(disk)
            print(f"Move disk {disk} from {to_rod.name} to {from_rod.name}")

    return 1


def run_hanoi_simulation(n):
    """Ініціалізує стрижні та виконує ітеративне рішення задачі Ханойських веж для n дисків"""
    source = CustomStack("A")
    destination = CustomStack("C")
    auxiliary = CustomStack("B")

    print(f"\nStarting configuration for {n} disks:")
    moves = iterative_hanoi(n, source, destination, auxiliary)
    print(f"\nCompleted in {moves} moves for {n} disks.\n")


def sort_random_disks(source, destination, auxiliary):
    """
    Сортує диски з довільного порядку на стрижні source до впорядкованого на стрижні destination,
    використовуючи auxiliary.
    """
    while source.get_size() > 0:
        smallest_disk = None

        # Знаходимо найменший диск
        while source.get_size() > 0:
            current_disk = source.pop()
            if smallest_disk is None or current_disk < smallest_disk:
                if smallest_disk is not None:
                    auxiliary.push(smallest_disk)
                smallest_disk = current_disk
            else:
                auxiliary.push(current_disk)

        # Переміщуємо найменший диск на стрижень destination
        if smallest_disk is not None:
            destination.push(smallest_disk)
            print(f"Move disk {smallest_disk} to {destination.name}")

        # Переміщуємо решту дисків назад на стрижень source
        while auxiliary.get_size() > 0:
            source.push(auxiliary.pop())


def run_disk_sorting():
    """Демонструє сортування дисків на стрижні з довільного порядку"""
    source = CustomStack("A")
    auxiliary = CustomStack("B")
    destination = CustomStack("C")

    # Довільний порядок дисків на стрижні A
    disks = [3, 1, 4, 2]
    for disk in disks:
        source.push(disk)

    print("Initial state of peg A:", disks)
    sort_random_disks(source, destination, auxiliary)
    print("Disks successfully sorted on peg C.")


def test_iterative_hanoi():
    print("Testing iterative_hanoi:")

    # Test 1: Moving 1 disk
    source1 = CustomStack("A")
    destination1 = CustomStack("C")
    auxiliary1 = CustomStack("B")
    source1.push(1)

    expected_moves1 = 1
    move_count1 = iterative_hanoi(1, source1, destination1, auxiliary1)
    print("Test 1 -",
          "Passed" if move_count1 == expected_moves1 else f"Failed. Expected {expected_moves1}, got {move_count1}")

    # Test 2: Moving 2 disks
    source2 = CustomStack("A")
    destination2 = CustomStack("C")
    auxiliary2 = CustomStack("B")
    source2.push(2)
    source2.push(1)

    expected_moves2 = 3
    move_count2 = iterative_hanoi(2, source2, destination2, auxiliary2)
    print("Test 2 -",
          "Passed" if move_count2 == expected_moves2 else f"Failed. Expected {expected_moves2}, got {move_count2}")

    # Test 3: Moving 3 disks
    source3 = CustomStack("A")
    destination3 = CustomStack("C")
    auxiliary3 = CustomStack("B")
    source3.push(3)
    source3.push(2)
    source3.push(1)

    expected_moves3 = 7
    move_count3 = iterative_hanoi(3, source3, destination3, auxiliary3)
    print("Test 3 -",
          "Passed" if move_count3 == expected_moves3 else f"Failed. Expected {expected_moves3}, got {move_count3}")

    print()


def test_sort_random_disks():
    print("Testing sort_random_disks:")

    # Test 1: Sorting disks
    source = CustomStack("A")
    auxiliary = CustomStack("B")
    destination = CustomStack("C")

    disks = [3, 1, 4, 2, 9, 4, 7, 3, 1, 1, -1]
    for disk in disks:
        source.push(disk)

    print("Initial state of peg A:", disks)
    sort_random_disks(source, destination, auxiliary)

    sorted_disks = []
    while destination.get_size() > 0:
        sorted_disks.append(destination.pop())

    expected_sorted_disks = [9, 7, 4, 4, 3, 3, 2, 1, 1, 1, -1]
    print("Disks on peg C:", sorted_disks)
    print("Test 1 -",
          "Passed" if sorted_disks == expected_sorted_disks else f"Failed. Expected {expected_sorted_disks}, got {sorted_disks}")


if __name__ == "__main__":
    # Завдання 5.1
    for n in range(1, 6):
        run_hanoi_simulation(n)

    run_disk_sorting()
