#!/usr/bin/env python

# tt-runner.py <file>
#
# Run a typetastic command file.

import argparse
import typetastic


def main():
    """Run a typetastic file."""

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("inputfile")
    args = arg_parser.parse_args()

    robot = typetastic.Robot()
    result = robot.load_file(args.inputfile)
    if not result:
        print("Failed to load yaml file: {0}".format(args.inputfile))
        exit(1)

    if "commands" in result:
        for command in result["commands"]:
            robot.run_command(command)


if __name__ == "__main__":
    main()
