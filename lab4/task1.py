from customstack import CustomStack


def find_parentheses_pairs(formula):
    stack = CustomStack()
    pairs = []

    for i, char in enumerate(formula):
        if char == '(':
            stack.push(i)
        elif char == ')':
            opening_pos = stack.pop()
            if opening_pos is not None:
                pairs.append((opening_pos, i))

    return pairs


def sort_by_opening(pairs):
    sorted_pairs = []
    stack = CustomStack()

    for pair in pairs:
        stack.push(pair)

    while stack.get_size() > 0:
        current_pair = stack.pop()
        if len(sorted_pairs) == 0:
            sorted_pairs.append(current_pair)
        else:
            inserted = False
            for i in range(len(sorted_pairs)):
                if current_pair[0] < sorted_pairs[i][0]:
                    sorted_pairs.insert(i, current_pair)
                    inserted = True
                    break
            if not inserted:
                sorted_pairs.append(current_pair)

    return sorted_pairs


def sort_by_closing(pairs):
    sorted_pairs = []
    stack = CustomStack()

    for pair in pairs:
        stack.push(pair)

    while stack.get_size() > 0:
        current_pair = stack.pop()
        if len(sorted_pairs) == 0:
            sorted_pairs.append(current_pair)
        else:
            inserted = False
            for i in range(len(sorted_pairs)):
                if current_pair[1] < sorted_pairs[i][1]:
                    sorted_pairs.insert(i, current_pair)
                    inserted = True
                    break
            if not inserted:
                sorted_pairs.append(current_pair)

    return sorted_pairs


def print_for_parenthesis(pairs):
    result = []
    for pair in pairs:
        result.append(f"Open: {pair[0]}, Close: {pair[1]}")
    return result


def test_find_parentheses_pairs():
    print("Testing find_parentheses_pairs:")

    # Test 1: Basic case
    formula1 = "(a + b) * (c + d)"
    expected1 = [(0, 6), (10, 16)]
    result1 = find_parentheses_pairs(formula1)
    print("Test 1 -", "Passed" if result1 == expected1 else f"Failed. Expected {expected1}, got {result1}")

    # Test 2: Nested parentheses
    formula2 = "( (a + b) * (c + d) )"
    expected2 = [(2, 8), (12, 18), (0, 20)]
    result2 = find_parentheses_pairs(formula2)
    print("Test 2 -", "Passed" if result2 == expected2 else f"Failed. Expected {expected2}, got {result2}")

    # Test 3: Empty string
    formula3 = ""
    expected3 = []
    result3 = find_parentheses_pairs(formula3)
    print("Test 3 -", "Passed" if result3 == expected3 else f"Failed. Expected {expected3}, got {result3}")

    # Test 4: Unbalanced parentheses
    formula4 = "(a + (b)"
    expected4 = [(5, 7)]
    result4 = find_parentheses_pairs(formula4)
    print("Test 4 -", "Passed" if result4 == expected4 else f"Failed. Expected {expected4}, got {result4}")

    # Test 5: No parentheses
    formula5 = "a + b * c"
    expected5 = []
    result5 = find_parentheses_pairs(formula5)
    print("Test 5 -", "Passed" if result5 == expected5 else f"Failed. Expected {expected5}, got {result5}")
    print()


def test_sort_by_opening():
    print("Testing sort_by_opening:")

    # Test 1: Random order
    pairs1 = [(6, 12), (18, 22), (0, 24)]
    expected_sorted1 = [(0, 24), (6, 12), (18, 22)]
    result_sorted1 = sort_by_opening(pairs1)
    print("Test 1 -",
          "Passed" if result_sorted1 == expected_sorted1 else f"Failed. Expected {expected_sorted1}, got {result_sorted1}")
    print()


def test_sort_by_closing():
    print("Testing sort_by_closing:")

    # Test 1: Random order
    pairs1 = [(6, 12), (18, 22), (0, 24)]
    expected_sorted1 = [(6, 12), (18, 22), (0, 24)]
    result_sorted1 = sort_by_closing(pairs1)
    print("Test 1 -",
          f"Passed. Expected {expected_sorted1}, got {result_sorted1}" if result_sorted1 == expected_sorted1 else f"Failed. Expected {expected_sorted1}, got {result_sorted1}")
    print()


def test_print_by_opening_order():
    print("Testing print_by_opening_order:")

    pairs1 = [(0, 24), (6, 12), (18, 22)]
    expected_output1 = ['Open: 0, Close: 24', 'Open: 6, Close: 12', 'Open: 18, Close: 22']
    result_output1 = print_for_parenthesis(pairs1)
    print("Test 1 -",
          f"Passed. Expected {expected_output1}, got {result_output1}" if result_output1 == expected_output1 else f"Failed. Expected {expected_output1}, got {result_output1}")
    print()


def test_print_by_closing_order():
    print("Testing print_by_closing_order:")

    pairs1 = [(6, 12), (18, 22), (0, 24)]
    expected_output1 = ['Open: 6, Close: 12', 'Open: 18, Close: 22', 'Open: 0, Close: 24']
    result_output1 = print_for_parenthesis(pairs1)
    print("Test 1 -",
          f"Passed. Expected {expected_output1}, got {result_output1}" if result_output1 == expected_output1 else f"Failed. Expected {expected_output1}, got {result_output1}")
    print()


if __name__ == '__main__':
    test_find_parentheses_pairs()
    test_sort_by_opening()
    test_sort_by_closing()
    test_print_by_opening_order()
    test_print_by_closing_order()
