# Umaru

<img align="right" src="./assets/umaru.png" height="220px">

***A small Switch Pro Controller driver which lets you use your computer with it !***

<br>
<br>

[![PyPI version](https://badge.fury.io/py/umaru.svg)](https://pypi.org/project/umaru/)
[![Downloads](https://static.pepy.tech/personalized-badge/umaru?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/umaru)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/umaru)](https://pypistats.org/packages/umaru)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/umaru)](https://pypi.org/project/umaru/)
[![PyPI - Status](https://img.shields.io/pypi/status/umaru)](https://pypi.org/project/umaru/)
[![GitHub - License](https://img.shields.io/github/license/Animenosekai/umaru)](https://github.com/Animenosekai/umaru/blob/master/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/Animenosekai/umaru)](https://github.com/Animenosekai/umaru)
[![CodeQL Checks Badge](https://github.com/Animenosekai/umaru/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Animenosekai/umaru/actions/workflows/codeql-analysis.yml)
![Code Size](https://img.shields.io/github/languages/code-size/Animenosekai/umaru)
![Repo Size](https://img.shields.io/github/repo-size/Animenosekai/umaru)
![Issues](https://img.shields.io/github/issues/Animenosekai/umaru)

## Index

- [Index](#index)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Installing](#installing)
  - [Option 1: From PyPI](#option-1-from-pypi)
  - [Option 2: From Git](#option-2-from-git)
- [Usage](#usage)
  - [Select your device](#select-your-device)
  - [Use your controller](#use-your-controller)
  - [Quitting Umaru](#quitting-umaru)

## Features

- A cool looking Bluetooth device selection screen
- Control your mouse using your controller
- Use a virtual keyboard with your controller

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need Python 3 to use this module

```bash
# vermin output
Minimum required versions: 3.7
Incompatible versions:     2
```

## Installing

### Option 1: From PyPI

```bash
pip install --upgrade umaru
```

> This will install the latest stable version from PyPI

### Option 2: From Git

```bash
pip install --upgrade git+https://github.com/Animenosekai/umaru.git
```

> This will install the latest development version from the git repository

You can check if you successfully installed it by printing out its version:

```bash
$ umaru --version
1.0
```

## Usage

```bash
usage: umaru [-h] [--filter FILTER]

options:
  -h, --help            show this help message and exit
  --filter FILTER, -f FILTER
                        The default filter. Can be used to skip the controller discovery step.
```

You can use the `--filter` parameter to give a default filter for the discovery step, which automatically selects the controller if it is the only result which comes up.

If you are using `umaru` for the first time, I would recommend using the interactive discovery window first:

Start by running *umaru*

```bash
umaru
```

### Select your device

You should see the device discovery scene appear :

```bash
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓                                                                                            
┃ Device                             ┃ Manufacturer ┃ Serial Number         ┃                                                                                            
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩                                                                                            
│                                    │ Apple        │                       │                                                                                            
│                                    │ Apple        │                       │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ Apple Internal Keyboard / Trackpad │ Apple Inc.   │ FM70*************+F** │                                                                                            
│ BTM                                │ APPL         │                       │                                                                                            
│ Headset                            │ Apple        │                       │                                                                                            
│ Keyboard Backlight                 │              │                       │                                                                                            
└────────────────────────────────────┴──────────────┴───────────────────────┘                                                                                            
                                                                                                                                                                         
                                                                                                                                                                         
                                                                                                                                                                         
⠴ Searching for a controller — 0:00:07                                                                      
```

Here, you can search your Switch Pro Controller using the arrows on your keyboard. You can also filter the results by typing a keyword.

```bash
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓                                                                                                                    
┃ Device         ┃ Manufacturer ┃ Serial Number     ┃                                                                                                                    
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩                                                                                                                    
│ Pro Controller │              │ 58:**:**:**:**:D9 │                                                                                                                    
└────────────────┴──────────────┴───────────────────┘                                                                                                                    
                                                                                                                                                                                                                                                                                                                                       
⠸ Filter: pro — 0:00:13                                             
```

Press **ENTER** to select the device.

### Use your controller

It should now connect to your controller.

- You can use the directional pad (the arrows) to move your cursor
- You can use the `A` button to left-click
- You can use the `B` button to right-click
- You can use the left stick to move the cursor up and down
- You can use the right stick to scroll
- You can use the share button (the square with a square in it) to bring up the virtual keyboard
  - With the keyboard opened you can use the `ZR` button to capture or remove the controller capturing : this switches if the controller controls the mouse or the keyboard.
  - When captured, you can use the directional pad (the arrows) to move around the keys
  - When captured, you can use the `A` button to press a key, `B` to delete
  - The capture also releases the scroll, which is might act weird if the controller is not captured by the keyboard
  - You can press the share button again to remove the capture and close the virtual keyboard

### Quitting Umaru

Go back to your terminal and press `CTRL+C` or just press the left and right stick at the same time to quit `umaru`