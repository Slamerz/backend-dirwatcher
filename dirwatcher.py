#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module docstring: One line description of what your program does.

There should be a blank line in between description above, and this
more detailed description. In this section you should put any caveats, 
environment variable expectations, gotchas, and other notes about running
the program.  Author tag (below) helps instructors keep track of who 
wrote what, when grading.
"""
import argparse

__author__ = "Jacob Walker"

# Imports go at the top of your file, after the module docstring.
# One module per import line. These are for example only.
import sys
from math import pi

# This statement will run once at module import.
print("Executing module import, name is {}".format(__name__))

# declare a few constants
MY_MODULE_PI = pi


def second_helper_func(y):
    """docstring as first line"""
    print("inside second_helper() with y={}".format(y))
    return MY_MODULE_PI


def first_helper_func(x):
    """docstring as first line"""
    print("inside first_helper() with x={}".format(x))
    return second_helper_func(x)


def function_to_be_implemented():
    """You can raise your own exceptions"""
    raise NotImplementedError("TODO Get to work and write this!")


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir', help='destination directory for something')
    return parser


def main(args):
    """Main function is declared as standalone, for testability"""
    # You can call this main() function even if it is imported by
    # another program.
    print("main args: {}".format(args))
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    parsed_args = parser.parse_args(args)
    # get the first argument, do something cool
    result = first_helper_func(parsed_args.todir)
    # return 0 if everything is awesome, nonzero otherwise ...
    print('result is {}'.format(result))
    return 0


if __name__ == '__main__':
    """Docstring goes here"""
    print("Command line arguments: {}".format(sys.argv))
    # Invoke standalone main() with cmdline argument list.
    # Program should return status==0 if no errors.
    status = main(sys.argv[1:])
    # return status code to OS.
    sys.exit(status)
