"""
This is a collection of constants for the qtile config.
"""
# pyright: reportUnknownVariableType=false
# pyright: reportAny=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# pyright: reportUntypedFunctionDecorator=false
# pyright: reportUnknownMemberType=false
import os
import re
import json

from libqtile.utils import send_notification
from qtile_extras.widget.decorations import (
    PowerLineDecoration,
    RectDecoration
)
from qtile_extras.layout.decorations import GradientBorder
from qtile_extras.widget.groupbox2 import GroupBoxRule
from libqtile.log_utils import logger
from libqtile import qtile

###################
#### WALLPAPER ####
###################

WALLPAPERS_PATH = os.path.expanduser("~/Pictures/Wallpapers/")


TIMER_MINUTES = 30


################################
#### COMMON CONSTANT VALUES ####
################################

launcher = ""
file_manager = ""

if qtile.core.name == "x11":
    term = "urxvt"
    launcher = "rofi -show drun"
    file_manager = "thunar"
elif qtile.core.name == "wayland":
    term = "foot"
    launcher = "wofi --show drun"
    file_manager = "dolphin"

MOD = "mod4"
TERMINAL = "kitty"
POWER_MENU = "~/.config/qtile/scripts/powermenu"
SHIFT = "shift"
CONTROL = "control"
SPACE = "space"
LOCK_SCREEN = "~/.config/qtile/lock.py"
BORDER_WIDTH = 4
MIN_BORDER_WIDTH = BORDER_WIDTH
MAX_BORDER_WIDTH = int(1.5 * BORDER_WIDTH)
BORDER_RADIUS = 18
BAR_HEIGHT = 41



#######################
#### COLOR SECTION ####
#######################
# not really fitting, consider adding later: #EEFF28
# not really fitting, consider adding later: #FF28EE
# not really fitting, consider adding later: #EE28FF
# not really fitting, consider adding later: #28FFEE
# not really fitting, consider adding later: #28EEFF
_COLOR_SCHEME_PATH = "~/.config/qtile/color_scheme.jsonc"

with open(os.path.expanduser(_COLOR_SCHEME_PATH), encoding="utf-8") as color_scheme_json:
    json_data:dict[str,str] = json.load(color_scheme_json)

def match_color_hexcode(color:str) -> bool:
    x = re.fullmatch("#([0-9a-fA-F]{6})",color)
    return bool(x)

failed_colors:list[str] = []


json_color_keys = [
    "yellow",
    "orange",
    "red",
    "magenta",
    "purple",
    "blue",
    "cyan",
    "light_green",
    "green",
    "lime",
    "gray",
]

for key in json_color_keys:
    value = json_data[key]
    if not match_color_hexcode(value):
        message = f"Value {value} is not a full rgb hexcode. Only the format `#RRGGBB` is allowed in color_scheme.jsonc"
        #print(message)
        logger.warning(message)
        failed_colors.append(key)
        # _ = json_data.pop(key)

for key in failed_colors:
    _ = json_data.pop(key)

# Fallback colorscheme:
_YELLOW =        "#FFEE28"
_ORANGE =        "#FFAA28"
_RED =           "#FF2828"
_MAGENTA =       "#FF28AA"
_PURPLE =        "#AA28FF"
_BLUE =          "#2828FF"
_CYAN =          "#28AAFF"
_LIGHT_GREEN =   "#28FFAA"
_GREEN =         "#28FF28"
_LIME =          "#AAFF28"
_GRAY =          "#A2A29A"

YELLOW       = json_data.get("yellow", _YELLOW)
ORANGE       = json_data.get("orange", _ORANGE)
RED          = json_data.get("red", _RED)
MAGENTA      = json_data.get("magenta", _MAGENTA)
PURPLE       = json_data.get("purple", _PURPLE)
BLUE         = json_data.get("blue", _BLUE)
CYAN         = json_data.get("cyan", _CYAN)
LIGHT_GREEN  = json_data.get("light_green", _LIGHT_GREEN)
GREEN        = json_data.get("green", _GREEN)
LIME         = json_data.get("lime", _LIME)
GRAY         = json_data.get("gray", _GRAY)

_A = 0.0244048
_B = -0.219048
_C = 0.694643
_D = 0.5

def _interpolating_polynomial(x:float) -> float:
    return _A * x ** 3 + _B * x ** 2 + _C * x + _D

##Original intuitive basis for the interpolation function.
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

# Quotients to be used in dim_color() and dim_color_alpha()
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

_M_ALPHA = 13.0
_B_ALPHA = 173.0

def _alpha_interpolation(x:float) -> float:
    if x == 0.0:
        return 0.0
    return _M_ALPHA * x + _B_ALPHA

# 0x00,
# 0xBB
# 0xC0,
# 0xCC,
# 0xE0,
# 0xEE,

