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
import logging
import os
import signal
import sys
import time


__author__ = "Jacob Walker"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s -'
                              ' %(levelname)s - %(message)s')
log_stream = logging.StreamHandler(sys.stdout)
log_stream.setLevel(logging.INFO)
log_stream.setFormatter(formatter)
logger.addHandler(log_stream)

# declare a few constants
checked_files = {}


def magic_word_finder(directory, magic_word):
    d = os.path.abspath(directory)
    text_files = [f for f in os.listdir(d) if ".txt" in f]
    text_files = [f for f in os.listdir(d) if extension in f]
    for f in text_files:
        line_count = len(open(f).readlines())
        if f not in checked_files:
            checked_files[f] = 0
            logger.info("checking... " + f)
            search_file(f, magic_word)
        else:
            if checked_files[f] != 0 and line_count != checked_files[f]:
                logger.info(
                    "File {} changed, searching again".format(f))
                search_file(f, magic_word)


def search_file(f, magic_word):
    logging.info("searching {} for instances of {}".format(f, magic_word))
    logger.info("searching {} for instances of {}".format(f, magic_word))

    with open(f) as doc:
        content = doc.readlines()
        last_index = 0
        for i, line in enumerate(content):
            last_index += 1
            if magic_word in line:
                logger.info("Match found for {} found on line {} in {}"
                            .format(magic_word, i + 1, f))
        checked_files[f] = i + 1


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
    parser.add_argument('-x', '--extension', help='Sets the type of file to watch for', default='.txt')
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
            magic_word_finder(os.path.join(os.getcwd(), parsed_args.directory), parsed_args.magic_word)
        except Exception as e:
            logging.exception(e)
        time.sleep(parsed_args.interval)


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
