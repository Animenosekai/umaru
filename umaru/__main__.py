"""
Umaru

The command line interface for Umaru — A pro controller driver

Copyright
---------
Animenosekai
    MIT License
"""

import typing
import shutil
import queue
import threading
import argparse
import pathlib

import rich.console
import rich.progress
import rich.status
import rich.table
import rich.live
import rich.layout
from pynput import keyboard, mouse
# import notifypy

import umaru
from umaru import umaru_keyboard


def notify(msg: str):
    return
    notification = notifypy.Notify()

    notification.title = "Umaru"
    notification.message = str(msg)

    notification.icon = str((pathlib.Path(__file__).parent.parent / "yay.png").absolute())

    notification.send()


def sanitizer(el: typing.Any):
    """
    Sanitizes the input element to conform to a special string style

    Parameters
    ----------
    el: typing.Any
    """
    if not el:
        return ""
    return str(el).lower().replace(" ", "")


class Event:
    """
    A class representing an event
    """

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
        """
        return "{}()".format(self.__class__.__name__)


class TableDirection(Event):
    """Moving in the table"""


class TableUp(TableDirection):
    """Moving up in the table"""


class TableDown(TableDirection):
    """Moving down in the table"""


class Filter(Event):
    """
    Changing the results filter
    """

    def __init__(self, query: typing.Optional[str] = "") -> None:
        """
        Parameters
        ----------
        query: typing.Optional[str], default = ""

        Returns
        -------
        None
        """
        super().__init__()
        self.query = query or ""

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
        """
        return "Filter('{}')".format(self.query)


class Select(Event):
    """When a device is selected"""


def input_loop(input_queue: queue.Queue, default_filter: typing.Optional[str] = None):
    """
    A loop to check for user input

    Parameters
    ----------
    input_queue: queue.Queue
    default_filter: typing.Optional[str], default = None
    """
    with keyboard.Events() as events:
        query = default_filter or ""
        for event in events:
            if isinstance(event, keyboard.Events.Release):
                continue
            if event.key == keyboard.Key.enter:
                input_queue.put(Select())
            elif event.key == keyboard.Key.backspace:
                query = query[:-1]
                input_queue.put(Filter(query))
            elif event.key == keyboard.Key.space:
                query += " "
                input_queue.put(Filter(query))
            elif event.key == keyboard.Key.up:
                input_queue.put(TableUp())
            elif event.key == keyboard.Key.down:
                input_queue.put(TableDown())
            elif event.key and event.key.char:
                query += str(event.key.char)
                input_queue.put(Filter(query=query))


def reduce_devices(devices: list[umaru.Device], query: typing.Optional[str] = None):
    """
    Reduces the number of devices shown

    Parameters
    ----------
    devices: list[umaru.Device]
    query: typing.Optional[str], default = None
    """
    if query:
        query = sanitizer(query)
    return [
        device
        for device in devices
        if not query or
        (query in sanitizer(device.name)
         or query in sanitizer(device.manufacturer)
         or query in sanitizer(device.serial_number))
    ]


def create_table(devices: list[umaru.Device], current_device: int = 0, limit: typing.Optional[int] = None):
    """
    Creates a table element, containing the formatted devices

    Parameters
    ----------
    devices: list[umaru.Device]
    query: typing.Optional[str], default = None
    limit: typing.Optional[int], default = None
    current_device: int, default = 0
    """
    limit = limit or (shutil.get_terminal_size().lines - 5)

    table = rich.table.Table()
    table.add_column("Device")
    table.add_column("Manufacturer")
    table.add_column("Serial Number")

    devices = sorted(devices, key=lambda d: (d.name, d.manufacturer, d.serial_number))

    items = 0
    skip_count = max(current_device - limit + 1, 0)
    for device in devices:
        if skip_count > 0:
            skip_count -= 1
            current_device -= 1
            continue
        if current_device == items:
            table.add_row(f"[green]{device.name}", f"[green]{device.manufacturer}", f"[green]{device.serial_number}")
        else:
            table.add_row(device.name, device.manufacturer, device.serial_number)
        items += 1
        if items >= limit:
            break
    return table


