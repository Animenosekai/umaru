"""
A virtual keyboard viewer for Umaru
"""

import tkinter as tk
import enum
import dataclasses
import typing
import collections


class SpecialKey(enum.Enum):
    """All of the special keys on the keyboard"""
    ESC = "esc"
    POWER = "🍡"
    TAB = "TAB"
    BACKSPACE = "DEL"
    ENTER = "ENTER"
    CAPS_LOCK = "CAPS LOCK"
    SHIFT = "SHIFT"
    RIGHT_SHIFT = "R SHIFT"
    FN = "🌐"
    CONTROL = "ctrl"
    OPTION = "⌥"
    CMD = "⌘"
    SPACE = "SPACE"


# type alias
KeyboardElement = typing.Union[str, SpecialKey]
Keyboard = typing.List[typing.List[KeyboardElement]]


@dataclasses.dataclass
class Cursor:
    """Represents the current cursor position on the keyboard"""
    x: int = 0
    y: int = 0
    element: KeyboardElement = SpecialKey.SPACE


class Direction(enum.Enum):
    """A direction on the keyboard"""
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


KeyboardViewer = collections.namedtuple("KeyboardViewer", ["app", "buttons", "cursor", "keyboard"])

AZERTY = [
    [SpecialKey.ESC, *[f"F{i}" for i in range(1, 13)], SpecialKey.POWER],
    [*"@&é\"'(§è!çà)-", SpecialKey.BACKSPACE],
    [SpecialKey.TAB, *"azertyuiop^$", SpecialKey.ENTER],
    [SpecialKey.CAPS_LOCK, *"qsdfghjklmù"],
    [SpecialKey.SHIFT, *"<wxcvbn,;:=", SpecialKey.RIGHT_SHIFT],
    [SpecialKey.FN, SpecialKey.CONTROL, SpecialKey.OPTION, SpecialKey.CMD, SpecialKey.SPACE, SpecialKey.CMD, SpecialKey.OPTION]
]


# pylint: disable=W0102
def create_window(keyboard: Keyboard = AZERTY):
    """
    Creates a keyboard window

    Returns
    (Tk, list[Button], Cursor)

    Parameters
    ----------
    keyboard: Keyboard, default = AZERTY

    Returns
    -------
    KeyboardViewer
    """
    # Create object

    # root = tk.Toplevel()
    root = tk.Tk()
    root.title("Umaru Keyboard")

    # Adjust size
    root.geometry("800x300")

    root.attributes("-topmost", True)

    buttons = []

    for row, line in enumerate(keyboard):
        tk.Grid.rowconfigure(root, row, weight=1)
        column_push = 0
        for column, button in enumerate(line):
            tk.Grid.columnconfigure(root, column, weight=1)
            new_button = tk.Button(root, text=button.value if isinstance(button, SpecialKey) else str(button))
            match button:
                # case SpecialKey.POWER:
                #     # might be half the size
                #     pass
                case SpecialKey.TAB:
                    new_button.grid(row=row, column=column, sticky="NSEW", columnspan=2)
                    column_push += 1
                case SpecialKey.BACKSPACE:
                    new_button.grid(row=row, column=column, sticky="NSEW", columnspan=2)
                    column_push += 1
                case SpecialKey.ENTER:
                    new_button.grid(row=row, column=column, sticky="NSEW", rowspan=2)
                case SpecialKey.CAPS_LOCK:
                    new_button.grid(row=row, column=column, sticky="NSEW", columnspan=2)
                    column_push += 1
                # case SpecialKey.SHIFT:
                #     pass
                case SpecialKey.RIGHT_SHIFT:
                    new_button.grid(row=row, column=column, sticky="NSEW", columnspan=3)
                    column_push += 2
                # case SpecialKey.FN:
                #     pass
                # case SpecialKey.CONTROL:
                #     pass
                # case SpecialKey.OPTION:
                #     pass
                # case SpecialKey.CMD:
                #     pass
                case SpecialKey.SPACE:
                    new_button.grid(row=row, column=column, sticky="NSEW", columnspan=7)
                    column_push += 6
                case _:
                    new_button.grid(row=row, column=column + column_push, sticky="NSEW")

            buttons.append(new_button)

    return KeyboardViewer(app=root, buttons=buttons, cursor=Cursor(element=keyboard[0][0]), keyboard=keyboard)


def move_on_keyboard(direction: Direction, keyboard: KeyboardViewer):
    """
    Parameters
    ----------
    direction: Direction
    buttons: typing.List[tk.Button]
    cursor: Cursor
    keyboard: Keyboard
    """
    maximum_len = 0
    for line in keyboard.keyboard:
        maximum_len = max(maximum_len, len(line) - 1)

    match direction:
        case Direction.UP:
            keyboard.cursor.y = max(0, keyboard.cursor.y - 1)
        case Direction.DOWN:
            keyboard.cursor.y = min(len(keyboard.keyboard) - 1, keyboard.cursor.y + 1)
        case Direction.LEFT:
            keyboard.cursor.x = max(0, keyboard.cursor.x - 1)
        case Direction.RIGHT:
            keyboard.cursor.x = min(maximum_len, keyboard.cursor.x + 1)

    current = 0
    for row, line in enumerate(keyboard.keyboard):
        current_cursor_x = min(len(line) - 1, keyboard.cursor.x)
        for column, button in enumerate(line):
            if current_cursor_x == column and keyboard.cursor.y == row:
                keyboard.cursor.x = current_cursor_x
                # print(keyboard.cursor)
                keyboard.cursor.element = button
                # keyboard.buttons[current]["background"] = "#222"
                keyboard.buttons[current].configure(fg="red", bg="red", background="red", activebackground="red",
                                                    activeforeground="red", state="active")
            else:
                keyboard.buttons[current].configure(fg="black", bg="SystemButtonFace", background="SystemButtonFace", activebackground="SystemButtonFace",
                                                    activeforeground="black", state="normal")
                # keyboard.buttons[current]["background"] = "SystemButtonFace"
            current += 1

    keyboard.app.update()
    return keyboard.cursor


def destroy(keyboard: KeyboardViewer):
    """
    Destroying the given keyboard

    Parameters
    ----------
    app: tk.Tk
    """
    keyboard.app.attributes("-topmost", False)
    keyboard.app.destroy()
    # keyboard.app.unbind_all()
    keyboard.app.quit()
    keyboard.app.update()
