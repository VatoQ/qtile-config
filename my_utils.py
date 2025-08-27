"""
This is a collection of constants for the qtile config
"""
import os
from qtile_extras.widget.decorations import (
    PowerLineDecoration,
    RectDecoration
)

WALLPAPERS_PATH = os.path.expanduser("~/Pictures/Wallpapers/")


TIMER_MINUTES = 30

BAR_NORMAL = 0

BAR_CHOICE_LEFT = 1

BAR_CHOICE_RIGHT = 2

BAR_CHOICE_LEFT_SLASH = 3

BAR_CHOICE_RIGHT_SLASH = 4

mod = "mod4"
terminal = "kitty"  # guess_terminal()
power_menu = "~/.config/qtile/scripts/powermenu"



YELLOW      = "#FFEE28"
ORANGE      = "#FFAA28"
MAGENTA     = "#FF28AA"
RED         = "#F02850"
LIME        = "#AAFF28"
LIGHT_GREEN = "#28FFAA"
CYAN        = "#28AAFF"
BLUE        = "#2828FF"
GRAY        = "#ABABAB"


def dim_color(color:str, factor:float) -> str:
    """
    dim a given color hex code by a given factor.

    :param color: hexcode of a color. format: `#XXXXXX`
    :param factor: positive real number, where 1.0 does 
    nothing and the larger it is, the darker the color gets.
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    color:list[int] = [r, g, b]
    color_str:list[str] = []


    for i in range(len(color)):
        color[i] = int(color[i] / factor)

        color_str.append(f"{color[i]:02x}")

    return "#" + "".join(color_str)





FOCUS_COLOR = ORANGE
SECONDARY_COLOR = YELLOW
NORMAL_COLORS = dim_color(FOCUS_COLOR, factor=1.5)
POINT1 = (0, 0)
POINT2 = (0, 1)

def get_decoration_group(choice: int):
    result = {}

    if choice == BAR_NORMAL:
        result["decorations"] = [
            RectDecoration(
                colour="#004040", radius=2, filled=True, padding=0, group=True
            )
        ]

        result["padding"] = 20

    elif choice == BAR_CHOICE_LEFT:
        result["decorations"] = [
            RectDecoration(
                # colour="#004040",
                use_widget_background=True,
                padding_y=5,
                filled=True,
                radius=3,
            ),
            PowerLineDecoration(path="rounded_left", padding_y=0),
        ]

        result["padding"] = 15
        # result["height"] = 30

    elif choice == BAR_CHOICE_RIGHT:
        result["decorations"] = [
            RectDecoration(
                # colour="#004040",
                use_widget_background=True,
                padding_y=5,
                filled=True,
                radius=3,
            ),
            PowerLineDecoration(path="rounded_right", padding_y=0),
        ]
        result["padding"] = 15

    return result


