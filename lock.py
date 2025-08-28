#!/bin/python


import subprocess
from my_utils import *


BLANK       = dim_color_alpha(GRAY, DARK2, "00")
CLEAR       = dim_color_alpha(GRAY, LIGHT, "22")
DEFAULT     = dim_color_alpha(FOCUS_COLOR, NEUTRAL, "CC")
TEXT        = dim_color_alpha(FOCUS_COLOR, DIMMED, "EE")
WRONG       = dim_color_alpha(RED, NEUTRAL, "BB")
NOT_WRONG   = dim_color_alpha(GREEN, NEUTRAL, "BB")
VERIFYING   = dim_color_alpha(YELLOW, DIMMED2, "BB")

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





_ = subprocess.run(command, check=False)
