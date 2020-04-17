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
    robot.load(args.inputfile)
    robot.run()


if __name__ == "__main__":
    main()
