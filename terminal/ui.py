import curses
import locale
import os
import signal
import sys
import time
import threading
import textwrap
import random
import psutil
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Tuple, Optional

H = "─"
V = "│"
TL = "┌"
TR = "┐"
BL = "└"
BR = "┘"
LT = "├"
RT = "┤"
TT = "┬"
BT = "┴"
DBL = "═"
DTL = "╔"
DTR = "╗"
DBL2 = "╚"
DBR = "╝"
BLOCK = "█"
HALF = "░"
DOT = "●"

CP_ORANGE = 1
CP_WHITE = 2
CP_GREEN = 3
CP_RED = 4
CP_CYAN = 5
CP_YELLOW = 6
CP_DIM = 7
CP_HDR = 8
CP_ORANGE2 = 9
CP_SELECTED = 10

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"
ROLE_ERROR = "error"

def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    can_custom = curses.can_change_color() and curses.COLORS >= 256

    if can_custom:
        curses.init_color(16, 1000, 430, 0)
        OG = 16
    else:
        OG = curses.COLOR_YELLOW

    curses.init_pair(CP_ORANGE, OG, -1)

def safestr(win, y: int, x: int, text: str, attr: int = 0):
    try:
        max_y, max_x = win.getmaxyx()
        if y < 0 or y >= max_y or x >= max_x - 1:
            return
        if x < 0:
            text = text[-x:]
            x = 0
        avail = max_x - x - 1
        if avail <= 0:
            return
        win.addstr(y, x, text[:avail], attr)
    except curses.error:
        pass
def draw_border(win, title: str = "", title_attr: int = 0):
    h, w = win.getmaxyx()
    ca = curses.color_pair(CP_ORANGE)

    safestr(win, 0, 0, TL + H * (w - 2) + TR, ca)
    safestr(win, h -1, 0, BL + H * (w - 2) + BR, ca)

    for y in range(1, h - 1):
        safestr(win, y, 0, V, ca)
        safestr(win, y, w - 1, V, ca)

    if title:
        s = f" {title} "
        tx = max(2, (w - len(s)) // 2)
        safestr(win, 0, tx, s,
                title_attr or (curses.color_pair(CP_ORANGE) | curses.A_BOLD))
        
def main(stdscr):
    curses.curs_set(0)
    setup_colors()

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        draw_border(stdscr, "ORIGIN AI")

        msg = "press 'q' to quit"
        safestr(stdscr, h // 2, (w - len(msg)) // 2, msg,
                curses.color_pair(CP_ORANGE))
        
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
