import sys
from io import StringIO


def analyze_numbers(numbers):
    try:
        positive_count = 0
        negative_count = 0
        negative_sum = 0

        for num in numbers:
            if isinstance(num, (int, float)):
                if num > 0:
                    positive_count += 1
                elif num < 0:
                    negative_count += 1
                    negative_sum += num

        if negative_count == 0:
            negative_avg = 0
        else:
            negative_avg = negative_sum / negative_count

        return positive_count, negative_count, round(negative_avg, 2)
    except Exception:
        return 0, 0, 0


def analyze_triangle(a, b, c):
    if a + b > c and a + c > b and b + c > a:
        if a == b and b == c:
            return "Рівносторонній трикутник"
        elif a == b or b == c or a == c:
            return "Рівнобедрений трикутник"
        else:
            return "Різносторонній трикутник"
    else:
        return "Такий трикутник не існує"


def split_sentence(sentence):
    words = sentence.split()
    for word in words:
        print(word)


def find_max_sum_rectangle(matrix):
    try:
        rows = len(matrix)
        cols = len(matrix[0])
        max_sum = float("-inf")
        start_row, start_col, end_row, end_col = None, None, None, None

        for top_row in range(rows):
            for left_col in range(cols):
                for bottom_row in range(top_row, rows):
                    for right_col in range(left_col, cols):
                        current_sum = 0
                        for i in range(top_row, bottom_row + 1):
                            for j in range(left_col, right_col + 1):
                                current_sum += matrix[i][j]

                        if current_sum > max_sum:
                            max_sum = current_sum
                            start_row, start_col, end_row, end_col = top_row, left_col, bottom_row, right_col

        return max_sum, (start_row, start_col, end_row, end_col)
    except Exception:
        return 0, []


def read_test_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        input_data = []
        expected_output = []
        reading_input = False
        t = []

        for line in lines:
            if line.startswith('Вхідні дані:'):
                if len(expected_output) > 0:
                    t.append('\n'.join(expected_output))
                    expected_output = []
                reading_input = True
                continue
            elif line.startswith('Очікуваний результат:'):
                reading_input = False
                continue
            elif line.strip() != '' and reading_input:
                input_data.append(line.strip())
            elif line.strip() != '' and not reading_input:
                expected_output.append(line.strip())
        t.append('\n'.join(expected_output))
        expected_output = t

    return input_data, expected_output


def split_into_float_and_tuple(input_str):
    parts = input_str.split(',')
    float_value = float(str.strip(parts[0]))
    tuple_values = tuple(map(float, remove_parentheses(input_str).split(",", 1)[1].split(",")))

    return float_value, tuple_values


def remove_parentheses(input_str):
    result_str = input_str.replace("(", "").replace(")", "")
    return result_str


def run_tests(test_function, test_data):
    if test_data is None:
        return []

    input_data, expected_output = test_data
    results = []

    for i, input_values in enumerate(input_data):
        try:
            if test_function.__name__ == "analyze_numbers":
                result = test_function(list(map(float, input_values.split())))
                expected_output[i] = tuple(map(float, expected_output[i].split()))
            elif test_function.__name__ == "analyze_triangle":
                a, b, c = map(float, input_values.split())
                expected_output[i] = analyze_triangle(a, b, c)
                result = test_function(a, b, c)
            elif test_function.__name__ == "split_sentence":
                old_stdout = sys.stdout
                sys.stdout = StringIO()

                test_function(input_values)

                captured_output = sys.stdout.getvalue()

                sys.stdout = old_stdout

                result = captured_output.strip()
                expected_output[i] = expected_output[i].strip()
            elif test_function.__name__ == "find_max_sum_rectangle":
                matrix = [list(map(float, row.split())) for row in input_values.split(';')]
                expected_output[i] = split_into_float_and_tuple(expected_output[i])
                result = test_function(matrix)
            else:
                raise ValueError("Невідома функція")

            results.append((result == expected_output[i], result))
        except Exception as e:
            print(f"Помилка при виконанні тесту {i + 1}: {e}")
            results.append((False, None))

    return results


def write_test_results(test_name, input_data, expected_output, results):
    if input_data is None or expected_output is None:
        print("Дані тестів недоступні. Немає що записувати.")
        return

    with open('ResultAll.txt', 'a') as result_file:
        result_file.write(f'{test_name}\n')

        for i in range(len(input_data)):
            result_file.write(f'вхід:\n{input_data[i]}\n')

            result, result_value = results[i]
            expected = expected_output[i]

            result_file.write(f'Отримані результати: {"Пройдено" if result else "Провалено"}\n')
            result_file.write(f'Результат виконання: {result_value}\n')
            result_file.write(f'Очікуваний результат: {expected}\n')
            result_file.write('---------------------------\n')


def main():
    while True:
        print("Оберіть функцію для тестування:")
        print("1. analyze_numbers")
        print("2. analyze_triangle")
        print("3. split_sentence")
        print("4. find_max_sum_rectangle")
        print("5. Вийти")

        choice = input("Ваш вибір: ")

        if choice == '1':
            test_function = analyze_numbers
        elif choice == '2':
            test_function = analyze_triangle
        elif choice == '3':
            test_function = split_sentence
        elif choice == '4':
            test_function = find_max_sum_rectangle
        elif choice == '5':
            break
        else:
            print("Неправильний вибір. Спробуйте ще раз.")
            continue

        test_name = f"Тестування функції {test_function.__name__}"
        test_data = read_test_data(f'InData{choice}.txt')
        if test_data is not None:
            input_data, expected_output = test_data
            results = run_tests(test_function, test_data)
            write_test_results(test_name, input_data, expected_output, results)


if __name__ == "__main__":
    main()
