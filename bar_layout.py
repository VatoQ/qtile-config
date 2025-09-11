"""
Contains `bar_layout()`, which returns a Bar object.
"""
# pyright: reportUnknownVariableType=false
# pyright: reportAny=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# pyright: reportUntypedFunctionDecorator=false
# pyright: reportUnknownMemberType=false

import copy
from qtile_extras import widget as extrawidgets
from qtile_extras.widget.decorations import RectDecoration
from libqtile import bar, lazy
from my_utils import (
    BAR_HEIGHT,
    BLUE,
    BORDER_WIDTH,
    DIMMED,
    FOCUS_COLOR,
    GRAY,
    CYAN,
    RED,
    SECONDARY_COLOR,
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
from show_outdated import show_outdated 
from powermenu import show_power_menu

def bar_layout() -> bar.Bar:
    """
    Defines a nice layout for the status bar.

    :return: a Bar object that contains some widgets with decorations.
    """
    # decoration_group = get_decoration_group(BAR_NORMAL)
    decorations_left = get_decoration_group(BAR_CHOICE_LEFT)
    decorations_right = get_decoration_group(BAR_CHOICE_RIGHT)

    # some widgets look better with slightly other settings:
    workspace_decoration = decorations_left.copy()
    workspace_decoration["padding"] = 4
    workspace_decoration["decorations"][0] = RectDecoration(
        use_widget_background=True,
        padding_y=20,
        filled=True,
        radius=9,
    )


    wifi_decoration =  decorations_right.copy()
    wifi_decoration["padding"] = 8

    most_right_widget_deccoration = copy.deepcopy(decorations_right)
    most_right_widget_deccoration["decorations"] = [
        RectDecoration(
            use_widget_background=True,
            padding_y=-16,
            filled=True,
            radius=9,
        )
    ]

    tasklist_decorations = copy.deepcopy(decorations_right)
    tasklist_decorations["padding"] = 6


    dark_blue = dim_color(BLUE, DARK2)
    medium_blue = dim_color(BLUE, DARKER2)
    light_blue = dim_color(BLUE, DARKER)


    return bar.Bar(
        [
            extrawidgets.CurrentLayoutIcon(
                background=dim_color(SECONDARY_COLOR, DARKER2), 
                use_mask=True,
                margin_y=3,
                foreground=[
                    dim_color(FOCUS_COLOR, NEUTRAL),
                    dim_color(SECONDARY_COLOR, DIMMED),
                    dim_color(FOCUS_COLOR, NEUTRAL)],
                **decorations_left
            ),
            extrawidgets.GroupBox2(
                font="FiraCode Nerd Font",
                fontsize=19,
                highlight_method="block",
                background=dim_color(GRAY, DARK),
                hide_unused=True,
                rules=GROUPBOX_RULES,
                **workspace_decoration,
            ),
            # extrawidgets.WindowCount(
            #     background=dim_color(GRAY, MEDIUM2),
            #     font_shadow=dim_color(GRAY, DARK),
            #     text_format="  : {num}",
            #     **wifi_decoration
            #     ),
            # extrawidgets.WindowName(
            #     background=dim_color(GRAY, MEDIUM2),
            #     fontshadow=dim_color(GRAY, DARK),
            #     width=400,
            #     scroll=True,
            #     scroll_fixed_width=True,
            #     **decorations_right
            # ),
            extrawidgets.TaskList(
                background=dim_color(GRAY, DARKER),
                border=dim_color(FOCUS_COLOR, DIMMED),
                unfocused_border=dim_color(SECONDARY_COLOR, DARKER),
                fontshadow=dim_color(GRAY, DARK),
                scroll=True,
                highlight_method="block",
                max_title_width=200,
                txt_floating="  ",
                txt_maximized="  ",
                txt_minimized="  ",
                spacing=BORDER_WIDTH,
                **tasklist_decorations
                ),
            # extrawidgets.Spacer(
            #     background=dim_color(GRAY, MEDIUM2),
            #     hide_crash=True,
            #     **decorations_right,
            #     ),
            extrawidgets.WiFiIcon(
                background=dark_blue,
                interface="wlp2s0",
                wifi_arc=75,
                **wifi_decoration,
                ),
            extrawidgets.Bluetooth(
                background=dark_blue,
                fontsize=25,
                default_text="󰂯 {connected_devices}",
                **wifi_decoration,
                ),
            extrawidgets.CheckUpdates(
                background=dark_blue,
                distro="Arch_checkupdates",
                no_update_string="✅",
                display_format="󰚰  - {updates}",
                mouse_callbacks = {
                    "Button1": lazy.lazy.function(show_outdated)
                },
                **wifi_decoration,
                ),
            extrawidgets.Systray(
                background=dark_blue,
                hide_crash=True, # Systray tends to crash on reload because of singleton rule
                **decorations_right
                ),
            extrawidgets.Clock(
                background=medium_blue,
                #fontsize=11,
                format="%a %d.%m.%y",
                #**decorations_right,
            ),
            extrawidgets.AnalogueClock(
                background=medium_blue,
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
                background=light_blue,
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
                mode="bar",
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
            extrawidgets.Image(
                background=dim_color(RED, DIMMED2),
                colour=dim_color(RED, LIGHT / 2.),
                filename="~/Pictures/Icons/qtile/bar/logout.png",
                mask=True,
                margin_y=3,
                mouse_callbacks= {
                    "Button1": lazy.lazy.function(show_power_menu),
                    },
                **most_right_widget_deccoration,
            ),
        ],
        BAR_HEIGHT,
        # radius=10,
        # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
        # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
    )
