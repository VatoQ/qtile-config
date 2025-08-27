"""
This is a collection of constants for the qtile config
"""

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
