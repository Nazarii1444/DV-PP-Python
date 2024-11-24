import json

def fn_sol_1(numbers):
    try:
        positive_count = 0
        negative_count = 0
        negative_sum = 0
        negative_count_total = 0

        for number in numbers:
            if number > 0:
                positive_count += 1
            elif number < 0:
                negative_count += 1
                negative_sum += number
                negative_count_total += 1

        avg_negative = negative_sum / negative_count_total if negative_count_total != 0 else 0
        return positive_count, negative_count, avg_negative
    except Exception as e:
        return 0, 0, 0

def fn_sol_2(a, b, c):
    try:
        if a + b > c and a + c > b and b + c > a:
            if a == b == c:
                return "Equilateral"
            elif a == b or b == c or a == c:
                return "Rivnobedrebyi"
            else:
                return "Versatile"
        else:
            return "Not a triangle"
    except:
        return "Not a triangle"

def fn_sol_3(sentence):
    try:
        return sentence.split()
    except:
        return []

def fn_sol_4(matrix):
    try:
        rows = len(matrix)
        cols = len(matrix[0])
        max_sum = float("-inf")
        start_row, start_col, end_row, end_col = None, None, None, None

        for top_row in range(rows):
            for left_col in range(cols):
                for bottom_row in range(top_row, rows):
                    for right_col in range(left_col, cols):
                        cur_sum = 0
                        for i in range(top_row, bottom_row + 1):
                            for j in range(left_col, right_col + 1):
                                cur_sum += matrix[i][j]

                        if cur_sum > max_sum:
                            max_sum = cur_sum
                            start_row, start_col, end_row, end_col = top_row, left_col, bottom_row, right_col

        return max_sum, (start_row, start_col, end_row, end_col)
    except Exception:
        return 0, []

def read_input_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_results_to_res(filename, results):
    with open(filename, 'a') as f:
        f.write(f"{results}\n")

def run_tests_for_function(function, data_file, result_file, arg_name):
    data = read_input_data(data_file)
    for test in data["tests"]:
        print(f"Running: {test['description']}")

        if isinstance(arg_name, list):
            args = {key: test[key] for key in arg_name}
            result = function(**args)
        else:
            result = function(test[arg_name])

        expected = test["expected"]

        if isinstance(expected, int):
            passed = result == expected
            status = "Passed" if passed else "Failed"
            write_results_to_res(result_file, f"Test {test['description']} result: {result} {status}")
            print(f"Result: {result}, Expected: {expected} {status}")

        elif isinstance(expected, (list, tuple)):
            if len(expected) == 2 and isinstance(expected[1], (list, tuple)):
                passed = result[0] == expected[0] and list(result[1]) == list(expected[1])
            else:
                passed = list(result) == list(expected)

            status = "Passed" if passed else "Failed"
            write_results_to_res(result_file, f"Test {test['description']} result: {result} {status}")
            print(f"Result: {result}, Expected: {expected} {status}")

        elif isinstance(expected, str):
            passed = result == expected
            status = "Passed" if passed else "Failed"
            write_results_to_res(result_file, f"Test {test['description']} result: {result} {status}")
            print(f"Result: {result}, Expected: {expected} {status}")


def test_fn_sol_1():
    print("============= Testing: test_fn_sol_1")
    run_tests_for_function(fn_sol_1, "InData1.json", "Res1.txt", "numbers")


def test_fn_sol_2():
    print("============= Testing: test_fn_sol_2")
    run_tests_for_function(fn_sol_2, "InData2.json", "Res2.txt", ["a", "b", "c"])


def test_fn_sol_3():
    print("============= Testing: test_fn_sol_3")
    run_tests_for_function(fn_sol_3, "InData3.json", "Res3.txt", "sentence")


def test_fn_sol_4():
    print("============= Testing: test_fn_sol_4")
    run_tests_for_function(fn_sol_4, "InData4.json", "Res4.txt", "matrix")

def testorg():
    while True:
        print('Enter a problem number (1-4) or enter "exit:" ')
        print("1 - fn_sol_1")
        print("2 - fn_sol_2")
        print("3 - fn_sol_3")
        print("4 - fn_sol_4")

        choice = input("Choice: ")

        if choice == "exit":
            exit(0)
        else:
            choice = int(choice)

        if choice == 1:
            test_fn_sol_1()
        elif choice == 2:
            test_fn_sol_2()
        elif choice == 3:
            test_fn_sol_3()
        elif choice == 4:
            test_fn_sol_4()
        else:
            print("Wrong problem number")

if __name__ == "__main__":
    testorg()
