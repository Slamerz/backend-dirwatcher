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
import sys
import signal
import logging
import time
import os


__author__ = "Jacob Walker"

logging.basicConfig(filename='test.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')

# declare a few constants

def first_helper_func(x):
    """docstring as first line"""
    print("inside first_helper() with x={}".format(x))


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here
    as well (SIGHUP?) Basically it just sets a global flag, and main() will
    exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    signame = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                   if v.startswith('SIG') and not v.startswith('SIG_'))
    logging.warning('Received {}'.format(signame[sig_num]))
    raise KeyboardInterrupt


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='directory to monitor')
    parser.add_argument('magic_word', help='The magic word/words to watch for')
    parser.add_argument('-i',
                        '--interval',
                        help='Sets the interval in seconds to check the directory for magic words',
                        default=1)
    parser.add_argument('-x', '--extension', help='Sets teh type of file to watch for', default='.txt')
    return parser


def main(args):
    """Main function is declared as standalone, for testability"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    print(parsed_args)
    print("Starting App")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while 1:
        try:
            print("main args: {}".format(args))
        except Exception as e:
            logging.exception(e)
        time.sleep(10)


if __name__ == '__main__':
    """Runs the main loop until an interrupt like control+c are input."""
    print("My Pid is {}".format(os.getpid()))
    print("Command line arguments: {}".format(sys.argv))
    start_time = time.time()
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nExiting by user request.\n"
              "Process ran for {} seconds".format(time.time() - start_time))
        sys.exit(0)
