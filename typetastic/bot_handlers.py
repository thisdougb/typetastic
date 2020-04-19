"""Handlers for commands."""

import getch
import pexpect


def bot_handler_newline(command):
    # pylint: disable=unused-argument
    """Handler for newline."""
    print()
    return True


def bot_handler_pause(command):
    # pylint: disable=unused-argument
    """Handler for pause."""
    pause_flow()
    return True


def bot_handler_editor(command):
    # pylint: disable=unused-argument
    """Handler for vi."""
    pause_flow()
    return True


def bot_handler_vi(command):
    """Handler for vi."""
    return bot_handler_editor(command)


def bot_handler_default(command):
    """Handler for ls."""
    return False


def pause_flow():
    getch.getch()


def run_command(command):
    """Run local command."""

    spawn_cmd = "/bin/bash -c '{0}'".format(command)
    child = pexpect.spawn(spawn_cmd, timeout=None, encoding='utf-8')

    for line in child:
        print(line, end="")
    child.close()

    # 0 = success, 1 = failure in Unix, so invert result
    return not bool(child.exitstatus)
