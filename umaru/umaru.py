"""
umaru.py

Core internals for umaru
"""

import dataclasses
from typing import Optional

import hid


@dataclasses.dataclass
class RawDeviceData:
    """
    Represents the raw data returned by `hid.enumetate`
    """
    vendor_id: str
    product_id: str
    path: Optional[str] = None
    serial_number: Optional[str] = None
    release_number: Optional[str] = None
    manufacturer_string: Optional[str] = None
    product_string: Optional[str] = None
    usage_page: Optional[str] = None
    usage: Optional[str] = None
    interface_number: Optional[str] = None


class Device():
    """
    Represents a pairable controller device

    This is a high level interface
    """

    def __init__(self, data: RawDeviceData):
        """
        Parameters
        ----------
        data: RawDeviceData
        """
        self._raw = data
        self.path = data.path
        self.name = data.product_string
        self.serial_number = data.serial_number
        self.product_id = data.product_id
        self.vendor_id = data.vendor_id
        self.manufacturer = data.manufacturer_string

    def open(self):
        """
        Returns an opened connection to the device
        """
        return open_connection(self)


def pairable_devices() -> list[Device]:
    """
    Returns the currently available devices

    Returns
    -------
    list[Device]
    """
    return [Device(data=RawDeviceData(**d)) for d in hid.enumerate()]


def open_connection(device: Device):
    """
    Opens a connection to the given device

    Parameters
    ----------
    device: Device
    """
    gamepad = hid.device()
    if device.path:
        gamepad.open_path(device.path)
    else:
        gamepad.open(device.vendor_id, device.product_id)
    gamepad.set_nonblocking(True)
    return gamepad


class ControllerButtons:
    """The controller buttons representation"""
    def __repr__(self) -> str:
        results = []
        for attr in dir(self):
            attr = str(attr)
            if attr.startswith("__"):
                continue
            content = getattr(self, attr)
            if callable(content):
                continue
            if content:
                if isinstance(content, ControllerButtons):
                    results.append(str(content))
                else:
                    results.append(attr)
        return f"{self.__class__.__name__}({', '.join(results)})"


class ControllerData:
    """
    Represents the data coming from the controller
    """

    class Buttons(ControllerButtons):
        """The different buttons on the controller"""
        class DirectionalPad(ControllerButtons):
            """Represents a directional pad on the controller"""

            def __init__(self, bitmask: int = 0) -> None:
                def check_bitmask(bit: int = 0):
                    return bool(bit & bitmask)

                self.DOWN = check_bitmask(0b00000001)
                """If the down button is pressed"""
                self.UP = check_bitmask(0b00000010)
                """If the up button is pressed"""
                self.RIGHT = check_bitmask(0b00000100)
                """If the right button is pressed"""
                self.LEFT = check_bitmask(0b00001000)
                """If the left button is pressed"""
        class Stick(ControllerButtons):
            """Represents a stick on the controller"""

            def __init__(self, bitmask: int = 0) -> None:
                def check_bitmask(bit: int = 0):
                    return bool(bit & bitmask)

                self.RIGHT = check_bitmask(0b00000100)
                """If the right stick is pressed"""
                self.LEFT = check_bitmask(0b00001000)
                """If the left stick is pressed"""

        def __init__(self, left: int = 0, middle: int = 0, right: int = 0) -> None:
            # Right buttons
            def check_right(bit: int = 0):
                return bool(bit & right)

            self.Y = check_right(0b00000001)
            """If the Y button is pressed"""
            self.X = check_right(0b00000010)
            """If the X button is pressed"""
            self.B = check_right(0b00000100)
            """If the B button is pressed"""
            self.A = check_right(0b00001000)
            """If the A button is pressed"""
            self.R = check_right(0b01000000)
            """If the R button is pressed"""
            self.ZR = check_right(0b10000000)
            """If the ZR button is pressed"""

            # Middle buttons
            def check_middle(bit: int = 0):
                return bool(bit & middle)

            self.MINUS = check_middle(0b00000001)
            """If the - button is pressed"""
            self.PLUS = check_middle(0b00000010)
            """If the + button is pressed"""
            self.sticks = self.Stick(middle)
            """If the sticks are pressed"""
            self.HOME = check_middle(0b00010000)
            """If the HOME button is pressed"""
            self.SHARE = check_middle(0b00100000)
            """If the share button is pressed"""

            # Left buttons
            def check_left(bit: int = 0):
                return bool(bit & left)

            self.directional = self.DirectionalPad(left)
            """The different directional pad buttons"""
            self.L = check_left(0b01000000)
            """If the L button is pressed"""
            self.ZL = check_left(0b10000000)
            """If the ZL button is pressed"""

    class AnalogStick:
        """Represents an analog stick"""
        BOTTOM: int
        """The bottom position value"""
        UP: int
        """The up position value"""

        def __init__(self, y: int) -> None:
            self.range_center = ((self.UP + self.BOTTOM) / 2)
            self.y = (y - self.range_center) / self.range_center

        def __repr__(self) -> str:
            return "{}(y={})".format(self.__class__.__name__, self.y)

    class LeftStick(AnalogStick):
        """Represents the left stick"""
        BOTTOM = 25
        # BOTTOM = 23
        # UP = 226
        UP = 225

        def __init__(self, y: int) -> None:
            super().__init__(y)

    class RightStick(AnalogStick):
        """Represents the right stick"""
        BOTTOM = 25
        # BOTTOM = 31
        # UP = 227
        UP = 225

        def __init__(self, y: int) -> None:
            super().__init__(y)

    def __init__(self, data: list[int]) -> None:
        """
        Parameters
        ----------
        data: list[int]

        Returns
        -------
        None
        """
        self.buttons = self.Buttons(
            left=data[5],
            middle=data[4],
            right=data[3]
        )

        self.left_stick = self.LeftStick(data[8])
        self.right_stick = self.RightStick(data[11])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.buttons}, {self.left_stick}, {self.right_stick})"
