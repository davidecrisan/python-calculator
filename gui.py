"""The calculator window, built with tkinter.

Run it with:  python gui.py

This file only draws the window and sends button presses to the
Calculator class in calculator.py, where the real work happens.
"""

import tkinter as tk

from calculator import OPERATIONS, OPERATOR_ALIASES, Calculator

FONT = "Segoe UI"

# Colors
BACKGROUND = "#1c1c1e"
TEXT = "#ffffff"
MUTED_TEXT = "#a1a1a6"

# Each button style has a normal color, a hover color and a text color.
STYLES = {
    "number": {"bg": "#3a3a3c", "hover": "#4a4a4d", "fg": "#ffffff"},
    "function": {"bg": "#636366", "hover": "#757579", "fg": "#ffffff"},
    "operator": {"bg": "#ff9f0a", "hover": "#ffb340", "fg": "#ffffff"},
}

# (text, row, column, column span, style)
BUTTONS = [
    ("√", 0, 0, 1, "function"), ("^", 0, 1, 1, "function"),
    ("mod", 0, 2, 1, "function"), ("⌫", 0, 3, 1, "function"),

    ("C", 1, 0, 1, "function"), ("±", 1, 1, 1, "function"),
    ("%", 1, 2, 1, "function"), ("÷", 1, 3, 1, "operator"),

    ("7", 2, 0, 1, "number"), ("8", 2, 1, 1, "number"),
    ("9", 2, 2, 1, "number"), ("×", 2, 3, 1, "operator"),

    ("4", 3, 0, 1, "number"), ("5", 3, 1, 1, "number"),
    ("6", 3, 2, 1, "number"), ("-", 3, 3, 1, "operator"),

    ("1", 4, 0, 1, "number"), ("2", 4, 1, 1, "number"),
    ("3", 4, 2, 1, "number"), ("+", 4, 3, 1, "operator"),

    ("0", 5, 0, 2, "number"), (".", 5, 2, 1, "number"),
    ("=", 5, 3, 1, "operator"),
]

# Keyboard keys -> button text
KEY_MAP = {
    "+": "+", "-": "-", "*": "×", "/": "÷", "^": "^", "%": "mod",
    "=": "=", ".": ".", ",": ".", "c": "C", "C": "C", "r": "√",
}
SPECIAL_KEY_MAP = {
    "Return": "=", "KP_Enter": "=", "BackSpace": "⌫",
    "Escape": "C", "Delete": "C",
}
DIGITS = set("0123456789")


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.calculator = Calculator()

        root.title("Calculator")
        root.configure(bg=BACKGROUND)
        root.resizable(False, False)

        # Buttons that are not digits or operators, linked to their action.
        c = self.calculator
        self.actions = {
            "=": c.press_equals,
            ".": c.press_dot,
            "C": c.clear,
            "⌫": c.backspace,
            "±": c.press_negate,
            "%": c.press_percent,
            "√": c.press_square_root,
        }

        left = tk.Frame(root, bg=BACKGROUND)
        left.grid(row=0, column=0, padx=(12, 6), pady=12)
        right = tk.Frame(root, bg=BACKGROUND)
        right.grid(row=0, column=1, padx=(6, 12), pady=12, sticky="ns")

        self._build_display(left)
        self._build_buttons(left)
        self._build_history(right)

        root.bind("<Key>", self._on_key)
        self._refresh()

    # -- building the window ------------------------------------------------

    def _build_display(self, parent):
        # width=1 stops long text from stretching the window.
        self.expression_label = tk.Label(
            parent, text="", anchor="e", width=1,
            bg=BACKGROUND, fg=MUTED_TEXT, font=(FONT, 12),
        )
        self.expression_label.grid(row=0, column=0, columnspan=4,
                                   sticky="ew", padx=6, pady=(4, 0))

        self.display_label = tk.Label(
            parent, text="0", anchor="e", width=1,
            bg=BACKGROUND, fg=TEXT, font=(FONT, 32),
        )
        self.display_label.grid(row=1, column=0, columnspan=4,
                                sticky="ew", padx=6, pady=(0, 10))

    def _build_buttons(self, parent):
        for column in range(4):
            parent.grid_columnconfigure(column, weight=1, uniform="buttons")

        for text, row, column, span, style in BUTTONS:
            colors = STYLES[style]
            button = tk.Button(
                parent, text=text, width=5, height=2,
                font=(FONT, 16), relief="flat", bd=0, cursor="hand2",
                takefocus=False,
                bg=colors["bg"], fg=colors["fg"],
                activebackground=colors["hover"], activeforeground=colors["fg"],
                command=lambda t=text: self._on_button(t),
            )
            button.grid(row=row + 2, column=column, columnspan=span,
                        sticky="nsew", padx=3, pady=3)
            # Change color when the mouse is over the button.
            button.bind("<Enter>", lambda e, b=button, c=colors: b.config(bg=c["hover"]))
            button.bind("<Leave>", lambda e, b=button, c=colors: b.config(bg=c["bg"]))

    def _build_history(self, parent):
        tk.Label(parent, text="History", anchor="w",
                 bg=BACKGROUND, fg=MUTED_TEXT, font=(FONT, 12)).pack(fill="x")

        self.history_list = tk.Listbox(
            parent, width=26, height=10,
            bg="#2c2c2e", fg=TEXT, font=(FONT, 10),
            bd=0, highlightthickness=0, activestyle="none",
            selectbackground="#3a3a3c", selectforeground=TEXT,
        )
        self.history_list.pack(fill="both", expand=True, pady=6)

        tk.Button(
            parent, text="Clear history", command=self._clear_history,
            bg=STYLES["function"]["bg"], fg=TEXT, relief="flat", bd=0,
            activebackground=STYLES["function"]["hover"], activeforeground=TEXT,
            font=(FONT, 10), cursor="hand2", takefocus=False, pady=4,
        ).pack(fill="x")

    # -- reacting to the user -----------------------------------------------

    def _on_button(self, text):
        """Called when a button is clicked (or the matching key is pressed)."""
        if text in DIGITS:
            self.calculator.press_digit(text)
        elif text in OPERATIONS or text in OPERATOR_ALIASES:
            self.calculator.press_operator(text)
        elif text in self.actions:
            self.actions[text]()
        self._refresh()

    def _on_key(self, event):
        if event.char in DIGITS:
            self._on_button(event.char)
        elif event.keysym in SPECIAL_KEY_MAP:
            self._on_button(SPECIAL_KEY_MAP[event.keysym])
        elif event.char in KEY_MAP:
            self._on_button(KEY_MAP[event.char])

    def _clear_history(self):
        self.calculator.clear_history()
        self._refresh()

    # -- updating what the user sees ----------------------------------------

    @staticmethod
    def _font_size(text):
        """Smaller text for long numbers so they always fit."""
        if len(text) <= 9:
            return 32
        if len(text) <= 12:
            return 24
        if len(text) <= 16:
            return 18
        return 14

    def _refresh(self):
        calculator = self.calculator
        self.expression_label.config(text=calculator.expression)
        self.display_label.config(
            text=calculator.display,
            font=(FONT, self._font_size(calculator.display)),
        )

        self.history_list.delete(0, tk.END)
        for entry in reversed(calculator.history):  # newest first
            self.history_list.insert(tk.END, entry)


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
