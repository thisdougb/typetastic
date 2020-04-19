"""Handlers for commands."""

import getch
import pexpect


def bot_handler_pause():
    """Handler for ls."""
    _pause_flow()
    return True


def bot_handler_ls(command):
    """Handler for ls."""
    _run_command(command)
    return True


def _pause_flow():
    print("pause flow 2")


def _run_command(command):
    """Run local command."""

    spawn_cmd = "/bin/bash -c '{0}'".format(command)
    child = pexpect.spawn(spawn_cmd, timeout=None, encoding='utf-8')

    for line in child:
        print(line, end="")
    child.close()

    # 0 = success, 1 = failure in Unix, so invert result
    return not bool(child.exitstatus)
