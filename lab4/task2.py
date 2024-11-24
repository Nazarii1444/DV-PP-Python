from customstack import CustomStack


def calculate_sum_of_nested_list(nested_list):
    """Task 2 - Calculate the sum of elements in a nested list"""
    stack = CustomStack()
    total = 0
    stack.push(iter(nested_list))

    while stack.get_size() > 0:
        current_iterator = stack.pop()
        for element in current_iterator:
            if isinstance(element, list):
                stack.push(iter(element))
            elif isinstance(element, (int, float)):
                total += element

    return total


def test_calculate_sum_of_nested_list():
    """Test functions for calculate_sum_of_nested_list"""
    print("Testing calculate_sum_of_nested_list:")

    # Test 1: Case with both positive and negative numbers
    nested_list1 = [5, -2, [3, [-1, 2]], -6, [[4, [-7, 7], [3, -3]]]]
    expected_sum1 = 5
    result1 = calculate_sum_of_nested_list(nested_list1)
    print("Test 1 -", "Passed" if result1 == expected_sum1 else f"Failed. Expected {expected_sum1}, got {result1}")

    # Test 2: Large flat list with zero elements
    nested_list2 = [0, 0, 0, 0, 0]
    expected_sum2 = 0
    result2 = calculate_sum_of_nested_list(nested_list2)
    print("Test 2 -", "Passed" if result2 == expected_sum2 else f"Failed. Expected {expected_sum2}, got {result2}")

    # Test 3: Deeply nested list with one element
    nested_list3 = [[[[[[42]]]]]]
    expected_sum3 = 42
    result3 = calculate_sum_of_nested_list(nested_list3)
    print("Test 3 -", "Passed" if result3 == expected_sum3 else f"Failed. Expected {expected_sum3}, got {result3}")

    # Test 4: List with mixed types (including strings, which should be ignored)
    nested_list4 = [5, [3, ["hello", 2]], [6, [None, 8], "world"]]
    expected_sum4 = 24
    result4 = calculate_sum_of_nested_list(nested_list4)
    print("Test 4 -", "Passed" if result4 == expected_sum4 else f"Failed. Expected {expected_sum4}, got {result4}")

    # Test 5: List with all zero values
    nested_list5 = [[0], [0, [0, [0]]], 0]
    expected_sum5 = 0
    result5 = calculate_sum_of_nested_list(nested_list5)
    print("Test 5 -", "Passed" if result5 == expected_sum5 else f"Failed. Expected {expected_sum5}, got {result5}")

    # Test 6: Complex nested list with a mix of integers and empty lists
    nested_list6 = [[], [1, [], [2, [], 3]], 4]
    expected_sum6 = 10
    result6 = calculate_sum_of_nested_list(nested_list6)
    print("Test 6 -", "Passed" if result6 == expected_sum6 else f"Failed. Expected {expected_sum6}, got {result6}")

    # Test 7: Empty list
    nested_list7 = []
    expected_sum7 = 0
    result7 = calculate_sum_of_nested_list(nested_list7)
    print("Test 7 -", "Passed" if result7 == expected_sum7 else f"Failed. Expected {expected_sum7}, got {result7}")


if __name__ == '__main__':
    test_calculate_sum_of_nested_list()
