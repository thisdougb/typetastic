"""Handlers for commands."""

import getch
import pexpect
import random
import sys
import time


def bot_handler_default(handler_data):
    """Handler for ls."""

    command = handler_data["command"]
    current_directory = handler_data["current_directory"]

    (speed_min, speed_max, return_key_delay) = handler_data["typing_speed"]
    simulate_typing(command, speed_min, speed_max, return_key_delay)

    return run_command(command, current_directory)


def bot_handler_newline(handler_data):
    # pylint: disable=unused-argument
    """Handler for newline."""
    simulate_typing("", 0, 0, 0)
    return True


def bot_handler_pause(handler_data):
    # pylint: disable=unused-argument
    """Handler for pause."""
    pause_flow()
    return True


def bot_handler_editor(handler_data):
    # pylint: disable=unused-argument
    """Handler for vi."""
    pause_flow()
    return True


def bot_handler_emacs(handler_data):
    """Handler for emacs."""
    return bot_handler_editor(handler_data)


def bot_handler_vi(handler_data):
    """Handler for vi."""
    return bot_handler_editor(handler_data)


def emit_prompt(prompt):
    """Emit a prompt."""
    print(prompt, end="")
    sys.stdout.flush()


def pause_flow():
    """Creates a pause by waiting for a keypress."""
    getch.getch()


def run_command(command, current_dir):
    """Run local command."""

    spawn_cmd = "/bin/bash -c '{0}'".format(command)
    child = pexpect.spawn(spawn_cmd, cwd=current_dir, timeout=None, encoding='utf-8')

    for line in child:
        print(line, end="")
    child.close()

    # 0 = success, 1 = failure in Unix, so invert result
    return not bool(child.exitstatus)


def simulate_typing(command, speed_min, speed_max, return_key_delay):
    """Simulates typing to stdout."""

    for char in command:
        print(char, end="")
        sys.stdout.flush()
        char_delay = random.uniform(speed_min, speed_max)
        time.sleep(char_delay)

    time.sleep(return_key_delay)
    print()  # newline required after typing command
