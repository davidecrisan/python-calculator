# Python Calculator

A calculator with a graphical window, written in Python with `tkinter`.
My first Python project.

## Features

- Add, subtract, multiply, divide
- Power (`^`), modulo (`mod`), square root (`√`), percent (`%`)
- Positive/negative switch (`±`) and backspace (`⌫`)
- Works with the mouse **and** the keyboard
- History panel with your last calculations
- Friendly error messages (for example, dividing by zero)
- Automated tests with `pytest`

## How to run

You need Python 3.8 or newer. `tkinter` comes with Python on Windows and macOS.

```
python gui.py
```

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| `0`-`9`, `.` | Type a number |
| `+` `-` `*` `/` `^` | Operations |
| `%` | Modulo |
| `Enter` or `=` | Calculate |
| `Backspace` | Delete last digit |
| `Esc`, `Delete` or `c` | Clear |
| `r` | Square root |

## How to run the tests

```
pip install -r requirements-dev.txt
pytest
```

## Project structure

| File | What it does |
| --- | --- |
| `calculator.py` | The logic: math functions and the `Calculator` class |
| `gui.py` | The window (buttons, display, history) |
| `test_calculator.py` | Automated tests for the logic |

The logic and the window are in separate files, so the logic can be tested without opening a window.
