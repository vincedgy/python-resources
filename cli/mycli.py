#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI program
"""
# Args
import argparse
# Logging
import logging
# Colors
from colorama import Fore, Back, Style    
# Progress bar (tqdm)
import time
from tqdm import tqdm
# Ini file
from ConfigParser import SafeConfigParser
from os.path import dirname, join, expanduser
INSTALL_DIR = dirname(__file__)
# Signals
import signal


# Parser args
def init_parser():
    """ Initialize command options parser """
    parser = argparse.ArgumentParser(description="This is a simple CLI program with Python")
    parser.add_argument(
        "-L", "--logLevel",
        dest="logLevel",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Set the logging level (default is WARNING)",
        default="INFO")
    parser.add_argument(
        '-l', '--log',
        dest="logout",
        help='the file where log information is written.')
    # Program argument
    parser.add_argument('name', nargs='?')
    # Defining logging
    args = parser.parse_args()
    logging.basicConfig(
        level=getattr(logging, args.logLevel),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        filename=args.logout,
        filemode='a'
        )
    return parser

#
# Signals Handlers
def mysiginfofunc():
    print 'Interrupted'
signal.siginterrupt(signal.SIGINFO, False)
signal.signal(signal.SIGINFO, mysiginfofunc)

# --------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------
def app_main():
    """ Main """
    #
    # Get parser
    parser = init_parser()
    args = parser.parse_args()
    # Verify logging
    logging.info("\n-1- Arguments are %s", format(args))
    #
    # Display content of grabed argument
    name = (args.name or 'World')
    print("\n-2- Hello {} !".format(name))
    #
    # Play with a progress bar
    print "\n-3- Progress bar display"
    for i in tqdm(range(1000)):
        time.sleep(0.0005)
    #
    # Read from init config file
    print "\n-4- Get config from multiple ini files and compose a whole set "
    config = SafeConfigParser()
    config.read([
        join(INSTALL_DIR, 'defaults.ini'),
        expanduser('project.ini'),
        expanduser('tool.ini'),
        'config.ini'
        ])
    print config.get('server', 'host')
    print config.getint('server', 'port')
    print config.get('server', 'url')
    #
    # Interrupts from keyboard
    verified=False
    try:
        print "\n-5- Waiting 5sec for keyboard interruption via Ctrl+C"
        time.sleep(5)
    except KeyboardInterrupt:
        print "Interruption verified"
        verified=True
        pass
    if verified:
        print "Verified !"
    else:
        print "Not interrupted..."
    #
    # 
    print "\nContinue..."



# -----------------------------------------------------------------
# Main call
if __name__ == '__main__':
    app_main()
