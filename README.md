<a id="readme-top"></a>



<!-- PROJECT SUMMARY -->
<br />
<div align="center">
  <img src="https://i.imgur.com/8nvN82u.png" alt="Logo">
  <br />
  <p align="center">
    An expressive GUI framework for compatible terminals
    <br />
    <a href="https://github.com/Kieran-Lock/XtermGUI/blob/main/DOCUMENTATION.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#getting-started">Getting Started</a>
    ·
    <a href="#basic-usage">Usage</a>
    ·
    <a href="https://github.com/Kieran-Lock/XtermGUI/blob/main/DOCUMENTATION.md">Documentation</a>
    ·
    <a href="#api-summary">API</a>
    ·
    <a href="https://github.com/Kieran-Lock/XtermGUI/blob/main/LICENSE">License</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->

## About the Project

XtermGUI is a lightweight GUI framework for compatible xterm terminals, allowing you to write complex terminal
applications, with expressive, concise, and readable code.

With zero external dependencies, and features including keyboard and mouse input, customizable event listeners, and
multiple layer management, you can create and manage complex terminal GUIs with minimal overhead, all in Python.



<!-- GETTING STARTED -->

## Getting Started

XtermGUI is available on [PyPI](https://pypi.org/project/XtermGUI/). To use it in your project, run:

```
pip install XtermGUI
```

To install specific previous versions, take a look at the version history, locate the version tag (vX.Y.Z), and run:

```
pip install Xterm==X.Y.Z
```

<!-- TROUBLE SHOOTING -->

## Trouble Shooting

XtermGUI uses xterm-specific control sequences. If XtermGUI is running incorrectly once installed, ensure that the
terminal you are using has sufficient mouse-reporting and xterm support support.

This framework has been tested using the default setup for [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/) on
Windows 10, which uses an `xterm-256color` terminal by default.

[Here](https://gist.github.com/justinmk/a5102f9a0c1810437885a04a07ef0a91) is a useful resource for xterm control
sequences reference.



<!-- BASIC USAGE EXAMPLES -->

## Basic Usage

### Setting up the terminal

Use the `console_inputs` context manager to prepare the terminal for use with XtermGUI. This will handle the cleanup
automatically.

```py
from xtermgui import terminal_inputs

with terminal_inputs():
    ...
```

_Please note that there may sometimes be control sequence leakage when exiting your application. This is unavoidable (I
am yet to find a solution), but will only happen once the application is exited, and for only very short periods of
time._

### Reading console input

Use the `read_console` function to read both keyboard and mouse input from the console. View
the [API summary](#api-summary) or [documentation](https://github.com/Kieran-Lock/XtermGUI/blob/main/DOCUMENTATION.md)
for the possible events you can receieve from this function.

```py
from xtermgui import terminal_inputs, read_event

with terminal_inputs():
    read_key = read_event()
    ...
```

Read repeated console input by placing this function in a loop. This can be useful for reading a stream of user inputs.

```py
from xtermgui import terminal_inputs, read_event

with terminal_inputs():
    while True:  # Or some other loop
        read_key = read_event()
        ...
```

### Text Formatting

The `Text` class can be used to represent formatted text, which can be printed to the console. It provides all the same
functionality as the built-in `str` string type, but can be used in conjunction with the `Style` and `Colour` classes to
represent coloured and styled text.

```py
from xtermgui import TextColours, Styles, Text, TextColour, Colours

TextColour.configure_default_background(
    Colours.DEFAULT_BACKGROUND_WSL.value)  # Test written in WSL, so the background is configured like so

text = "This is styled text."
text_colour = TextColours.F_BLUE.value.blend(TextColours.F_GREY.value, foreground_bias=0.5,
                                             foreground_gamma=2.2)  # This blending just uses the default blending parameters
text_background_colour = TextColours.B_BLACK.value
text_style = Styles.BOLD.value + Styles.UNDERLINED.value

text = Text(text, colour=text_colour, style=text_style)
text.add_colour(text_background_colour)

print(text)  # Prints the text string, with a silver-blue foreground, black background, underlined and in bold
```

<!-- COMPLEX USAGE EXAMPLES -->

## Complex Usage

For more complex use cases, it is best to organise your application using the `GUI` or `LayeredGUI` classes. Some of the
benefits of this approach are:

* Easier & Customizable Event Listeners
* Layer Management
* Simplified GUI Manipulation

### Creating and configuring a GUI

You can create a simple GUI by inheriting from `GUI`.

```py
from xtermgui import GUI


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()
```

You can use this GUI by using the `start` method as a context manager.

```py
from xtermgui import GUI


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()


def main() -> None:
    gui = MyGUI()

    with gui.start():
        ...


if __name__ == "__main__":
    main()
```

### Interactions

Receiving input events, via interactions, is an opt-in behaviour in XtermGUI. When enabled, it handles the input thread
automatically, such that all events you receive will be called in a separate thread.

To use a `GUI` with this capability, pass `inputs=True` to the `start` method.

```py
from xtermgui import GUI


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()


def main() -> None:
    gui = MyGUI()

    with gui.start(inputs=True):
        ...


if __name__ == "__main__":
    main()
```

#### Keyboard Interactions

Receive keyboard events with the `KeyboardInteraction` decorator.

```py
from xtermgui import GUI, KeyboardInteraction, Events, KeyboardEvent


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()

    @KeyboardInteraction(Events.SPACE.value)
    def clicked_space(self, event: KeyboardEvent) -> None:
        ...
```

The `clicked_space` method runs when space is pressed. Reference the API for other keyboard events you can receive.

#### Mouse Interactions

Mouse events can be dealt with similarly, with the `MouseInteraction` decorator.

```py
from xtermgui import GUI, MouseInteraction, Events, MouseEvent, Region, Coordinate

INTERACTION_REGION = Region(Coordinate(0, 0), Coordinate(20, 0), Coordinate(20, 10), Coordinate(0,
                                                                                                10))  # An example region - a 20x10 rectangle, which forms a square in the terminal


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()

    @MouseInteraction(Events.LEFT_MOUSE_DOWN.value,
                      region=INTERACTION_REGION)  # Runs when left mouse button is pressed within the specified region
    def left_mouse_down(self, event: MouseEvent) -> None:
        ...
```

Mouse interactions require an `Event`, and take a `Region` as an optional argument. If `region` is omitted, the event
will fire at any position.

### GUI I/O Operations

The `GUI` class provides three key I/O methods - `print`, `erase`, and `clear` - each of which are show below.

```py
from xtermgui import GUI, Coordinate


class MyGUI(GUI):
    def __init__(self) -> None:
        super().__init__()


def main() -> None:
    gui = MyGUI()
    text = "This text will be printed in the console."
    coordinates = Coordinate(10, 5)

    with gui.start():
        gui.print(text, at=coordinates)  # Print provides all the same functionality as the built-in print function
        gui.erase(at=coordinates)
        gui.clear()


if __name__ == "__main__":
    main()
```

### Managing Layers

To manage GUI layers in your application, use the `LayeredGUI` class. This will provide all of the same I/O methods as
the simple `GUI` class, but manages layers automatically.

```py
from xtermgui import TextColour, Colours, LayeredGUI, Coordinate

TextColour.configure_default_background(Colours.DEFAULT_BACKGROUND_WSL.value)


class MyGUI(LayeredGUI):
    def __init__(self) -> None:
        super().__init__()  # self.base_layer is created automatically
        self.second_layer = self.add_layer("Layer Name",
                                           z=1)  # z-index is the same as that of the existing layer with the greatest z-index by default


def main() -> None:
    gui = MyGUI()
    text_base_layer = "This text will be printed in the console, on the base layer."
    text_1_second_layer = "This text will be printed in the console, on the second layer."
    text_2_second_layer = "This text will also be printed in the console, on the second layer."
    coordinates = Coordinate(10, 5)

    with gui.start():
        gui.print(text_base_layer,
                  at=coordinates)  # Prints on the active layer by default - this is initially the base layer
        gui.print(text_1_second_layer, at=coordinates, layer=gui.second_layer)  # Prints over the text on the base layer
        with gui.second_layer.as_active():  # Second layer is set as active within this scope only
            gui.print(text_2_second_layer, at=coordinates)  # Overwrites the existing text
        gui.clear(layer=gui.second_layer)  # Only the content printed to the base layer now shows


if __name__ == "__main__":
    main()
```

Methods on the `Layer` class should not be used directly - only interact with layered GUIs via the `LayeredGUI` class
methods.

_For more examples, functionality, and detail, please refer to
the [Documentation](https://github.com/Kieran-Lock/XtermGUI/blob/main/DOCUMENTATION.md)_

## API Summary

Details of the XtermGUI API are listed below for quick reference.

### Input Events

Input events can be received via the `GUI` API.

```py
from enum import Enum
from xtermgui import Event, KeyboardEvent, MouseEvent


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

Events that do not appear in this enum (such as the letters of the alphabet) can be created with `Event("<LETTER>")`.
For example, `Event("A")`.

### RGB Colours

RGB colours represent only information about a specific colour.

```py
from enum import Enum
from xtermgui import Colour


class RGBs(Enum):
    DEFAULT_FOREGROUND = Colour(192, 192, 192)
    DEFAULT_BACKGROUND_PYCHARM = Colour(43, 43, 43)
    DEFAULT_BACKGROUND_REPLIT = Colour(28, 35, 51)
    DEFAULT_BACKGROUND_WSL = Colour(12, 12, 12)
    BLACK = Colour(0, 0, 0)
    WHITE = Colour(255, 255, 255)
    RED = Colour(255, 0, 0)
    GREEN = Colour(0, 255, 0)
    BLUE = Colour(0, 0, 255)
    YELLOW = Colour(255, 255, 0)
    CYAN = Colour(0, 255, 255)
    MAGENTA = Colour(255, 0, 255)
    ORANGE = Colour(255, 165, 0)
    PURPLE = Colour(230, 230, 250)
    GREY = Colour(142, 142, 142)
    BROWN = Colour(162, 162, 42)
```

### Text Colours

Text colours represent the colour of text printed to the console.

```py
from enum import Enum
from xtermgui import TextColour, Colours


class Colours(Enum):
    F_BLACK: TextColour = TextColour(foreground=Colours.BLACK.value)
    F_WHITE: TextColour = TextColour(foreground=Colours.WHITE.value)
    F_RED: TextColour = TextColour(foreground=Colours.RED.value)
    F_GREEN: TextColour = TextColour(foreground=Colours.GREEN.value)
    F_BLUE: TextColour = TextColour(foreground=Colours.BLUE.value)
    F_YELLOW: TextColour = TextColour(foreground=Colours.YELLOW.value)
    F_CYAN: TextColour = TextColour(foreground=Colours.CYAN.value)
    F_MAGENTA: TextColour = TextColour(foreground=Colours.MAGENTA.value)
    F_ORANGE: TextColour = TextColour(foreground=Colours.ORANGE.value)
    F_PURPLE: TextColour = TextColour(foreground=Colours.PURPLE.value)
    F_GREY: TextColour = TextColour(foreground=Colours.GREY.value)
    F_BROWN: TextColour = TextColour(foreground=Colours.BROWN.value)
    F_DEFAULT: TextColour = TextColour(foreground=Colours.DEFAULT_FOREGROUND.value)

    B_BLACK: TextColour = TextColour(background=Colours.BLACK.value)
    B_WHITE: TextColour = TextColour(background=Colours.WHITE.value)
    B_RED: TextColour = TextColour(background=Colours.RED.value)
    B_GREEN: TextColour = TextColour(background=Colours.GREEN.value)
    B_BLUE: TextColour = TextColour(background=Colours.BLUE.value)
    B_YELLOW: TextColour = TextColour(background=Colours.YELLOW.value)
    B_CYAN: TextColour = TextColour(background=Colours.CYAN.value)
    B_MAGENTA: TextColour = TextColour(background=Colours.MAGENTA.value)
    B_ORANGE: TextColour = TextColour(background=Colours.ORANGE.value)
    B_PURPLE: TextColour = TextColour(background=Colours.PURPLE.value)
    B_GREY: TextColour = TextColour(background=Colours.GREY.value)
    B_BROWN: TextColour = TextColour(background=Colours.BROWN.value)
    B_DEFAULT_PYCHARM: TextColour = TextColour(background=Colours.DEFAULT_BACKGROUND_PYCHARM.value)
    B_DEFAULT_REPLIT: TextColour = TextColour(background=Colours.DEFAULT_BACKGROUND_REPLIT.value)
    B_DEFAULT_BACKGROUND_WSL = TextColour(background=Colours.DEFAULT_BACKGROUND_WSL.value)
```

### Text Styles

Text styles represent the style of text printed to the console.

```py
from enum import Enum
from xtermgui import Style


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

Distributed under the GNU General Public License v3.0.
See [LICENSE](https://github.com/Kieran-Lock/XtermGUI/blob/main/LICENSE) for further details.

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>
