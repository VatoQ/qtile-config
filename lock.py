#!/bin/python
"""
This module launches i3lock-color with the colorscheme defined in
this configuration.
"""

import subprocess
from my_utils import (
        FOCUS_COLOR,
        GRAY,
        RED,
        GREEN,
        SECONDARY_COLOR,
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
CLEAR       = dim_color_alpha(SECONDARY_COLOR, LIGHT, TRANSLUCENT0)
DEFAULT     = dim_color_alpha(FOCUS_COLOR, NEUTRAL, TRANSLUCENT3)
TEXT        = dim_color_alpha(FOCUS_COLOR, DIMMED, TRANSLUCENT5)
WRONG       = dim_color_alpha(RED, NEUTRAL, TRANSLUCENT1)
INSIDE_WRONG= dim_color_alpha(RED, NEUTRAL, TRANSLUCENT0)
NOT_WRONG   = dim_color_alpha(GREEN, NEUTRAL, TRANSLUCENT1)
VERIFYING   = dim_color_alpha(YELLOW, DIMMED2, TRANSLUCENT1)

command = [
    "i3lock",
    f"--insidever-color={CLEAR}",
    f"--ringver-color={VERIFYING}",

    f"--insidewrong-color={INSIDE_WRONG}",
    f"--ringwrong-color={WRONG}",

    f"--inside-color={CLEAR}",
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
    "--blur", "2",
    "--clock",
    "--indicator",
    '--time-str=%H:%M:%S',
    '--date-str=%a, %d.%m.%y',
    "--keylayout", "1"
]

_ = subprocess.run(command, check=False)
