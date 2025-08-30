#!/bin/python

import subprocess
from my_utils import (
        FOCUS_COLOR,
        GRAY,
        RED,
        GREEN,
        YELLOW,
        LIGHT,
        NEUTRAL,
        DIMMED,
        DIMMED2,
        DARK2,
        TRANSPARENT,
        TRANSLUCENT0,
        TRANSLUCENT1,
        TRANSLUCENT3,
        TRANSLUCENT5,
        dim_color_alpha
)

BLANK       = dim_color_alpha(GRAY, DARK2, TRANSPARENT)
CLEAR       = dim_color_alpha(GRAY, LIGHT, TRANSLUCENT0)
DEFAULT     = dim_color_alpha(FOCUS_COLOR, NEUTRAL, TRANSLUCENT3)
TEXT        = dim_color_alpha(FOCUS_COLOR, DIMMED, TRANSLUCENT5)
WRONG       = dim_color_alpha(RED, NEUTRAL, TRANSLUCENT1)
NOT_WRONG   = dim_color_alpha(GREEN, NEUTRAL, TRANSLUCENT1)
VERIFYING   = dim_color_alpha(YELLOW, DIMMED2, TRANSLUCENT1)

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

    f"--verif-color={VERIFYING}",
    f"--wrong-color={WRONG}",
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