def main(default_filter: typing.Optional[str] = None):
    """
    The main execution flow

    Parameters
    ----------
    default_filter: typing.Optional[str], default = None
    """
    layout = rich.layout.Layout()

    layout.split_column(
        rich.layout.Layout(name="upper"),
        rich.layout.Layout(name="lower")
    )

    overall_progress = rich.progress.Progress(*(
        rich.progress.SpinnerColumn(),
        rich.progress.TextColumn("[progress.description]{task.description}"),
        rich.progress.TextColumn("—"),
        rich.progress.TimeElapsedColumn()),
        transient=True)

    devices = reduce_devices(umaru.pairable_devices(), query=default_filter)
    if len(devices) != 1:
        layout["upper"].update(create_table(devices=devices))
        layout["lower"].update(overall_progress)
        layout["lower"].size = 1

        current_device_index = 0
        current_filter = default_filter or ""

        overall_task = overall_progress.add_task("Searching for a controller" if not current_filter else "Filter: {}".format(current_filter))
        overall_progress.update(overall_task)

        input_queue = queue.Queue()
        threading.Thread(target=input_loop, args=(input_queue, default_filter), daemon=True).start()

        with rich.live.Live(layout, refresh_per_second=10, transient=True):  # 60 fps yay
            while True:
                previous_devices = devices
                devices = reduce_devices(umaru.pairable_devices(), query=current_filter)
                try:
                    new_input = input_queue.get_nowait()
                    # with open("tests", "a") as f:
                    #     f.write(str(current_device_index) + "\n")
                    if isinstance(new_input, Select):
                        selected_device = previous_devices[current_device_index]
                        break
                    elif isinstance(new_input, Filter):
                        current_filter = new_input.query
                        if current_filter:
                            overall_progress.update(overall_task, description="Filter: {}".format(current_filter))
                        else:
                            overall_progress.update(overall_task, description="Searching for a controller")
                    elif isinstance(new_input, TableUp):
                        current_device_index = max(current_device_index - 1, 0)
                    elif isinstance(new_input, TableDown):
                        current_device_index = min(current_device_index + 1, len(devices) - 1)
                except Exception:
                    pass

                layout["upper"].update(create_table(devices=devices, current_device=current_device_index))
    else:
        selected_device = devices[0]

    with rich.progress.Progress(*(
            rich.progress.SpinnerColumn(),
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.TextColumn("—"),
            rich.progress.TimeElapsedColumn()),
            transient=True) as progress:
        progress.add_task("Connecting to the controller")
        if selected_device.name:
            selection = selected_device.name
            if selected_device.manufacturer:
                selection += " by {}".format(selected_device.manufacturer)
            if selected_device.serial_number:
                selection += " ({})".format(selected_device.serial_number)
        elif selected_device.manufacturer:
            selection = "Product by {}".format(selected_device.manufacturer)
            if selected_device.serial_number:
                selection += " ({})".format(selected_device.serial_number)
        elif selected_device.serial_number:
            selection = "Product {}".format(selected_device.serial_number)
        else:
            selection = "{}:{}".format(selected_device.vendor_id, selected_device.product_id)
        progress.console.print("[green][✓] Selected: {}".format(selection))

        gamepad = umaru.open_connection(selected_device)

    def list_repr(current, old):
        results = []
        for index, element in enumerate(current):
            try:
                old_element = old[index]
            except Exception:
                old_element = 0
            if element - old_element <= 5:
                results.append(f"[red]{str(element).zfill(3)}[/red]")
            else:
                results.append(f"[green]{str(element).zfill(3)}[/green]")
        return "[" + ", ".join(results) + "]"

    with rich.progress.Progress(*(
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.TextColumn("—"),
            rich.progress.TimeElapsedColumn()),
            transient=True) as progress:
        progress.add_task("[green][✓] Connected")
        progress.console.print("[ℹ] Press [magenta]CTRL+C[/magenta] or the [magenta]right and left[/magenta] stick simultaneously to quit")
        notify("Connected to a Pro Controller")

        last_share = False
        last_a = False
        last_b = False
        last_l = False
        last_r = False
        last_zr = False
        last_home = False
        last_plus = False
        last_minus = False
        last_up = False
        last_down = False
        last_left = False
        last_right = False
        last = None

        # last_state = umaru.ControllerData([0] * 13)
        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()

        def pressing(key):
            keyboard_controller.press(key)
            keyboard_controller.release(key)

        keyboard_viewer = None
        captured = True

        while True:
            # report = gamepad.read(64)
            try:
                report = gamepad.read(13)
                data = umaru.ControllerData(report)

                # progress.console.print(data)
                if data.buttons.sticks.LEFT and data.buttons.sticks.RIGHT:
                    return

                if data.buttons.SHARE != last_share and data.buttons.SHARE:
                    if keyboard_viewer:
                        umaru_keyboard.destroy(keyboard_viewer)
                        keyboard_viewer = None
                    else:
                        progress.console.print("[ℹ] Bringing up the virtual keyboard")
                        keyboard_viewer = umaru_keyboard.create_window()
                        with keyboard_controller.pressed(keyboard.Key.cmd):
                            keyboard_controller.press(keyboard.Key.tab)
                            keyboard_controller.release(keyboard.Key.tab)

                if last_home != data.buttons.HOME and data.buttons.HOME:
                    with keyboard_controller.pressed(keyboard.Key.cmd):
                        keyboard_controller.press(keyboard.Key.space)
                    captured = True

                if last_plus != data.buttons.PLUS and data.buttons.PLUS:
                    keyboard_controller.press(keyboard.Key.media_volume_up)

                if last_minus != data.buttons.MINUS and data.buttons.MINUS:
                    keyboard_controller.press(keyboard.Key.media_volume_down)

                keyboard_title = ["Umaru"]

                if keyboard_viewer is not None and captured:
                    # keyboard_viewer.app.update()

                    if last_up != data.buttons.directional.UP and data.buttons.directional.UP:
                        umaru_keyboard.move_on_keyboard(umaru_keyboard.Direction.UP, keyboard_viewer)
                    if last_down != data.buttons.directional.DOWN and data.buttons.directional.DOWN:
                        umaru_keyboard.move_on_keyboard(umaru_keyboard.Direction.DOWN, keyboard_viewer)
                    if last_left != data.buttons.directional.LEFT and data.buttons.directional.LEFT:
                        umaru_keyboard.move_on_keyboard(umaru_keyboard.Direction.LEFT, keyboard_viewer)
                    if last_right != data.buttons.directional.RIGHT and data.buttons.directional.RIGHT:
                        umaru_keyboard.move_on_keyboard(umaru_keyboard.Direction.RIGHT, keyboard_viewer)

                    # progress.console.print(keyboard_viewer.cursor.element)

                    if last_b != data.buttons.B and data.buttons.B:
                        pressing(keyboard.Key.backspace)

                    if last_zr != data.buttons.ZR and data.buttons.ZR:
                        captured = False

                    if data.buttons.L:
                        keyboard_controller.press(keyboard.Key.shift)

                    if data.buttons.ZL:
                        if keyboard_controller.shift_pressed:
                            keyboard_controller.release(keyboard.Key.shift)
                        else:
                            keyboard_controller.press(keyboard.Key.shift)

                    element: umaru_keyboard.KeyboardElement = keyboard_viewer.cursor.element
                    keyboard_title.append("`{}` selected".format(element))

                    if keyboard_controller.shift_pressed:
                        keyboard_title.append("⇧ Shifted")

                    if last_a != data.buttons.A and data.buttons.A:
                        # element: umaru_keyboard.KeyboardElement = keyboard_viewer.cursor.element

                        match element:
                            case umaru_keyboard.SpecialKey.ESC:
                                pressing(keyboard.Key.esc)
                            case umaru_keyboard.SpecialKey.TAB:
                                pressing(keyboard.Key.tab)
                            case umaru_keyboard.SpecialKey.BACKSPACE:
                                pressing(keyboard.Key.backspace)
                            case umaru_keyboard.SpecialKey.ENTER:
                                pressing(keyboard.Key.enter)
                            case umaru_keyboard.SpecialKey.CAPS_LOCK:
                                keyboard_controller.press(keyboard.Key.shift)
                            case umaru_keyboard.SpecialKey.SHIFT:
                                pressing(keyboard.Key.shift_l)
                            case umaru_keyboard.SpecialKey.RIGHT_SHIFT:
                                pressing(keyboard.Key.shift_r)
                            case umaru_keyboard.SpecialKey.CONTROL:
                                pressing(keyboard.Key.ctrl)
                            case umaru_keyboard.SpecialKey.CMD:
                                pressing(keyboard.Key.cmd)
                            case umaru_keyboard.SpecialKey.SPACE:
                                pressing(keyboard.Key.space)
                            case _:
                                pressing(element)

                    if data.buttons.L:
                        keyboard_controller.release(keyboard.Key.shift)

                    keyboard_viewer.app.update()
                else:
                    if data.buttons.A != last_a and data.buttons.A:
                        mouse_controller.press(mouse.Button.left)
                    elif data.buttons.A != last_a and not data.buttons.A:
                        mouse_controller.release(mouse.Button.left)

                    if data.buttons.B != last_b and data.buttons.B:
                        mouse_controller.press(mouse.Button.right)
                    elif data.buttons.B != last_b and not data.buttons.B:
                        mouse_controller.release(mouse.Button.right)

                    if data.buttons.L:
                        factor = 10
                    elif data.buttons.ZL:
                        factor = 1
                    else:
                        factor = 5

                    if last_zr != data.buttons.ZR and data.buttons.ZR:
                        captured = True

                    dy = -factor if data.buttons.directional.UP else 0
                    dy += factor if data.buttons.directional.DOWN else 0
                    dy -= int(factor * data.left_stick.y)

                    dx = -factor if data.buttons.directional.LEFT else 0
                    dx += factor if data.buttons.directional.RIGHT else 0

                    if dy or dx:
                        mouse_controller.move(dx, dy)

                    mouse_controller.scroll(dx=0, dy=int(factor * data.right_stick.y))

                if keyboard_viewer is not None:
                    if captured:
                        keyboard_title.append("Captured")
                    else:
                        keyboard_title.append("Not Captured")

                    keyboard_viewer.app.title(" - ".join(keyboard_title))
                    keyboard_viewer.app.update()

                last_share = data.buttons.SHARE
                last_a = data.buttons.A
                last_b = data.buttons.B
                last_l = data.buttons.L
                last_r = data.buttons.R
                last_zr = data.buttons.ZR
                last_home = data.buttons.HOME
                last_plus = data.buttons.PLUS
                last_minus = data.buttons.MINUS
                last_up = data.buttons.directional.UP
                last_down = data.buttons.directional.DOWN
                last_left = data.buttons.directional.LEFT
                last_right = data.buttons.directional.RIGHT

                # if report:
                #     # data from the controller
                #     if report != last:
                #         progress.console.print(list_repr(report, last))
                #         last = report
            except Exception:
                # progress.console.print_exception()
                pass


def entry():
    """The CLI entrypoint"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", "-f", help="The default filter. Can be used to skip the controller discovery step.",
                        required=False, default=None, type=str)
    args = parser.parse_args()
    main(default_filter=args.filter)


if __name__ == "__main__":
    entry()
