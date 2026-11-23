"""Tests for calculator.py. Run them with:  pytest"""

import pytest

from calculator import (
    Calculator,
    CalculatorError,
    add,
    calculate,
    divide,
    format_number,
    modulo,
    multiply,
    power,
    square_root,
    subtract,
)


def press(calculator, keys):
    """Press many buttons at once, for example press(calc, "1 2 + 3 =").

    Words are separated by spaces. A word made of digits (like "12")
    presses each digit one after the other.
    """
    for key in keys.split():
        if key.isdigit():
            for digit in key:
                calculator.press_digit(digit)
        elif key == ".":
            calculator.press_dot()
        elif key == "=":
            calculator.press_equals()
        elif key == "C":
            calculator.clear()
        elif key == "back":
            calculator.backspace()
        elif key == "neg":
            calculator.press_negate()
        elif key == "sqrt":
            calculator.press_square_root()
        elif key == "percent":
            calculator.press_percent()
        else:
            calculator.press_operator(key)
    return calculator


# ---------------------------------------------------------------------------
# Math functions
# ---------------------------------------------------------------------------

def test_basic_operations():
    assert add(2, 3) == 5
    assert subtract(2, 3) == -1
    assert multiply(4, 2.5) == 10
    assert divide(9, 3) == 3
    assert modulo(10, 3) == 1
    assert power(2, 10) == 1024
    assert square_root(81) == 9


def test_divide_by_zero():
    with pytest.raises(CalculatorError):
        divide(5, 0)


def test_modulo_by_zero():
    with pytest.raises(CalculatorError):
        modulo(5, 0)


def test_square_root_of_negative_number():
    with pytest.raises(CalculatorError):
        square_root(-4)


def test_power_with_invalid_input():
    with pytest.raises(CalculatorError):
        power(-8, 0.5)
    with pytest.raises(CalculatorError):
        power(0, -1)


def test_power_with_huge_result():
    with pytest.raises(CalculatorError):
        power(10, 1000)


def test_multiply_with_huge_result():
    with pytest.raises(CalculatorError):
        calculate(1e200, "×", 1e200)


def test_calculate_accepts_keyboard_symbols():
    assert calculate(6, "*", 7) == 42
    assert calculate(8, "/", 2) == 4


def test_calculate_unknown_operator():
    with pytest.raises(CalculatorError):
        calculate(1, "?", 2)


def test_format_number():
    assert format_number(5.0) == "5"
    assert format_number(-3.0) == "-3"
    assert format_number(2.5) == "2.5"
    assert format_number(0.1 + 0.2) == "0.3"
    assert format_number(-0.0) == "0"


# ---------------------------------------------------------------------------
# Calculator class (button presses)
# ---------------------------------------------------------------------------

def test_starts_at_zero():
    calculator = Calculator()
    assert calculator.display == "0"
    assert calculator.expression == ""


def test_typing_digits():
    calculator = press(Calculator(), "1 2 3")
    assert calculator.display == "123"


def test_no_leading_zeros():
    calculator = press(Calculator(), "0 0 7")
    assert calculator.display == "7"


def test_decimal_point():
    calculator = press(Calculator(), "1 . 5")
    assert calculator.display == "1.5"


def test_only_one_decimal_point():
    calculator = press(Calculator(), "1 . 5 . 2")
    assert calculator.display == "1.52"


def test_decimal_point_first():
    calculator = press(Calculator(), ". 5")
    assert calculator.display == "0.5"


def test_digit_limit():
    calculator = press(Calculator(), "1" * 30)
    assert len(calculator.display) == Calculator.MAX_DIGITS


def test_simple_addition():
    calculator = press(Calculator(), "2 + 3 =")
    assert calculator.display == "5"
    assert calculator.expression == "2 + 3 ="


def test_all_operators():
    assert press(Calculator(), "9 - 4 =").display == "5"
    assert press(Calculator(), "6 × 7 =").display == "42"
    assert press(Calculator(), "8 ÷ 4 =").display == "2"
    assert press(Calculator(), "2 ^ 8 =").display == "256"
    assert press(Calculator(), "10 mod 3 =").display == "1"


