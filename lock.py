#!/bin/python

import sys
import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from my_utils import (
        BLUE,
        CYAN,
        GRAY,
        GREEN,
        RED,
        ORANGE,
        PURPLE,
        YELLOW,
        FOCUS_COLOR,
        dim_color
)
import subprocess

BLANK = dim_color(GRAY, 5) + "00"
CLEAR = dim_color(GRAY, 0.5) + "22"
DEFAULT = dim_color(FOCUS_COLOR, 1.0) + "CC"
TEXT = dim_color(FOCUS_COLOR, 1.3) + "EE"
WRONG = dim_color(RED, 1.0) + "BB"
NOT_WRONG = dim_color(GREEN, 1.0) + "BB"
VERIFYING = dim_color(YELLOW, 1.5) + "BB"

command = [
    "i3lock",
    f"--insidever-color={CLEAR}",
    f"--ringver-color={VERIFYING}",

    f"--insidewrong-color={CLEAR}",
    f"--ringwrong-color={WRONG}",

    f"--inside-color={BLANK}",
    f"--ring-color={DEFAULT}",
    f"--line-color={BLANK}",
    f"--separator-color={DEFAULT}",

    f"--verif-color={TEXT}",
    f"--wrong-color={TEXT}",
    f"--time-color={TEXT}",
    f"--date-color={TEXT}",
    f"--layout-color={TEXT}",
    f"--keyhl-color={NOT_WRONG}",
    f"--bshl-color={NOT_WRONG}",

    "--screen", "1",
    "--blur", "5",
    "--clock",
    "--indicator",
    '--time-str="%H:%M:%S"',
    '--date-str="%a, %d.%m.%y"',
    "--keylayout", "1"
]

subprocess.run(command)
