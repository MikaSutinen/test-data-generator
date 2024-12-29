"""
A simple logger for logging INFO and ERROR messages from the modules.
"""

import logging

# ANSI escape codes for colors
YELLOW = '\033[93m'
RESET = '\033[0m'

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=f'{YELLOW}TIME:{RESET} %(asctime)s {YELLOW}SEVERITY:{RESET} %(levelname)s {YELLOW}MODULE:{RESET} %(module)s {YELLOW}MESSAGE:{RESET} %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

def get_logger(name):
    return logging.getLogger(name)