from sys import stdout, stdin  # , executable
from contextlib import contextmanager
from termios import tcgetattr, tcsetattr, ECHO, ICANON, TCSADRAIN
from typing import Iterator
# from subprocess import run, PIPE

from ..control import Cursor


IS_SETUP = False


@contextmanager
def console_inputs() -> Iterator[None]:
    global IS_SETUP

    if IS_SETUP:
        yield
        return

    setup_commands = (
        "\033[?7l", "\033[?1003h", "\033[?1006h"
    )  # Disable Line Wrapping, Enable Mouse Reporting (Full, SGR)
    cleanup_commands = (
        "\033[?1006l", "\033[?1003l", "\033[?7h"
    )  # Disable Mouse Reporting (SGR, Full), Enable Line Wrapping
    original_state = tcgetattr(stdin)
    new_state = original_state[:]

    Cursor.hide()
    for escape_code in setup_commands:
        stdout.write(escape_code)

    # new_state[3] -= (ECHO + ICANON)
    new_state[3] -= ICANON
    tcsetattr(stdin, TCSADRAIN, new_state)  # Disable ECHO and ICANON

    IS_SETUP = True

    try:
        yield
    finally:
        IS_SETUP = False
        tcsetattr(stdin, TCSADRAIN, original_state)  # Enable ECHO and ICANON
        # run((executable, "-c", "input()"), input="", stderr=PIPE, encoding="utf-8")  # Runs input() in a subprocess
        for escape_code in cleanup_commands:
            stdout.write(escape_code)
        Cursor.show()
