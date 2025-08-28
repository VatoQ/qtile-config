"""
This is a collection of constants for the qtile config
"""
import os
from qtile_extras.widget.decorations import (
    PowerLineDecoration,
    RectDecoration
)
from qtile_extras.layout.decorations import GradientBorder
from qtile_extras.widget.groupbox2 import GroupBoxRule

###################
#### WALLPAPER ####
###################

WALLPAPERS_PATH = os.path.expanduser("~/Pictures/Wallpapers/")


TIMER_MINUTES = 30


######################################
#### COMMON PROGRAMS AND BINDINGS ####
######################################

MOD = "mod4"
TERMINAL = "kitty"
POWER_MENU = "~/.config/qtile/scripts/powermenu"
SHIFT = "shift"
CONTROL = "control"
SPACE = "space"
LOCK_SCREEN = "~/.config/qtile/lock.py"



#######################
#### COLOR SECTION ####
#######################
# not really fitting, consider adding later: #EEFF28
# not really fitting, consider adding later: #FF28EE
# not really fitting, consider adding later: #EE28FF
# not really fitting, consider adding later: #28FFEE
# not really fitting, consider adding later: #28EEFF
YELLOW =        "#FFEE28"
ORANGE =        "#FFAA28"
RED =           "#FF2828"
MAGENTA =       "#FF28AA"
PURPLE =        "#AA28FF"
BLUE =          "#2828FF"
CYAN =          "#28AAFF"
LIGHT_GREEN =   "#28FFAA"
GREEN =         "#28FF28"
LIME =          "#AAFF28"
GRAY =          "#A2A29A"


_A = 0.0244048
_B = -0.219048
_C = 0.694643
_D = 0.5

def _interpolating_polynomial(x:float) -> float:
    return _A * x ** 3 + _B * x ** 2 + _C * x + _D

# quotients = [
#         0.5,    # LIGHT
#         1,      # NEUTRAL
#         1.3,    # DIMMED
#         1.5,    # DIMMED2
#         1.8,    # MEDIUM
#         2,      # MEDIUM2
#         2.5,    # DARKER
#         3,      # DARKER2
#         4,      # DARK
#         6.8     # DARK2
#         ]

LIGHT       = _interpolating_polynomial(0)
NEUTRAL     = _interpolating_polynomial(1)
DIMMED      = _interpolating_polynomial(2)
DIMMED2     = _interpolating_polynomial(3)
MEDIUM      = _interpolating_polynomial(4)
MEDIUM2     = _interpolating_polynomial(5)
DARKER      = _interpolating_polynomial(6)
DARKER2     = _interpolating_polynomial(7)
DARK        = _interpolating_polynomial(8)
DARK2       = _interpolating_polynomial(9)



def dim_color(color:str, quotient:float) -> str:
    """
    dim a given color hex code by a given factor.

    :param color: hexcode of a color. format: `#XXXXXX`
    :param factor: positive real number, where 1.0 does 
    nothing and the larger it is, the darker the color gets.
    :return: the dimmed color in the format `#XXXXXX`
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    color_int:list[int] = [r, g, b]
    color_str:list[str] = []


    for ci in color_int:
        ci = int(ci / quotient)
        ci = min(255, ci)
        color_str.append(f"{ci:02x}")

    return "#" + "".join(color_str)

def dim_color_alpha(color:str, quotient:float, alpha:str) -> str:
    """
    Dims a given color by a given quotient. The larger the quotient, the
    darker the color.

    :param color: hexcode of a color. format: `#XXXXXX`
    :param quotient: positive real number, where 1.0 does 
    nothing and the larger it is, the darker the color gets.
    :param alpha: alpha channel. Format: `XX` (hexadecimal)
    :return: the dimmed color in the format `#XXXXXXXX`
    """
    return dim_color(color, quotient) + alpha

FOCUS_COLOR = ORANGE
SECONDARY_COLOR = YELLOW
NORMAL_COLORS = dim_color(FOCUS_COLOR, quotient=1.5)
POINT1 = (0, 0)
POINT2 = (0, 1)


########################
#### BAR DECORATION ####
########################

BAR_NORMAL = 0
BAR_CHOICE_LEFT = 1
BAR_CHOICE_RIGHT = 2
BAR_CHOICE_LEFT_SLASH = 3
BAR_CHOICE_RIGHT_SLASH = 4

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
                use_widget_background=True,
                padding_y=5,
                filled=True,
                radius=3,
            ),
            PowerLineDecoration(path="rounded_left", padding_y=0),
        ]

        result["padding"] = 15

    elif choice == BAR_CHOICE_RIGHT:
        result["decorations"] = [
            RectDecoration(
                use_widget_background=True,
                padding_y=5,
                filled=True,
                radius=3,
            ),
            PowerLineDecoration(path="rounded_right", padding_y=0),
        ]
        result["padding"] = 15

    return result


def set_label(rule, box) -> bool:
    """
    Sets labels to group icons in GroupBox2

    :return: True
    """
    if box.focused:
        rule.text = "◉"
    elif box.occupied:
        rule.text = "◎"
    else:
        rule.text = "○"

    return True

GROUPBOX_RULES = [
    GroupBoxRule(text_colour=dim_color(YELLOW, 1.4)).when(screen=GroupBoxRule.SCREEN_THIS),
    GroupBoxRule(text_colour=dim_color(CYAN, 1.4)).when(occupied=True),
    GroupBoxRule(text_colour=dim_color(CYAN, 2.7)).when(occupied=False),
    GroupBoxRule().when(func=set_label)
]

################
#### LAYOUT ####
################

_gradient_border = GradientBorder(colours=[FOCUS_COLOR, SECONDARY_COLOR],
                                 radial=False)

def init_layout_theme():
    """
    Returns a dict of arguments for layout config. should be
    unpacked as kwargs to a layout constructor like this:

    ```
    layout_theme = init_layout_theme()

    layout.Bsp(**layout_theme)
    ```
    """
    return {
        "margin": 5,
        "border_width": 4,
        "border_focus": _gradient_border,
        "border_normal": NORMAL_COLORS,
        "border_on_single": True,
        "wrap_clients": True,
        "lower_right": True,
        "fair": True,
        "decorations": [_gradient_border],
    }



