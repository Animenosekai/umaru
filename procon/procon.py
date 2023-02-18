"""
procon.py

Core internals for procon
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
        return "{}({})".format(self.__class__.__name__, ", ".join(results))


class ControllerData:
    """
    """

    class Buttons(ControllerButtons):
        class DirectionalPad(ControllerButtons):
            def __init__(self, bitmask: int = 0) -> None:
                def check_bitmask(bit: int = 0):
                    return bool(bit & bitmask)

                self.DOWN = check_bitmask(0b00000001)
                self.UP = check_bitmask(0b00000010)
                self.RIGHT = check_bitmask(0b00000100)
                self.LEFT = check_bitmask(0b00001000)

        class Stick(ControllerButtons):
            def __init__(self, bitmask: int = 0) -> None:
                def check_bitmask(bit: int = 0):
                    return bool(bit & bitmask)

                self.RIGHT = check_bitmask(0b00000100)
                self.LEFT = check_bitmask(0b00001000)

        def __init__(self, left: int = 0, middle: int = 0, right: int = 0) -> None:
            # Right buttons
            def check_right(bit: int = 0):
                return bool(bit & right)

            self.Y = check_right(0b00000001)
            self.X = check_right(0b00000010)
            self.B = check_right(0b00000100)
            self.A = check_right(0b00001000)
            self.R = check_right(0b01000000)
            self.ZR = check_right(0b10000000)

            # Middle buttons
            def check_middle(bit: int = 0):
                return bool(bit & middle)

            self.MINUS = check_middle(0b00000001)
            self.PLUS = check_middle(0b00000010)
            self.sticks = self.Stick(middle)
            self.HOME = check_middle(0b00010000)
            self.SHARE = check_middle(0b00100000)

            # Left buttons
            def check_left(bit: int = 0):
                return bool(bit & left)

            self.directional = self.DirectionalPad(left)
            self.L = check_left(0b01000000)
            self.ZL = check_left(0b10000000)

    class AnalogStick:
        BOTTOM: int
        UP: int

        def __init__(self, y: int) -> None:
            self.range_center = ((self.UP + self.BOTTOM) / 2)
            self.y = (y - self.range_center) / self.range_center

        def __repr__(self) -> str:
            return "{}(y={})".format(self.__class__.__name__, self.y)

    class LeftStick(AnalogStick):
        BOTTOM = 25
        # BOTTOM = 23
        # UP = 226
        UP = 225

        def __init__(self, y: int) -> None:
            super().__init__(y)

    class RightStick(AnalogStick):
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
        return "{}({}, {}, {})".format(self.__class__.__name__, self.buttons, self.left_stick, self.right_stick)
