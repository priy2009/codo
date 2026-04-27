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
DBL2= "╚"
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

ROLE_USER      = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM    = "system"
ROLE_ERROR     = "error"

class CodoUI:
    def __init__(
        self,
        stdscr,
        ai_callback: Callable[[str], str],
        root_dir: str = ".",
        project_name: str = "ROOT_DIR",
    ):
        self.stdscr = stdscr
        self.ai_callback = ai_callback
        self.root_dir = Path(root_dir).resolve()
        self.project_name = project_name

        self.messages: List[Tuple[str, str]] = []
        self.input_buffer = ""
        self.cursor_pos = 0
        self.running = True
        self.session_start = datetime.now()

        self.h = self.w = 0
        self._compute_layout()

        self._init_curses()

        signal.signal(signal.SIGWINCH, self._on_sigwinch)
