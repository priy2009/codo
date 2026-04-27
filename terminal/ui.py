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

H   = "─"
V   = "│"
TL  = "┌"
TR  = "┐"
BL  = "└"
BR  = "┘"
LT  = "├"
RT  = "┤"
TT  = "┬"
BT  = "┴"
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

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"
ROLE_ERROR = "error"

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
        self.chat_scroll = 0
        self.file_scroll = 0
        self.selected_file: Optional[Path] = None
        self.thinking = False
        self.think_frame = 0
        self.running = True
        self.agent_state = "AWAITING INPUT"
        self.session_start = datetime.now()
        self._history: List[str] = []
        self._hist_idx = -1
        self.expanded_paths = set()
        self.focused_panel = "chat"

        self.metrics = {
            "cpu": [0.25, 0.40, 0.55, 0.35, 0.65, 0.50, 0.45],
            "mem_used": 2.0,
            "mem_total": 8.0,
        }
        self._metrick_lock = threading.Lock()
        self._start_metrics_thread()

        self.file_tree: List[Tuple[int, str, bool, Path]] = []
        self._refresh_tree()


def launch(
    ai_callback: Callable[[str], str],
    root_dir: str = ".",
    project_name: str = "ROOT_DIR",
):
    def _main(stdscr):
        ui = CodoUI(
            stdscr=stdscr,
            ai_callback=ai_callback,
            root_dir=root_dir,
            project_name=project_name,
        )
        ui.run()

    locale.setlocale(locale.LC_ALL, '')
    os.environ.setdefault("TERM", "xterm-256color")
    curses.wrapper(_main)















