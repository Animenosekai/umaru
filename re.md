# Reverse engineering the Nintendo Switch Pro Controller HID signal

```swift
report = 
[048, 108, 096, 000, 000, 000, 056, 088, 118, 207, 231, 127, 009, 000, 000, 000]
~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~~~~^~
   0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
```

|  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9 | 10 | 11 | 12 | 13 | 14 | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- | -- | -- | -- | -- | -- | -- |
| [Unknown](#unknown) | [Timestamp](#the-timestamp) | *Unknown* | [Right Buttons](#right-buttons) | [Middle Buttons](#middle-buttons) | [Left Buttons](#left-buttons) | *Unknown* | *Unknown* | [Left Stick](#left-stick) | *Unknown* | *Unknown* | [Right Stick](#right-stick) | *Unknown* | *Unknown* | *Unknown* | *Unknown* |

## Index

- [Index](#index)
- [Unknown](#unknown)
- [The timestamp](#the-timestamp)
- [Bitmasks](#bitmasks)
  - [Right buttons](#right-buttons)
  - [Middle buttons](#middle-buttons)
  - [Left buttons](#left-buttons)
- [Analog Sticks](#analog-sticks)
  - [Left Stick](#left-stick)
  - [Right Stick](#right-stick)
- [Implementation](#implementation)

## Unknown

> `report[0]`

The first slot doesn't seem to be reporting anything useful on the controller (?)

> **Note**  
> Might be the battery ?

## The timestamp

> `report[1]`

This slot reports a timestamp and increases independently of user actions.

Ranges from 0 to 255, by 3 on each update.

## Bitmasks

### Right buttons

> `report[3]`

This is a bitmask reporting on the current right buttons pressing state.

***Bitmask Sheet***

| Value          | Name       |
| -------------- | ---------- |
| `0b00000001`   | Y-Button   |
| `0b00000010`   | X-Button   |
| `0b00000100`   | B-Button   |
| `0b00001000`   | A-Button   |
| `0b01000000`   | R-Button   |
| `0b10000000`   | ZR-Button  |

### Middle buttons

> `report[4]`

This is a bitmask reporting on the current middle buttons pressing state.

***Bitmask Sheet***

| Value          | Name          |
| -------------- | ------------- |
| `0b00000001`   | Minus         |
| `0b00000010`   | Plus          |
| `0b00000100`   | Right Stick   |
| `0b00001000`   | Left Stick    |
| `0b00010000`   | Home Button   |
| `0b00100000`   | Share Button  |

### Left buttons

> `report[5]`

This is a bitmask reporting on the current left buttons pressing state.

***Bitmask Sheet***

| Value          | Name         |
| -------------- | ------------ |
| `0b00000001`   | *Down D*-Pad   |
| `0b00000010`   | *Up D*-Pad     |
| `0b00000100`   | *Right D*-Pad  |
| `0b00001000`   | *Left D*-Pad   |
| `0b01000000`   | *L* Button     |
| `0b10000000`   | *ZL* Button    |

## Analog Sticks

### Left Stick

> `report[8]`

Ranges from 23 (bottom) to 226 (up)


### Right Stick

> `report[11]`

Ranges from 31 (bottom) to 227 (up)

## Implementation

Here is the parser used by `umaru` to use those values:

<https://github.com/Animenosekai/umaru/blob/57c7d74f2a9a5831a90d0d9aa06b4b40d75db880/umaru/umaru.py#L105-L234>