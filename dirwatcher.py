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
exit_flag = False


def magic_word_finder(directory, magic_word, extension):
    """Goes through each file of a given type in the given directory
    and searches for given text."""
    d = os.path.abspath(directory)

    text_files = [f for f in os.listdir(d) if f.endswith(extension)]
    for f in text_files:
        full_path = os.path.join(d, f)
        fd = open(full_path)
        line_count = len(fd.readlines())
        fd.close()

        f = full_path
        if f not in checked_files:
            checked_files[f] = 0
            logger.info("checking... " + f)
            search_file(f, magic_word)
        else:
            if line_count != checked_files[f] and line_count != 0:
                logger.info(
                    "File {} changed, searching again".format(f))
                search_file(f, magic_word)


def search_file(f, magic_word):
    """Checks each line of a given file and searches for a given string"""
    logger.info("searching {} for instances of {}".format(f, magic_word))

    with open(f) as doc:
        start_line = checked_files[f]
        content = doc.readlines()[start_line:]
        i = 0
        for i, line in enumerate(content, start=start_line):
            if magic_word in line:
                logger.info("Match found for {} found on line {} in {}"
                            .format(magic_word, i+1, f))
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
    logger.warning('Received {}'.format(signame[sig_num]))
    global exit_flag
    exit_flag = True


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='directory to monitor')
    parser.add_argument('magic_word', help='The magic word/words to watch for')
    parser.add_argument('-i',
                        '--interval',
                        help='Sets the interval in seconds to check the '
                             'directory for magic words',
                        type=float,
                        default=1.0)
    parser.add_argument('-x', '--extension', help='Sets the type of file to '
                                                  'watch for', default='.txt')
    return parser


def main(args):
    """Main function is declared as standalone, for testability"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    logger.info(parsed_args)
    logger.info("Starting App")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    start_time = time.time()

    while not exit_flag:
        try:
            magic_word_finder(
                parsed_args.directory,
                parsed_args.magic_word,
                parsed_args.extension,
            )
            time.sleep(parsed_args.interval)
        except OSError as e:
            logger.warning(e)
            time.sleep(10)
        except Exception as e:
            logger.exception(e)
            time.sleep(10)

    logger.info("\nExiting.\n"
                "Process ran for {} seconds".format(time.time() - start_time))


if __name__ == '__main__':
    """Runs the main loop until an interrupt like control+c are input."""
    logger.info("My Pid is {}".format(os.getpid()))
    logger.info("Command line arguments: {}".format(sys.argv))
    main(sys.argv[1:])

