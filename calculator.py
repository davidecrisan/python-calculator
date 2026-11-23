"""Calculator logic.

This file has NO window code. It only contains:
1. The math functions (add, subtract, ...)
2. The Calculator class, which remembers what the user typed and
   reacts to button presses.

Keeping the logic separate from the window makes it easy to test.
"""

import math


class CalculatorError(Exception):
    """Raised when a calculation is not possible (for example 5 / 0)."""


# ---------------------------------------------------------------------------
# Math functions
# ---------------------------------------------------------------------------

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise CalculatorError("Cannot divide by zero")
    return a / b


def power(a, b):
    try:
        return math.pow(a, b)
    except OverflowError:
        raise CalculatorError("Number too large")
    except ValueError:
        # Happens for things like (-8) ^ 0.5 or 0 ^ -1
        raise CalculatorError("Invalid input")


def modulo(a, b):
    if b == 0:
        raise CalculatorError("Cannot divide by zero")
    return a % b


def square_root(a):
    if a < 0:
        raise CalculatorError("Invalid input")
    return math.sqrt(a)


# Every operator the calculator knows, linked to its function.
OPERATIONS = {
    "+": add,
    "-": subtract,
    "×": multiply,
    "÷": divide,
    "^": power,
    "mod": modulo,
}

# Keyboard characters that can be used instead of the symbols above.
OPERATOR_ALIASES = {
    "*": "×",
    "/": "÷",
}


def calculate(a, operator, b):
    """Do one calculation, for example calculate(6, "×", 7) -> 42."""
    operator = OPERATOR_ALIASES.get(operator, operator)
    if operator not in OPERATIONS:
        raise CalculatorError(f"Unknown operation: {operator}")

    try:
        result = OPERATIONS[operator](a, b)
    except OverflowError:
        raise CalculatorError("Number too large")

    # Python floats turn into "inf" when they get too big.
    if math.isinf(result) or math.isnan(result):
        raise CalculatorError("Number too large")
    return result


def format_number(value):
    """Turn a number into nice text: 5.0 -> "5", 0.30000000000000004 -> "0.3"."""
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.10g}"


# ---------------------------------------------------------------------------
# The Calculator class
# ---------------------------------------------------------------------------

class Calculator:
    """Remembers the state of the calculator and reacts to button presses.

    After every button press you can read:
        calculator.display     -> the big number on the screen
        calculator.expression  -> the small line above it (for example "5 +")
        calculator.history     -> a list of finished calculations
    """

    MAX_DIGITS = 15
    MAX_HISTORY = 50

    def __init__(self):
        self.history = []
        self.clear()

    # -- helpers ------------------------------------------------------------

    def _current_value(self):
        return float(self.display)

    def _digit_count(self):
        return sum(character.isdigit() for character in self.display)

    def _show_error(self, error):
        self.display = str(error)
        self.expression = ""
        self.first_number = None
        self.operator = None
        self.start_new_number = True
        self.has_error = True

    def _add_to_history(self, text):
        self.history.append(text)
        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)

    # -- buttons ------------------------------------------------------------

    def clear(self):
        """The C button: reset everything except the history."""
        self.display = "0"
        self.expression = ""
        self.first_number = None
        self.operator = None
        self.start_new_number = True
        self.has_error = False

    def clear_history(self):
        self.history = []

    def press_digit(self, digit):
        if self.has_error:
            self.clear()

        if self.start_new_number:
            self.display = digit
            self.start_new_number = False
        elif self._digit_count() < self.MAX_DIGITS:
            if self.display == "0":
                self.display = digit
            else:
                self.display += digit

    def press_dot(self):
        if self.has_error:
            self.clear()

        if self.start_new_number:
            self.display = "0."
            self.start_new_number = False
        elif "." not in self.display:
            self.display += "."

    def press_operator(self, operator):
        operator = OPERATOR_ALIASES.get(operator, operator)
        if self.has_error:
            return

        if self.operator is not None and self.start_new_number:
            # Two operators in a row (5 + ×): the last one wins.
            self.operator = operator
        else:
            current = self._current_value()
            if self.operator is not None:
                # Chained calculation (5 + 3 ×): finish 5 + 3 first.
                try:
                    current = calculate(self.first_number, self.operator, current)
                except CalculatorError as error:
                    self._show_error(error)
                    return
                self.display = format_number(current)
            self.first_number = current
            self.operator = operator
            self.start_new_number = True

        self.expression = f"{format_number(self.first_number)} {self.operator}"

    def press_equals(self):
        if self.has_error or self.operator is None:
            return

        first = self.first_number
        second = self._current_value()
        try:
            result = calculate(first, self.operator, second)
        except CalculatorError as error:
            self._show_error(error)
            return

        text = f"{format_number(first)} {self.operator} {format_number(second)}"
        self.display = format_number(result)
        self.expression = text + " ="
        self._add_to_history(f"{text} = {self.display}")

        self.first_number = None
        self.operator = None
        self.start_new_number = True

    def press_square_root(self):
        if self.has_error:
            return

        value = self._current_value()
        try:
            result = square_root(value)
        except CalculatorError as error:
            self._show_error(error)
            return

        text = f"√({format_number(value)})"
        self.display = format_number(result)
        self.start_new_number = True
        if self.operator is None:
            self.expression = text + " ="
        self._add_to_history(f"{text} = {self.display}")

    def press_percent(self):
        """The % button divides the number on the screen by 100."""
        if self.has_error:
            return

        value = self._current_value()
        self.display = format_number(value / 100)
        self.start_new_number = True
        if self.operator is None:
            self.expression = f"{format_number(value)} ÷ 100 ="

    def press_negate(self):
        """The ± button: switch between positive and negative."""
        if self.has_error or self.display == "0":
            return

        if self.display.startswith("-"):
            self.display = self.display[1:]
        else:
            self.display = "-" + self.display

    def backspace(self):
        """The ⌫ button: delete the last typed character."""
        if self.has_error or self.start_new_number:
            return

        self.display = self.display[:-1]
        if self.display in ("", "-"):
            self.display = "0"
