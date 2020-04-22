"""Handlers for commands."""

import re
import getch
import pexpect
import random
import sys
import time


def bot_handler_default(handler_data):
    """Handler for ls."""

    (speed_min, speed_max, return_key_delay) = handler_data["typing_speed"]
    simulated_typing = handler_data["simulated_typing"]
    simulate_typing(simulated_typing, speed_min, speed_max, return_key_delay)

    if handler_data["remote"]:
        return run_ssh_command(handler_data)

    return run_command(handler_data)


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


# SSH
def bot_handler_ssh(handler_data):
    """SSH login."""
    if "command" in handler_data:

        (speed_min, speed_max, return_key_delay) = handler_data["typing_speed"]
        simulated_typing = handler_data["simulated_typing"]
        simulate_typing(simulated_typing, speed_min, speed_max, return_key_delay)

        command = handler_data["command"]
        ssh_conn = handler_data["remote"]

        (user, host) = parse_ssh_user_host(command)

        try:
            ssh_conn.login(host, user)
            return not ssh_conn.closed

        except pexpect.pxssh.ExceptionPxssh as error:
            print("ssh login failed: {0}".format(error))

    return False


def bot_handler_exit(handler_data):
    """SSH exit."""
    if "remote" in handler_data and handler_data["remote"]:

        (speed_min, speed_max, return_key_delay) = handler_data["typing_speed"]
        simulated_typing = handler_data["simulated_typing"]
        simulate_typing(simulated_typing, speed_min, speed_max, return_key_delay)

        ssh_conn = handler_data["remote"]
        ssh_conn.logout()
        return ssh_conn.closed

    return False


def parse_ssh_user_host(command):
    """Find user and host."""

    user_patterns = [
        r" ([a-z0-9\.]+)@",
        r"-l ([a-z0-9\.]+) "
    ]

    user = None
    for pattern in user_patterns:
        comp_pattern = re.compile(pattern)
        result = comp_pattern.search(command)
        if result:
            user = result.group(1)

    host = None
    host_patterns = [
        r"@([a-z0-9\.]+)",
        r" ([a-z0-9\.]+)$"
    ]

    for pattern in host_patterns:
        comp_pattern = re.compile(pattern)
        result = comp_pattern.search(command)
        if result:
            host = result.group(1)

    return (user, host)


# EDITORS
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


def run_command(handler_data):
    """Run local command.
    """

    delay = 0.2
    command = handler_data["command"]
    session = handler_data["local"]
    prompt = handler_data["config"]["prompt-string"]

    session.sendline(command)
    time.sleep(delay)
    while True:
        session.expect_exact([prompt, '\r\n', pexpect.EOF, pexpect.TIMEOUT])
        if session.before.rstrip():
            print(session.before.rstrip())
        if not session.buffer:
            break

    # this is how we get the exit status of the command
    session.sendline("echo $?")
    time.sleep(delay)  # at least 0.2 seems to work, otherwise expect buffer is empty
    retval = False
    while True:
        # session.expect_exact(['\r\n', pexpect.EOF, pexpect.TIMEOUT])
        session.expect_exact(["\r\n", prompt, pexpect.EOF, pexpect.TIMEOUT])
        if session.before.isdigit():
            retval = not bool(int(session.before))
        if not session.buffer:
            break

    return retval


def run_ssh_command(handler_data):
    """Run local command."""

    command = handler_data["command"]
    ssh_conn = handler_data["remote"]

    if ssh_conn:
        ssh_conn.sendline(command)
        ssh_conn.prompt()
        print(ssh_conn.before[len(command)+2:].decode("utf-8"), end="")

        ssh_conn.sendline("echo $?")
        ssh_conn.prompt()
        retval = ssh_conn.before[-3:-2].decode("utf-8")
        if retval == "0":
            return True

    # 0 = success, 1 = failure in Unix, so invert result
    return False


def simulate_typing(command, speed_min, speed_max, return_key_delay):
    """Simulates typing to stdout."""

    for char in command:
        print(char, end="")
        sys.stdout.flush()
        char_delay = random.uniform(speed_min, speed_max)
        time.sleep(char_delay)

    time.sleep(return_key_delay)
    print()  # newline required after typing command
