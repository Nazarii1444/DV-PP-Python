from customstack import CustomStack


def validate_expression(expression):
    stack = CustomStack()
    valid_chars = set("xyz+-()[]{} ")
    prev_char = ''

    for char in expression:
        if char not in valid_chars:
            return False

        if char in "xyz":
            if prev_char in "+-":
                pass
            prev_char = char

        elif char in "+-":
            if prev_char in "+-(" or prev_char == '':
                return False

        elif char in "({[":
            stack.push(char)
            prev_char = char

        elif char in ")}]":
            if stack.get_size() == 0:
                return False

            opening_bracket = stack.pop()
            if (opening_bracket == '(' and char != ')') or \
                    (opening_bracket == '{' and char != '}') or \
                    (opening_bracket == '[' and char != ']'):
                return False

        prev_char = char

    if stack.get_size() > 0:
        return False

    if prev_char in "+-":
        return False

    return True  # Формула коректна


def test_validate_formula():
    """Test functions for validate_formula"""
    print("Testing validate_formula:")

    # Test 1: Correct formula
    formula1 = "x + ( y - z - [ x + x ] + { [ z - z - y ] + ( y ) } ) - z"
    expected1 = True
    result1 = validate_expression(formula1)
    print("Test 1 -", "Passed" if result1 == expected1 else f"Failed. Expected {expected1}, got {result1}")

    # Test 2: Formula ending with an operator
    formula2 = "x + ( y - z - [ x + x ] + { [ z - z - y ] + ( y ) } ) -"
    expected2 = False
    result2 = validate_expression(formula2)
    print("Test 2 -", "Passed" if result2 == expected2 else f"Failed. Expected {expected2}, got {result2}")

    # Test 3: Empty formula
    formula3 = ""
    expected3 = False
    result3 = validate_expression(formula3)
    print("Test 3 -", "Passed" if result3 == expected3 else f"Failed. Expected {expected3}, got {result3}")

    # Test 4: Formula with unclosed brackets
    formula4 = "x + ( y - z - [ x + x ] + { [ z - z - y ] + ( y ) "
    expected4 = False
    result4 = validate_expression(formula4)
    print("Test 4 -", "Passed" if result4 == expected4 else f"Failed. Expected {expected4}, got {result4}")

    # Test 5: Formula without brackets (valid)
    formula5 = "x + y - z + x + y - z"
    expected5 = True
    result5 = validate_expression(formula5)
    print("Test 5 -", "Passed" if result5 == expected5 else f"Failed. Expected {expected5}, got {result5}")

    # Test 6: Formula with incorrect brackets
    formula6 = "x + ( y - z - [ x + x ] + { [ z - z - y ] + y ) }"
    expected6 = False
    result6 = validate_expression(formula6)
    print("Test 6 -", "Passed" if result6 == expected6 else f"Failed. Expected {expected6}, got {result6}")

    # Test 7: Valid formula with different types of brackets
    formula7 = "(x + [y - {z + x}] - z)"
    expected7 = True
    result7 = validate_expression(formula7)
    print("Test 7 -", "Passed" if result7 == expected7 else f"Failed. Expected {expected7}, got {result7}")


if __name__ == "__main__":
    test_validate_formula()
