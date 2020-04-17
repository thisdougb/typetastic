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

    tastic_bot = typetastic.Robot
    tastic_bot.hello()

if __name__ == "__main__":
    main()
