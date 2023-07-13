<a id="readme-top"></a> 



<!-- PROJECT SUMMARY -->
<br />
<div align="center">
  <img src="https://github.com/Kieran-Lock/ConsoleGUI/blob/main/logo.png" alt="Logo">
  <br />
  <p align="center">
    A lightweight, expressive GUI framework for compatible terminals
    <br />
    <a href="https://github.com/Kieran-Lock/ConsoleGUI/blob/main/DOCUMENTATION.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#getting-started">Getting Started</a>
    ·
    <a href="#basic-usage">Usage</a>
    ·
    <a href="https://github.com/Kieran-Lock/ConsoleGUI/blob/main/DOCUMENTATION.md">Documentation</a>
    ·
    <a href="https://github.com/Kieran-Lock/ConsoleGUI/blob/main/LICENSE">License</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About the Project

ConsoleGUI is a lightweight GUI framework for compatible xterm terminals, allowing you to write complex terminal applications, with expressive, concise, and readable code.  
  
With zero external dependencies, and features including keyboard and mouse input, customizable event listeners, and multiple layer management, you can create and manage complex terminal GUIs with minimal overhead, all in Python.



<!-- GETTING STARTED -->
## Getting Started

ConsoleGUI is available on [PyPI](https://pypi.org/). To use it in your project, run:

```
pip install ConsoleGUI
```

To install specific previous versions, take a look at the version history, locate the version tag (vX.Y.Z), and run:

```
pip install ConsoleGUI==X.Y.Z
```



<!-- TROUBLE SHOOTING -->
## Trouble Shooting

ConsoleGUI uses xterm-specific control sequences. If ConsoleGUI is running incorrectly once installed, ensure that the terminal you are using has sufficient mouse-reporting and xterm support support.  
  
This framework has been tested using the default setup for [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/) on Windows 10, which uses an `xterm-256color` terminal by default.  
  
[Here](https://gist.github.com/justinmk/a5102f9a0c1810437885a04a07ef0a91) is a useful resource for xterm control sequences reference.



<!-- BASIC USAGE EXAMPLES -->
## Basic Usage

### Setting up the terminal

Use the `console_inputs` context manager to prepare the terminal for use with ConsoleGUI. This will handle the cleanup automatically.
```py
from consolegui import console_inputs


with console_inputs():
    ...
```
_Please note that there may sometimes be control sequence leakage when exiting your application. This is unavoidable (I am yet to find a solution), but will only happen once the application is exited, and for only very short periods of time._

### Reading console input

Use the `read_console` function to read both keyboard and mouse input from the console. View the [API summary](#api-summary) or [documentation](https://github.com/Kieran-Lock/ConsoleGUI/blob/main/DOCUMENTATION.md) for the possible events you can receieve from this function.
```py
from consolegui import console_inputs, read_console


with console_inputs():
    read_key = read_console()
    ...
```

Read repeated console input by placing this function in a loop.
```py
from consolegui import console_inputs, read_console


with console_inputs():
    while True:  # Or some other loop
        read_key = read_console()
        ...
```



<!-- COMPLEX USAGE EXAMPLES -->
## Complex Usage
For more complex use cases, it is best to organise your application using the `GUI` or `LayeredGUI` classes. Some of the benefits of this approach are:  
* Easier & Customizable Event Listeners
* Layer Management
* Simplified GUI Manipulation

### Creating a GUI

You can  create a simple GUI by inheriting from `GUI`.
```py
from consolegui import GUI


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()
```

### Keyboard Interactions

Receive keyboard events with the `KeyboardInteraction` decorator.
```py
from consolegui import GUI, KeyboardInteraction, Events, KeyboardEvent


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()

    @KeyboardInteraction(Events.SPACE.value)
        def clicked_space(self, event: KeyboardEvent) -> None:
            ...
```
The `clicked_space` method runs when space is pressed. Reference the API for other keyboard events you can receive.

### Mouse Interactions

Mouse events can be dealt with similarly, with the `MouseInteraction` decorator.
```py
from consolegui import GUI, MouseInteraction, Events, MouseEvent, Region, Coordinate


INTERACTION_REGION = Region(Coordinate(0, 0), Coordinate(20, 0), Coordinate(20, 10), Coordinate(0, 10))


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()

    @MouseInteraction(Events.LEFT_MOUSE_DOWN.value, INTERACTION_REGION)  # Runs when left mouse button is pressed within the specified region
    def left_mouse_down(self, event: MouseEvent) -> None:
        ...
```
Mouse interactions require both an `Event` and `Region`, allowing for maximum customization.  

Note that both keyboard and mouse interaction methods make use of threading, and are called in a separate thread.

### GUI I/O Operations

The `GUI` class provides three key I/O methods - `print`, `erase`, and `clear` - each of which are show below.
```py
from consolegui import GUI, Coordinate


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()


def main() -> None:
    gui = MyGUI()
    text = "This text will be printed in the console."
    coordinates = Coordinate(10, 5)

    gui.print(text, at=coordinates)  # Print provides all of the same functionality as the built in print function
    gui.erase(at=coordinates)
    gui.clear()


if __name__ == "__main__":
    main()
```

### Managing Layers

To manage GUI layers in your application, use the `LayeredGUI` class. This will provide all of the same I/O methods as the simple `GUI` class, but manages layers automatically.
```py
from consolegui import LayeredGUI


class MyGUI(LayeredGUI):
    def __init__(self) -> None:
        super().__init__()  # self.base_layer is created automatically
        second_layer = self.add_layer("Layer Name", z=1)  # z-index is the same as that of the existing layer with the greatest z-index by default


def main() -> None:
    gui = MyGUI()
    text_base_layer = "This text will be printed in the console, on the base layer."
    text_1_second_layer = "This text will be printed in the console, on the second layer."
    text_2_second_layer = "This text will also be printed in the console, on the second layer."
    coordinates = Coordinate(10, 5)

    gui.print(text, at=coordinates)  # Prints on the active layer by default - this is initially the base layer
    gui.print(text_1_second_layer, at=coordinates, layer=gui.second_layer)  # Prints over the text on the base layer
    with gui.as_active(gui.second_layer):  # Second layer is set as active within this scope only
        gui.print(text_2_second_layer, at=coordinates)  # Overwrites the existing text
    gui.clear(layer=gui.second_layer)  # Only the content printed to the base layer now shows


if __name__ == "__main__":
    main()
```
Methods on the `Layer` class should not be used directly - only interact with layered GUIs via the `LayeredGUI` class methods.

_For more examples, functionality, and detail, please refer to the [Documentation](https://github.com/Kieran-Lock/ConsoleGUI/blob/main/DOCUMENTATION.md)_



## API Summary

Details of the ConsoleGUI API are listed below for quick reference.

### Input Events

```py

```
Events that do not appear on this list are likely to be under the alias of the key pressed, as a string: e.g. `"a", "A", "1", " ", "~"`



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See [LICENSE](https://github.com/Kieran-Lock/ConsoleGUI/blob/main/LICENSE) for further details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
