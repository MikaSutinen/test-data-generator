"""
Ensures all keyboard hooks are removed, flushes input buffers, and exits cleanly.
Started already putting together Linux support, but will need to work on that bit more elsewhere in the code.
"""

import sys
import keyboard
from modules.logger import get_logger

logger = get_logger(__name__)

def clean_exit(RUNNING_OS):
    logger.info("Exiting test data generator cleanly.")
    keyboard.unhook_all()
    if RUNNING_OS == 'Windows':
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        import termios
        import tty
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    print("Exiting test data generator...")
    sys.exit(0)

def flush_input(RUNNING_OS):
    try:
        if RUNNING_OS == 'Windows':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios
            import tty
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except ImportError:
        pass