from contextlib import contextmanager
from sys import stdout, stdin  # , executable
from termios import tcgetattr, tcsetattr, ECHO, ICANON, TCSADRAIN
from typing import Iterator


# from subprocess import run, PIPE


class State:
    IS_SETUP: bool = False


@contextmanager
def console_inputs() -> Iterator[None]:
    if State.IS_SETUP:
        yield
        return

    setup_commands = (
        "\033[?7l",  # TODO: Cleanup with escape code class
        "\033[?25l",  # TODO: Might require file structure refactor?
        "\033[?1006h"
    )  # Disable Line Wrapping, Hide Cursor, Enable Mouse Reporting (SGR)
    cleanup_commands = (
        "\033[?1006l",
        "\033[?25h",
        "\033[?7h"
    )  # Disable Mouse Reporting (SGR), Show Cursor, Enable Line Wrapping
    original_state = tcgetattr(stdin)
    new_state = original_state[:]

    for escape_code in setup_commands:
        stdout.write(escape_code)

    new_state[3] -= (ECHO + ICANON)
    # new_state[3] -= ICANON
    tcsetattr(stdin, TCSADRAIN, new_state)  # Disable ECHO and ICANON

    State.IS_SETUP = True

    try:
        yield

    finally:
        State.IS_SETUP = False

        tcsetattr(stdin, TCSADRAIN, original_state)  # Enable ECHO and ICANON

        # run((executable, "-c", "input()"), input="", stderr=PIPE, encoding="utf-8")  # Runs input() in a subprocess

        for escape_code in cleanup_commands:
            stdout.write(escape_code)
