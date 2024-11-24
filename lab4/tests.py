from task1 import (
    test_find_parentheses_pairs,
    test_sort_by_opening,
    test_sort_by_closing,
    test_print_by_opening_order,
    test_print_by_closing_order
)
from task2 import test_calculate_sum_of_nested_list
from task3 import test_validate_formula
from task4 import test_evaluate_expression
from task5 import test_sort_random_disks, test_iterative_hanoi

TEST_FUNCTIONS = {
    '1': test_find_parentheses_pairs,
    '2': test_sort_by_opening,
    '3': test_sort_by_closing,
    '4': test_print_by_opening_order,
    '5': test_print_by_closing_order,
    '6': test_calculate_sum_of_nested_list,
    '7': test_validate_formula,
    '8': test_evaluate_expression,
    '9': test_iterative_hanoi,
    '10': test_sort_random_disks
}


def print_help():
    """Виводить інформацію про всі доступні тестові функції."""
    print(
        "Доступні варіанти тестів:\n"
        "\nЗавдання 1 - Робота з дужками:\n"
        "  1. test_find_parentheses_pairs() - Тест на знаходження пар дужок у формулі.\n"
        "  2. test_sort_by_opening() - Тест для сортування пар дужок за позицією відкриття.\n"
        "  3. test_sort_by_closing() - Тест для сортування пар дужок за позицією закриття.\n"
        "  4. test_print_by_opening_order() - Тест для виведення пар дужок у порядку відкриття.\n"
        "  5. test_print_by_closing_order() - Тест для виведення пар дужок у порядку закриття.\n"
        "\nЗавдання 2 - Сума вкладених списків:\n"
        "  6. test_calculate_sum_of_nested_list() - Тест для обчислення суми елементів у вкладених списках.\n"
        "\nЗавдання 3 - Перевірка формули:\n"
        "  7. test_validate_formula() - Тест для перевірки правильності формули та збалансованості дужок.\n"
        "\nЗавдання 4 - Обчислення формули:\n"
        "  8. test_evaluate_expression() - Тест для обчислення математичних виразів.\n"
        "\nЗавдання 5 - Сортування дисків та Ханойські вежі:\n"
        "  9. test_iterative_hanoi() - Тест для ітеративного розв'язання задачі Ханойських веж.\n"
        "  10. test_sort_random_disks() - Тест для сортування випадково розміщених дисків.\n"
    )


def get_choice():
    return input("\nВиберіть номер тесту для запуску або введіть 'stop' для виходу: ").strip().lower()


if __name__ == '__main__':
    while True:
        print_help()
        choice = get_choice()

        if choice == 'stop':
            print("Вихід...")
            break
        elif choice in TEST_FUNCTIONS:
            TEST_FUNCTIONS[choice]()
        else:
            print("Неправильний вибір :( Спробуйте ще раз!")