def test_keyboard_symbols_work_as_operators():
    assert press(Calculator(), "6 * 7 =").display == "42"
    assert press(Calculator(), "8 / 4 =").display == "2"


def test_decimal_math_has_no_rounding_noise():
    calculator = press(Calculator(), "0 . 1 + 0 . 2 =")
    assert calculator.display == "0.3"


def test_chained_operations_go_left_to_right():
    calculator = press(Calculator(), "2 + 3 × 4 =")
    assert calculator.display == "20"


def test_changing_operator():
    calculator = press(Calculator(), "5 + × 3 =")
    assert calculator.display == "15"


def test_continue_with_result():
    calculator = press(Calculator(), "2 + 3 = × 4 =")
    assert calculator.display == "20"


def test_typing_after_result_starts_new_number():
    calculator = press(Calculator(), "2 + 3 = 7")
    assert calculator.display == "7"


def test_equals_without_operator_does_nothing():
    calculator = press(Calculator(), "5 =")
    assert calculator.display == "5"
    assert calculator.history == []


def test_divide_by_zero_shows_error():
    calculator = press(Calculator(), "5 ÷ 0 =")
    assert calculator.has_error
    assert calculator.display == "Cannot divide by zero"


def test_typing_after_error_starts_fresh():
    calculator = press(Calculator(), "5 ÷ 0 = 7")
    assert not calculator.has_error
    assert calculator.display == "7"


def test_operators_ignored_after_error():
    calculator = press(Calculator(), "5 ÷ 0 = +")
    assert calculator.has_error


def test_clear_resets_error():
    calculator = press(Calculator(), "5 ÷ 0 = C")
    assert not calculator.has_error
    assert calculator.display == "0"


def test_clear_in_the_middle():
    calculator = press(Calculator(), "5 + 3 C 2 =")
    assert calculator.display == "2"  # no operator left, so "=" does nothing


def test_backspace():
    calculator = press(Calculator(), "1 2 3 back")
    assert calculator.display == "12"


def test_backspace_to_zero():
    calculator = press(Calculator(), "5 back")
    assert calculator.display == "0"


def test_backspace_does_not_change_a_result():
    calculator = press(Calculator(), "2 + 3 = back")
    assert calculator.display == "5"


def test_negate():
    calculator = press(Calculator(), "5 neg")
    assert calculator.display == "-5"
    calculator.press_negate()
    assert calculator.display == "5"


def test_negate_zero_does_nothing():
    calculator = press(Calculator(), "neg")
    assert calculator.display == "0"


def test_negative_number_in_calculation():
    calculator = press(Calculator(), "5 neg + 2 =")
    assert calculator.display == "-3"


def test_square_root_button():
    calculator = press(Calculator(), "1 6 sqrt")
    assert calculator.display == "4"
    assert calculator.history[-1] == "√(16) = 4"


def test_square_root_of_negative_shows_error():
    calculator = press(Calculator(), "4 neg sqrt")
    assert calculator.has_error


def test_percent_button():
    calculator = press(Calculator(), "5 0 percent")
    assert calculator.display == "0.5"


def test_history_is_saved():
    calculator = press(Calculator(), "2 + 3 = × 4 =")
    assert calculator.history == ["2 + 3 = 5", "5 × 4 = 20"]


def test_clear_does_not_erase_history():
    calculator = press(Calculator(), "2 + 3 = C")
    assert len(calculator.history) == 1


def test_clear_history():
    calculator = press(Calculator(), "2 + 3 =")
    calculator.clear_history()
    assert calculator.history == []


def test_history_has_a_size_limit():
    calculator = Calculator()
    for _ in range(Calculator.MAX_HISTORY + 10):
        press(calculator, "1 + 1 =")
    assert len(calculator.history) == Calculator.MAX_HISTORY
