"""
Contains `bar_layout()`, which returns a Bar object.
"""

import copy
from qtile_extras import widget as extrawidgets
from qtile_extras.widget.decorations import GradientDecoration, PowerLineDecoration, RectDecoration
from libqtile import bar
from my_utils import (
    FOCUS_COLOR,
    SECONDARY_COLOR,
    BLUE,
    GRAY,
    CYAN,
    RED,
    dim_color,
    DARK,
    DARK2,
    DARKER,
    DARKER2,
    MEDIUM2,
    DIMMED2,
    NEUTRAL,
    LIGHT,
    GROUPBOX_RULES,
    get_decoration_group,
    BAR_NORMAL,
    BAR_CHOICE_LEFT,
    BAR_CHOICE_RIGHT,
)

def bar_layout() -> bar.Bar:
    """
    Defines a nice layout for the status bar.

    :return: a Bar object that contains some widgets with decorations.
    """
    decoration_group = get_decoration_group(BAR_NORMAL)
    decorations_left = get_decoration_group(BAR_CHOICE_LEFT)
    decorations_right = get_decoration_group(BAR_CHOICE_RIGHT)

    # some widgets look better with slightly other settings:
    workspace_decoration = decorations_left.copy()
    workspace_decoration["padding"] = 6
    workspace_decoration["decorations"][0] = RectDecoration(
        use_widget_background=True,
        padding_y=20,
        filled=True,
        radius=9,
    )


    wifi_decoration =  decorations_right.copy()
    wifi_decoration["padding"] = 8

    most_right_widget_deccoration = copy.deepcopy(decorations_right)
    # most_right_widget_deccoration["decorations"][1] = PowerLineDecoration(
    #         path="arrow_left",
    #         padding_y=0
    #         )
    most_right_widget_deccoration["decorations"] = [
            RectDecoration(
                use_widget_background=True,
                padding_y=-16,
                filled=True,
                radius=9,
                )
            ]

    return bar.Bar(
        [
            extrawidgets.CurrentLayoutIcon(
                background=dim_color(BLUE, DARKER), 
                **decorations_left
            ),
            extrawidgets.GroupBox2(
                fontsize=20,
                highlight_method="block",
                background=dim_color(GRAY, DARK),
                hide_unused=True,
                rules=GROUPBOX_RULES,
                **workspace_decoration,
            ),
            extrawidgets.WindowName(
                background=dim_color(GRAY, MEDIUM2),
                **decorations_right
            ),
            extrawidgets.WiFiIcon(
                background=dim_color(BLUE, DARK2),
                interface="wlp2s0",
                wifi_arc=75,
                **wifi_decoration,
                ),
            extrawidgets.Bluetooth(
                background=dim_color(BLUE, DARK2),
                fontsize=25,
                default_text="󰂯 {connected_devices}",
                **decorations_right
                ),
            extrawidgets.Systray(
                background=dim_color(BLUE, DARK2),
                hide_crash=True, # Systray tends to crash on reload because of singleton rule
                **decorations_right
                ),
            extrawidgets.Clock(
                background=dim_color(BLUE, DARKER2),
                #fontsize=11,
                format="%a %d.%m.%y",
                #**decorations_right,
            ),
            extrawidgets.AnalogueClock(
                background=dim_color(BLUE, DARKER2),
                face_shape="circle",
                face_border_colour=dim_color(CYAN, NEUTRAL),
                second_colour=dim_color(CYAN, LIGHT),
                hour_colour=dim_color(CYAN, LIGHT),
                minute_colour=dim_color(CYAN, LIGHT),
                face_background=dim_color(CYAN, DARKER2),
                face_border_width=2,
                second_size=1,
                second_length=0.7,
                minute_length=0.7,
                hour_length=0.5,
                **decorations_right,
            ),
            extrawidgets.Battery(
                background=dim_color(BLUE, DARKER),
                format="{char} {percent:2.0%}",
                empty_char="󰁺",
                discharge_char="󰁿",
                charge_char="󰂄",
                full_char="󰁹",
                low_background=RED,
                low_percentage=0.2,
                charge_controller=lambda: (0, 95),
                update_interval= 4,
                **decorations_right,
            ),
            extrawidgets.BrightnessControl(
                name="brightness",
                background=dim_color(CYAN, MEDIUM2),
                bar_colour=dim_color(CYAN, DARKER2),
                bar_height=25,
                min_brightness=35,
                device="/sys/class/backlight/amdgpu_bl1",
                format="󰃝 {percent:2.0%}",
                #hide_when_unavailable=False,
                mode="bar",
                #popup_hide_timeout=60,
                step=5,
                timeout_interval=5,
                **decorations_right
            ),
            extrawidgets.PulseVolume(
                name="volume",
                volume_app = "pavucontrol",
                emoji_list = [
                    "",
                    "",
                    "",
                    "",
                    ],
                background = dim_color(CYAN, DIMMED2), 
                emoji=True, 
                **decorations_right
            ),
            extrawidgets.ScriptExit(
                background=dim_color(RED, NEUTRAL),
                default_text="󰅙",
                countdown_format="{}",
                countdown_start=5,
                **most_right_widget_deccoration,
            ),
            # extended_clock,
        ],
        41,
        # radius=10,
        # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
        # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
    )
