"""
Ensures all keyboard hooks are removed, flushes input buffers, and exits cleanly.
Started already putting together Linux support, but will need to work on that bit more elsewhere in the code.
"""

import os
import sys
import keyboard

def clean_exit():
    keyboard.unhook_all()
    
    # Clear input buffer
    if os.name == 'nt':
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        import termios
        import tty
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    
    print("Exiting test data generator...")
    sys.exit(0)
