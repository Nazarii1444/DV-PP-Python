from customstack import CustomStack


def evaluate_expression(expression):
    """Task 4 - Evaluate a formula based on S (sum) and D (division) operations"""
    if not expression:
        raise ValueError("Invalid expression: the expression is empty.")

    stack = CustomStack()
    index = 0

    while index < len(expression):
        char = expression[index]

        if char.isdigit() or (char == '-' and index + 1 < len(expression) and expression[index + 1].isdigit()):
            # Збираємо повне число, враховуючи від'ємне число
            num_str = ""
            if char == '-':
                num_str += char
                index += 1
            while index < len(expression) and expression[index].isdigit():
                num_str += expression[index]
                index += 1
            stack.push(int(num_str))
            continue  # Переходимо до наступного символу

        elif char in {'S', 'D'}:
            stack.push(char)
            index += 1  # Пропускаємо відкриваючу дужку

        elif char == '(':
            # Пропускаємо відкриваючу дужку
            index += 1

        elif char == ')':
            # Обробляємо вираз
            right_operand = stack.pop()
            if right_operand is None:
                raise ValueError("Invalid expression: insufficient operands")

            left_operand = stack.pop()
            if left_operand is None:
                raise ValueError("Invalid expression: insufficient operands")

            operator = stack.pop()
            if operator is None:
                raise ValueError("Invalid expression: missing operator")

            # Виконуємо операцію
            if operator == 'S':
                result = left_operand + right_operand
            elif operator == 'D':
                if right_operand == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                result = left_operand // right_operand
            else:
                raise ValueError("Unknown operation")

            # Кладемо результат назад у стек
            stack.push(result)

        # Пропускаємо інші символи (пробіли, коми і т.п.)
        index += 1

    # Остаточний результат
    final_result = stack.pop()
    if stack.get_size() != 0:
        raise ValueError("Invalid expression: extraneous data")

    return final_result


def test_evaluate_expression():
    print("Testing evaluate_expression:")

    # Test 1: Валідний вираз з великими числами
    formula1 = "S(1000000,D(100000,10))"  # 1000000 + (100000 / 10) = 1000000 + 10000 = 1010000
    expected1 = 1010000
    result1 = evaluate_expression(formula1)
    print("Test 1 -", "Passed" if result1 == expected1 else f"Failed. Expected {expected1}, got {result1}")

    # Test 2: Валідний вираз з кількома рівнями вкладеності
    formula2 = "D(S(4,2),S(1,1))"  # (4 + 2) / (1 + 1) = 6 / 2 = 3
    expected2 = 3
    result2 = evaluate_expression(formula2)
    print("Test 2 -", "Passed" if result2 == expected2 else f"Failed. Expected {expected2}, got {result2}")

    # Test 3: Вираз з мінусовими числами
    formula3 = "S(-5,D(-10,2))"  # -5 + (-10 / 2) = -5 + (-5) = -10
    expected3 = -10
    result3 = evaluate_expression(formula3)
    print("Test 3 -", "Passed" if result3 == expected3 else f"Failed. Expected {expected3}, got {result3}")

    # Test 4: Невалідний вираз з пропущеними дужками
    formula4 = "S(5,D(4,2)"  # Немає закриваючої дужки
    try:
        evaluate_expression(formula4)
        print("Test 4 - Failed. Expected ValueError.")
    except ValueError:
        print("Test 4 - Passed: Missing closing parenthesis detected")

    # Test 5: Вираз з нульовим числом у додаванні
    formula5 = "S(0,0)"  # 0 + 0 = 0
    expected5 = 0
    result5 = evaluate_expression(formula5)
    print("Test 5 -", "Passed" if result5 == expected5 else f"Failed. Expected {expected5}, got {result5}")

    # Test 6: Валідний вираз з вкладеним діленням
    formula6 = "D(20,D(100,5))"  # 20 / (100 / 5) = 20 / 20 = 1
    expected6 = 1
    result6 = evaluate_expression(formula6)
    print("Test 6 -", "Passed" if result6 == expected6 else f"Failed. Expected {expected6}, got {result6}")

    # Test 7: Невалідний вираз з відсутнім аргументом
    formula7 = "S(5,)"  # Відсутній другий аргумент
    try:
        evaluate_expression(formula7)
        print("Test 7 - Failed. Expected ValueError.")
    except ValueError:
        print("Test 7 - Passed: Missing argument detected")

    # Test 8: Вираз, що використовує нуль як дільник
    formula8 = "D(10,0)"  # Ділення на нуль має викликати ZeroDivisionError
    try:
        evaluate_expression(formula8)
        print("Test 8 - Failed. Expected ZeroDivisionError.")
    except ZeroDivisionError:
        print("Test 8 - Passed: Division by zero detected")

    # Test 9: Вираз з від'ємним дільником
    formula9 = "D(10,-2)"  # 10 / (-2) = -5
    expected9 = -5
    result9 = evaluate_expression(formula9)
    print("Test 9 -", "Passed" if result9 == expected9 else f"Failed. Expected {expected9}, got {result9}")

    # Test 10: Валідний вираз з глибоким вкладенням
    formula10 = "S(D(20,S(3,D(9,3))),2)"  # (20 / (3 + (9 / 3))) + 2 = (20 / 6) + 2 = 3 + 2 = 5
    expected10 = 5
    result10 = evaluate_expression(formula10)
    print("Test 10 -", "Passed" if result10 == expected10 else f"Failed. Expected {expected10}, got {result10}")

    print()


if __name__ == '__main__':
    test_evaluate_expression()
