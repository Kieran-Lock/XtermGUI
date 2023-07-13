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

Input events can be received via the `GUI` API.
```py
class Events(Enum):
    SHIFT_BACKSPACE: Event = Event("SHIFT_BACKSPACE")
    TAB: Event = Event("TAB")
    ENTER: Event = Event("ENTER")
    BACKSPACE: Event = Event("BACKSPACE")
    POUND: Event = Event("POUND")

    UP_ARROW: Event = Event("UP_ARROW")
    DOWN_ARROW: Event = Event("DOWN_ARROW")
    RIGHT_ARROW: Event = Event("RIGHT_ARROW")
    LEFT_ARROW: Event = Event("LEFT_ARROW")
    END: Event = Event("END")
    HOME: Event = Event("HOME")
    SHIFT_TAB: Event = Event("SHIFT_TAB")

    LEFT_MOUSE_UP: Event = Event("LEFT_MOUSE_UP")
    LEFT_MOUSE_DOWN: Event = Event("LEFT_MOUSE_DOWN")
    MIDDLE_MOUSE_UP: Event = Event("MIDDLE_MOUSE_UP")
    MIDDLE_MOUSE_DOWN: Event = Event("MIDDLE_MOUSE_DOWN")
    RIGHT_MOUSE_UP: Event = Event("RIGHT_MOUSE_UP")
    RIGHT_MOUSE_DOWN: Event = Event("RIGHT_MOUSE_DOWN")
    LEFT_MOUSE_DRAG: Event = Event("LEFT_MOUSE_DRAG")
    MIDDLE_MOUSE_DRAG: Event = Event("MIDDLE_MOUSE_DRAG")
    RIGHT_MOUSE_DRAG: Event = Event("RIGHT_MOUSE_DRAG")
    MOVE: Event = Event("MOVE")
    SCROLL_UP: Event = Event("SCROLL_UP")
    SCROLL_DOWN: Event = Event("SCROLL_DOWN")

    INSERT: Event = Event("INSERT")
    DELETE: Event = Event("DELETE")
    PAGE_UP: Event = Event("PAGE_UP")
    PAGE_DOWN: Event = Event("PAGE_DOWN")
    F5: Event = Event("F5")
    F6: Event = Event("F6")
    F7: Event = Event("F7")
    F8: Event = Event("F8")
    F9: Event = Event("F9")
    F10: Event = Event("F10")
    F11: Event = Event("F11")
    F12: Event = Event("F12")

    F1: Event = Event("F1")
    F2: Event = Event("F2")
    F3: Event = Event("F3")
    F4: Event = Event("F4")
    SPACE: Event = Event(" ")
    FORWARD_SLASH: Event = Event("/")
    BACKSLASH: Event = Event("\\")
    VERTICAL_BAR: Event = Event("|")
    PIPE: Event = Event("|")
    EXCLAMATION_MARK: Event = Event("!")
    QUESTION_MARK: Event = Event("?")
    COMMA: Event = Event(",")
    FULL_STOP: Event = Event(".")
    LESS_THAN: Event = Event("<")
    LEFT_ANGLE_BRACKET: Event = Event("<")
    LEFT_CHEVRON: Event = Event("<")
    GREATER_THAN: Event = Event(">")
    RIGHT_ANGLE_BRACKET: Event = Event(">")
    RIGHT_CHEVRON: Event = Event(">")
    SEMI_COLON: Event = Event(";")
    COLON: Event = Event(":")
    APOSTROPHE: Event = Event("'")
    AT: Event = Event("@")
    HASHTAG: Event = Event("#")
    OCTOTHORPE: Event = Event("#")
    TILDE: Event = Event("~")
    LEFT_SQUARE_BRACKET: Event = Event("[")
    RIGHT_SQUARE_BRACKET: Event = Event("]")
    LEFT_CURLY_BRACKET: Event = Event("{")
    LEFT_BRACE: Event = Event("{")
    RIGHT_CURLY_BRACKET: Event = Event("}")
    RIGHT_BRACE: Event = Event("}")
    HYPHEN: Event = Event("-")
    MINUS: Event = Event("-")
    UNDERSCORE: Event = Event("_")
    EQUALS: Event = Event("=")
    PLUS: Event = Event("+")
    BACKTICK: Event = Event("`")
    LOGICAL_NEGATION: Event = Event("¬")
    BROKEN_BAR: Event = Event("¦")
    SPEECH_MARK: Event = Event("\")")
    QUOTATION_MARK: Event = Event("\")")
    DOLLAR: Event = Event("$")
    PERCENT: Event = Event("%")
    CARET: Event = Event("^")
    AMPERSAND: Event = Event("&")
    ASTERISK: Event = Event("*")
    LEFT_BRACKET: Event = Event("(")
    LEFT_PARENTHESIS: Event = Event("(")
    RIGHT_BRACKET: Event = Event(")")
    RIGHT_PARENTHESIS: Event = Event(")")

    ANY_KEYBOARD: Event = Event(KeyboardEvent.ANY, lambda _: True)
    ANY_MOUSE: Event = Event(MouseEvent.ANY, lambda _: True)
    UNRECOGNIZED_KEYBOARD: Event = Event(KeyboardEvent.UNRECOGNIZED)
    UNRECOGNIZED_MOUSE: Event = Event(MouseEvent.UNRECOGNIZED)