TRANSPARENT  = "00"
TRANSLUCENT0 = "22"
TRANSLUCENT1 = "99" #hex(int(_alpha_interpolation(1)))[2:]
TRANSLUCENT2 = hex(int(_alpha_interpolation(2)))[2:]
TRANSLUCENT3 = hex(int(_alpha_interpolation(3)))[2:]
TRANSLUCENT4 = hex(int(_alpha_interpolation(4)))[2:]
TRANSLUCENT5 = hex(int(_alpha_interpolation(5)))[2:]



def dim_color(color:str, quotient:float) -> str:
    """
    dim a given color hex code by a given factor.

    :param color: hexcode of a color. format: `#XXXXXX`
    ## list of reccomended constants:
        - YELLOW
        - ORANGE
        - RED
        - MAGENTA
        - PURPLE
        - BLUE
        - CYAN
        - LIGHT_GREEN
        - GREEN
        - LIME
        - GRAY

    :param factor: positive real number, where 1.0 does 
    nothing and the larger it is, the darker the color gets.
    ## list of reccomended constants:
        - LIGHT
        - NEUTRAL
        - DIMMED
        - DIMMED2
        - MEDIUM
        - MEDIUM2
        - DARKER
        - DARKER2
        - DARK
        - DARK2

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
    ## list of reccomended constants:
        - YELLOW
        - ORANGE
        - RED
        - MAGENTA
        - PURPLE
        - BLUE
        - CYAN
        - LIGHT_GREEN
        - GREEN
        - LIME
        - GRAY
    :param quotient: positive real number, where 1.0 does 
    nothing and the larger it is, the darker the color gets.
    ## list of reccomended constants:
        - LIGHT
        - NEUTRAL
        - DIMMED
        - DIMMED2
        - MEDIUM
        - MEDIUM2
        - DARKER
        - DARKER2
        - DARK
        - DARK2
    :param alpha: alpha channel. Format: `XX` (hexadecimal)
    :return: the dimmed color in the format `#XXXXXXXX`
    """
    return dim_color(color, quotient) + alpha


_THEME = json_data.get("theme", "sunset")

_focus_color = BLUE
_secondary_color = GRAY

if _THEME == "sunset":
    _focus_color = ORANGE
    _secondary_color = YELLOW
elif _THEME == "ocean":
    _focus_color = BLUE
    _secondary_color = CYAN
elif _THEME == "forest":
    _focus_color = GREEN
    _secondary_color = LIGHT_GREEN

FOCUS_COLOR = _focus_color
SECONDARY_COLOR = _secondary_color

NORMAL_COLORS = dim_color(FOCUS_COLOR, quotient=DIMMED2)
POINT1 = (0, 0)
POINT2 = (0, 1)

logger.info(f"Colortheme:\n\tPrimary: {FOCUS_COLOR}\n\tSecondary: {SECONDARY_COLOR}\n\tTertiary: {NORMAL_COLORS}")

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

        result["padding"] = 15

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
                #padding_x=40,
                filled=True,
                radius=3,
            ),
            PowerLineDecoration(path="rounded_right", padding_y=0),
        ]
        result["padding"] = 15

    return result


_SPECIAL_LABELS = {
        "term": "",
        "fox": "󰈹",
        "steam": "",
        }

_SL_VALS = [value for key, value in _SPECIAL_LABELS.items()]

def _set_label(rule, box) -> bool:
    """
    Sets labels to group icons in GroupBox2

    :return: True
    """
    if box.focused and rule.text not in _SL_VALS:
        rule.text = "◉"
    elif box.occupied and rule.text not in _SL_VALS:
        rule.text = "◎"
    else:
        rule.text = "○"

    return True

def _has_window_class(name, rule, box) -> bool:
    for win in box.group.windows:
        win_info = win.info()
        win_class = win_info["wm_class"]

        # send_notification(
        #         "qtile",
        #         f"looking at window {win_class}"
        #         )

        if name in win_class:
            return True

    return False


def _has_terminal(rule, box) -> bool:
    return _has_window_class("kitty", rule, box)

def _has_firefox(rule, box) -> bool:
    return _has_window_class("firefox", rule, box)

def _has_steam(rule, box) -> bool:
    return _has_window_class("steam", rule, box)

GROUPBOX_RULES = [
    GroupBoxRule(text_colour=dim_color(FOCUS_COLOR, NEUTRAL)).when(screen=GroupBoxRule.SCREEN_THIS),
    GroupBoxRule(text_colour=dim_color(FOCUS_COLOR, DIMMED2)).when(occupied=True),
    GroupBoxRule(text_colour=dim_color(SECONDARY_COLOR, DARK)).when(occupied=False),
    GroupBoxRule(text=_SPECIAL_LABELS["fox"]).when(func=_has_firefox),
    GroupBoxRule(text=_SPECIAL_LABELS["steam"]).when(func=_has_steam),
    GroupBoxRule(text=_SPECIAL_LABELS["term"]).when(func=_has_terminal),
    GroupBoxRule().when(func=_set_label),
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
        "border_width": BORDER_WIDTH,
        "border_focus": _gradient_border,
        "border_normal": NORMAL_COLORS,
        "border_on_single": True,
        "wrap_clients": True,
        "lower_right": True,
        "fair": True,
        "decorations": [_gradient_border],
    }