```
Events that do not appear in this enum (such as the letters of the alphabet) can be created with `Event("<LETTER>")`. For example, `Event("A")`.

### RGB Colours

RGB colours represent only information about a specific colour.
```py
class RGBs(Enum):
    DEFAULT_FOREGROUND = RGB(192, 192, 192)
    DEFAULT_BACKGROUND_PYCHARM = RGB(43, 43, 43)
    DEFAULT_BACKGROUND_REPLIT = RGB(28, 35, 51)
    DEFAULT_BACKGROUND_WSL = RGB(12, 12, 12)
    BLACK = RGB(0, 0, 0)
    WHITE = RGB(255, 255, 255)
    RED = RGB(255, 0, 0)
    GREEN = RGB(0, 255, 0)
    BLUE = RGB(0, 0, 255)
    YELLOW = RGB(255, 255, 0)
    CYAN = RGB(0, 255, 255)
    MAGENTA = RGB(255, 0, 255)
    ORANGE = RGB(255, 165, 0)
    PURPLE = RGB(230, 230, 250)
    GREY = RGB(142, 142, 142)
    BROWN = RGB(162, 162, 42)
```

### Text Colours

Text colours represent the colour of text printed to the console.
```py
class Colours(Enum):
    F_BLACK: Colour = Colour(foreground=RGBs.BLACK.value)
    F_WHITE: Colour = Colour(foreground=RGBs.WHITE.value)
    F_RED: Colour = Colour(foreground=RGBs.RED.value)
    F_GREEN: Colour = Colour(foreground=RGBs.GREEN.value)
    F_BLUE: Colour = Colour(foreground=RGBs.BLUE.value)
    F_YELLOW: Colour = Colour(foreground=RGBs.YELLOW.value)
    F_CYAN: Colour = Colour(foreground=RGBs.CYAN.value)
    F_MAGENTA: Colour = Colour(foreground=RGBs.MAGENTA.value)
    F_ORANGE: Colour = Colour(foreground=RGBs.ORANGE.value)
    F_PURPLE: Colour = Colour(foreground=RGBs.PURPLE.value)
    F_GREY: Colour = Colour(foreground=RGBs.GREY.value)
    F_BROWN: Colour = Colour(foreground=RGBs.BROWN.value)
    F_DEFAULT: Colour = Colour(foreground=RGBs.DEFAULT_FOREGROUND.value)

    B_BLACK: Colour = Colour(background=RGBs.BLACK.value)
    B_WHITE: Colour = Colour(background=RGBs.WHITE.value)
    B_RED: Colour = Colour(background=RGBs.RED.value)
    B_GREEN: Colour = Colour(background=RGBs.GREEN.value)
    B_BLUE: Colour = Colour(background=RGBs.BLUE.value)
    B_YELLOW: Colour = Colour(background=RGBs.YELLOW.value)
    B_CYAN: Colour = Colour(background=RGBs.CYAN.value)
    B_MAGENTA: Colour = Colour(background=RGBs.MAGENTA.value)
    B_ORANGE: Colour = Colour(background=RGBs.ORANGE.value)
    B_PURPLE: Colour = Colour(background=RGBs.PURPLE.value)
    B_GREY: Colour = Colour(background=RGBs.GREY.value)
    B_BROWN: Colour = Colour(background=RGBs.BROWN.value)
    B_DEFAULT_PYCHARM: Colour = Colour(background=RGBs.DEFAULT_BACKGROUND_PYCHARM.value)
    B_DEFAULT_REPLIT: Colour = Colour(background=RGBs.DEFAULT_BACKGROUND_REPLIT.value)
    B_DEFAULT_BACKGROUND_WSL = Colour(background=RGBs.DEFAULT_BACKGROUND_WSL.value)
```

### Text Styles

Text styles represent the style of text printed to the console.
```py
class Styles(Enum):
    NOT_STYLED: Style = Style()
    BOLD: Style = Style(bold=True)
    DIMMED: Style = Style(dimmed=True)
    ITALIC: Style = Style(italic=True)
    UNDERLINED: Style = Style(underlined=True)
    HIDDEN: Style = Style(hidden=True)
    CROSSED_OUT: Style = Style(crossed_out=True)
```



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See [LICENSE](https://github.com/Kieran-Lock/ConsoleGUI/blob/main/LICENSE) for further details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
